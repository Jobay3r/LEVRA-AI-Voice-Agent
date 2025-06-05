from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)
from livekit.agents.multimodal import MultimodalAgent
from dotenv import load_dotenv
from api import AssistantFnc
from prompts import prompt_manager, build_conversation_prompt, get_welcome_message, get_instructions
import os
import sys
import importlib
import inspect
import requests
import json

# Load environment variables first to ensure API keys are available
load_dotenv(override=True)

# OPENAI CONFIGURATION
# ------------------------------------------------------------------------

def setup_openai_api():
    """
    Configure OpenAI API with the key from environment variables.
    Validates presence of API key and provides feedback.
    
    Returns:
        str: The OpenAI API key if valid
        
    Exits program if API key is missing or invalid.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("ERROR: OPENAI_API_KEY environment variable is not set or empty.")
        print("Please set your OpenAI API key in the .env file or as an environment variable.")
        print("Create a .env file in the project root with: OPENAI_API_KEY=your_actual_key_here")
        sys.exit(1)
    
    # Print a masked version of the API key for debugging
    masked_key = f"sk-...{openai_api_key[-4:]}" if len(openai_api_key) > 8 else "INVALID_KEY_FORMAT"
    print(f"Using OpenAI API key: {masked_key}")
    
    # Set environment variable (ensure it's available to child processes)
    os.environ["OPENAI_API_KEY"] = openai_api_key
    
    return openai_api_key

# Initialize OpenAI plugin on main thread
try:
    # Import the openai plugin after setting the environment variable
    from livekit.plugins import openai as lk_openai
    print("Successfully imported LiveKit OpenAI plugin on main thread.")
except Exception as e:
    print(f"ERROR: Failed to import OpenAI plugin: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def configure_model(api_key, pdf_context=""):
    """
    Configure the OpenAI realtime model for conversation.
    
    Args:
        api_key (str): OpenAI API key for authentication
        pdf_context (str): PDF document content to include in system instructions
        
    Returns:
        RealtimeModel: Configured OpenAI model for realtime conversation
        
    Exits program if model configuration fails.
    """
    try:        # Create enhanced instructions with PDF context if available
        if pdf_context:
            # Use optimized prompt system with document context
            base_instructions = get_instructions(has_document_context=True)
            enhanced_instructions = f"""
{base_instructions}

📄 DOCUMENT CONTEXT - YOU HAVE UPLOADED DOCUMENT ACCESS:
The user has uploaded a PDF document. You MUST acknowledge this and reference specific details from it.

=== USER'S DOCUMENT CONTENT ===
{pdf_context}
=== END DOCUMENT CONTENT ===

CRITICAL INSTRUCTIONS:
1. In your FIRST response, acknowledge that you have read their uploaded document
2. Reference specific details from the document to prove you understand their context
3. Use this content throughout the conversation to provide highly personalized coaching
4. Create scenarios and examples based on their specific organizational context
5. Answer questions about the document content with detailed, accurate information
"""
            print(f"📄 Enhanced model instructions with PDF context ({len(pdf_context)} chars)")
        else:
            enhanced_instructions = get_instructions(has_document_context=False)
            print("📄 Using standard model instructions (no PDF context)")
        
        # Create the model with the enhanced instructions
        model = lk_openai.realtime.RealtimeModel(
            api_key=api_key,
            instructions=enhanced_instructions,
            voice="shimmer",
            temperature=0.8,
            modalities=["audio", "text"],
        )
        return model
    except Exception as e:
        print(f"ERROR: Failed to configure OpenAI model: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# LIVEKIT AGENT IMPLEMENTATION
# ------------------------------------------------------------------------

async def entrypoint(ctx: JobContext):
    """
    Main entry point for the LiveKit agent.
    
    Initializes OpenAI, connects to LiveKit room, and manages the conversation flow.
    
    Args:
        ctx (JobContext): The LiveKit job context providing room access
    """
    # Set up OpenAI API globally
    openai_api_key = setup_openai_api()
    
    # Connect to LiveKit room and wait for participant
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()
      # Get room name for PDF context lookup
    room_name = ctx.room.name if ctx.room else "default"
    print(f"Agent connected to room: {room_name}")
      # Fetch PDF context if available - Enhanced version
    pdf_context = ""
    pdf_available = False
    
    def fetch_pdf_context():
        """Fetch PDF context with robust error handling and retries"""
        nonlocal pdf_context, pdf_available
        
        try:
            # Try multiple possible server URLs
            possible_urls = [
                f"http://localhost:5001/get-pdf-context/{room_name}",
                f"http://localhost:3001/get-pdf-context/{room_name}",
                f"http://127.0.0.1:5001/get-pdf-context/{room_name}",
                f"http://127.0.0.1:3001/get-pdf-context/{room_name}"
            ]
            
            for url in possible_urls:
                try:
                    print(f"Attempting to fetch PDF context from: {url}")
                    response = requests.get(url, timeout=3)
                    print(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        context_data = response.json()
                        print(f"PDF context response: {context_data}")
                        
                        if context_data.get("has_context"):
                            pdf_context = context_data.get("context", "")
                            pdf_available = True
                            print(f"✅ PDF context loaded from {url}: {len(pdf_context)} characters")
                            return True
                        else:
                            print(f"No PDF context available in room {room_name}")
                            return False
                            
                except requests.exceptions.RequestException as e:
                    print(f"Failed to connect to {url}: {e}")
                    continue
                    
            print("❌ Could not fetch PDF context from any server URL")
            return False
            
        except Exception as e:
            print(f"❌ Error fetching PDF context: {e}")
            return False
      # Initial PDF context fetch
    fetch_pdf_context()
    
    if pdf_available:
        print(f"✅ PDF context loaded: {len(pdf_context)} characters")
    else:
        print(f"ℹ️ No PDF context found for room {room_name}")
    
    try:
        # First create a client directly with correct API key
        print("Creating custom OpenAI client with API key")
        import openai as openai_official
        openai_official.api_key = openai_api_key
          # Initialize the OpenAI realtime model with API key and PDF context
        print("Creating RealtimeModel with explicit API key and PDF context")
        model = configure_model(openai_api_key, pdf_context if pdf_available else "")
        
        # Initialize assistant functionality and multimodal agent
        assistant_fnc = AssistantFnc()
        assistant = MultimodalAgent(model=model, fnc_ctx=assistant_fnc)
        
        # Start the assistant in the room
        print("Starting assistant in room...")
        assistant.start(ctx.room)
        print("Assistant started successfully")
          # Get the first session and prepare for conversation
        if not model.sessions:
            print("ERROR: No sessions available after starting the assistant")
            sys.exit(1)
            
        session = model.sessions[0]
        print(f"Session initialized with ID: {session.id if hasattr(session, 'id') else 'unknown'}")
        welcome_sent = False
          # EVENT HANDLERS
        # ------------------------------------------------------------
        
        @session.on("session_started")
        def on_session_started():
            """
            Handle session start event.
            Sends welcome message to the user only once.
            AI will read and acknowledge PDF content if available.
            """
            nonlocal welcome_sent
            if not welcome_sent:
                print("🚀 Starting conversation with PDF-aware AI")
                try:
                    # Create system instructions with PDF content
                    if pdf_available:
                        print(f"📄 Including PDF document ({len(pdf_context)} chars) in AI system instructions")
                          # Enhanced welcome that shows AI has read the document
                        base_welcome = get_welcome_message(has_document_context=True)
                        welcome_content = f"""I've just read through your uploaded PDF document and I'm ready to provide personalized coaching based on your specific context! 

{base_welcome}

Based on what I've read in your document, I can see [I'll reference specific details from your materials to show I understand your situation]. This gives me excellent context to make our training session highly relevant to your real-world needs.

What specific aspect would you like to focus on today? I can create scenarios directly based on your uploaded content or answer any questions you have about the materials."""
                          # Include the PDF content in the system message so AI can reference it
                        base_instructions = get_instructions(has_document_context=True)
                        system_instructions = f"""
{base_instructions}

📄 DOCUMENT CONTEXT - READ CAREFULLY:
You have access to the user's uploaded PDF document. The content is provided below. 
You MUST acknowledge that you have read this document and reference specific details from it.

=== USER'S DOCUMENT CONTENT ===
{pdf_context}
=== END DOCUMENT CONTENT ===

CRITICAL: In your first response, acknowledge that you have read their document and reference specific details to prove you understand their context. Use this content throughout the conversation to provide highly personalized coaching.
"""
                        
                        # Send system instructions first
                        session.conversation.item.create(
                            llm.ChatMessage(
                                role="system", 
                                content=system_instructions
                            )
                        )
                        
                    else:
                        print("📄 No PDF available - using standard welcome")
                        welcome_content = get_welcome_message(has_document_context=False)
                        
                        # Send standard system instructions
                        session.conversation.item.create(
                            llm.ChatMessage(
                                role="system",
                                content=get_instructions(has_document_context=False)
                            )
                        )
                    
                    # Send welcome message
                    session.conversation.item.create(
                        llm.ChatMessage(
                            role="assistant",
                            content=welcome_content
                        )
                    )
                    
                    session.response.create()
                    welcome_sent = True
                    print("✅ Welcome message sent with PDF integration")
                except Exception as e:
                    print(f"❌ Error sending welcome message: {str(e)}")
                    import traceback
                    traceback.print_exc()
        
        @session.on("user_speech_committed")
        def on_user_speech_committed(msg: llm.ChatMessage):
            """
            Process user speech after it's been committed.
            Ensures PDF context is maintained throughout conversation.
            
            Args:
                msg (ChatMessage): The message from the user
            """
            # Filter out empty messages
            if not msg.content:
                return
                
            if isinstance(msg.content, list):
                # Process multimodal content (text and images)
                content_items = [x for x in msg.content if x and (not isinstance(x, str) or x.strip())]
                if not content_items:
                    return
                    
                msg.content = "\n".join("[image]" if isinstance(x, llm.ChatImage) else x for x in content_items)
            elif isinstance(msg.content, str) and not msg.content.strip():
                # Skip empty string messages
                return
            
            # Add PDF context reminder for each user interaction if available
            if pdf_available and pdf_context:
                # Inject a context reminder into the conversation to keep AI aware
                context_reminder = f"""
[SYSTEM REMINDER: Continue referencing the user's uploaded PDF document throughout this conversation. 
Remember you have access to their specific context: {pdf_context[:200]}...]
"""
                session.conversation.item.create(
                    llm.ChatMessage(
                        role="system",
                        content=context_reminder
                    )
                )
                print("📄 Added PDF context reminder to conversation")
            
            # Route message based on user profile state    
            if assistant_fnc.has_profile():
                handle_query(msg)
            else:
                find_profile(msg)
            
        # CONVERSATION FLOW HANDLERS
        # ------------------------------------------------------------
        
        def find_profile(msg: llm.ChatMessage):
            """
            Handle conversation when user profile doesn't exist.
            Triggers skill assessment flow.
            
            Args:
                msg (ChatMessage): The message from the user
            """
            session.conversation.item.create(
                llm.ChatMessage(
                    role="system",
                    content=SKILL_ASSESSMENT_MESSAGE(msg)
                )
            )
            session.response.create()
            
        def handle_query(msg: llm.ChatMessage):
            """
            Handle regular conversation when user profile exists.
            
            Args:
                msg (ChatMessage): The message from the user
            """
            session.conversation.item.create(
                llm.ChatMessage(
                    role="user",
                    content=msg.content
                )
            )
            session.response.create()
            
        # PDF CONTEXT MANAGEMENT
        # ------------------------------------------------------------
        
        def refresh_pdf_context():
            """
            Refresh PDF context during an active conversation.
            This can be called when new PDFs are uploaded mid-conversation.
            """
            nonlocal pdf_context, pdf_available
            
            print(f"🔄 Refreshing PDF context for room {room_name}")
            
            # Re-fetch PDF context
            if fetch_pdf_context():
                print(f"✅ PDF context refreshed: {len(pdf_context)} characters")
                
                # Inject updated context into the active conversation
                if pdf_context:
                    updated_context = f"""
[SYSTEM UPDATE: New PDF document has been uploaded and processed. You now have access to additional context.

📄 UPDATED DOCUMENT CONTENT:
{pdf_context}

Please acknowledge this new information and offer to help with questions or scenarios based on the updated content. Reference specific details from the new document to show you understand the additional context.]
"""
                    
                    session.conversation.item.create(
                        llm.ChatMessage(
                            role="system",
                            content=updated_context
                        )
                    )
                    
                    # Send an acknowledgment message from the assistant
                    acknowledgment = """I've just received and read through your new PDF document! I can see the additional context you've provided, and I'm ready to incorporate this information into our conversation. 

Would you like me to focus on any specific aspects from your newly uploaded document? I can help you with questions, create scenarios, or provide coaching based on this fresh content."""
                    
                    session.conversation.item.create(
                        llm.ChatMessage(
                            role="assistant",
                            content=acknowledgment
                        )
                    )
                    
                    session.response.create()
                    print("🎯 Sent PDF context update acknowledgment to user")
                    
                return True
            else:
                print("❌ Failed to refresh PDF context")
                return False

        # PDF CONTEXT MONITORING
        # ------------------------------------------------------------
        
        import asyncio
        import os
        
        async def monitor_pdf_updates():
            """
            Monitor for PDF context update triggers.
            This runs in the background during the conversation.
            """
            trigger_file = f"pdf_update_trigger_{room_name}.flag"
            
            while True:
                try:
                    if os.path.exists(trigger_file):
                        print(f"🔔 PDF update trigger detected for room {room_name}")
                        refresh_pdf_context()
                        os.remove(trigger_file)  # Remove trigger file after processing
                        
                    await asyncio.sleep(2)  # Check every 2 seconds
                    
                except Exception as e:
                    print(f"❌ Error monitoring PDF updates: {e}")
                    await asyncio.sleep(5)  # Wait longer on error
        
        # Start PDF update monitoring in background
        asyncio.create_task(monitor_pdf_updates())
        
        # ...existing code...
    except Exception as e:
        print(f"ERROR: Failed to initialize OpenAI connection: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
# APPLICATION ENTRY POINT
# ------------------------------------------------------------------------

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))