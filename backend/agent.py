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
from prompts import WELCOME_MESSAGE, INSTRUCTIONS, SKILL_ASSESSMENT_MESSAGE, PROVIDE_FEEDBACK
import os
import sys
import importlib
import inspect

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

def configure_model(api_key):
    """
    Configure the OpenAI realtime model for conversation.
    
    Args:
        api_key (str): OpenAI API key for authentication
        
    Returns:
        RealtimeModel: Configured OpenAI model for realtime conversation
        
    Exits program if model configuration fails.
    """
    try:
        # Create the model with the API key
        model = lk_openai.realtime.RealtimeModel(
            api_key=api_key,
            instructions=INSTRUCTIONS,
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
    
    try:
        # First create a client directly with correct API key
        print("Creating custom OpenAI client with API key")
        import openai as openai_official
        openai_official.api_key = openai_api_key
        
        # Initialize the OpenAI realtime model with API key
        print("Creating RealtimeModel with explicit API key")
        model = configure_model(openai_api_key)
        
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
            """
            nonlocal welcome_sent
            if not welcome_sent:
                print("Sending welcome message to user")  # Debug log
                try:
                    session.conversation.item.create(
                        llm.ChatMessage(
                            role="assistant",
                            content=WELCOME_MESSAGE
                        )
                    )
                    session.response.create()
                    welcome_sent = True
                    print("Welcome message sent successfully")  # Debug log
                except Exception as e:
                    print(f"Error sending welcome message: {str(e)}")
                    import traceback
                    traceback.print_exc()
        
        @session.on("user_speech_committed")
        def on_user_speech_committed(msg: llm.ChatMessage):
            """
            Process user speech after it's been committed.
            Routes to profile creation or query handling based on state.
            
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
            
    except Exception as e:
        print(f"ERROR: Failed to initialize OpenAI connection: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
# APPLICATION ENTRY POINT
# ------------------------------------------------------------------------

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))