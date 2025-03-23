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
from prompts import WELCOME_MESSAGE, INSTRUCTIONS, SKILL_ASSESSMENT_MESSAGE, PROVIDE_SUGGESTIONS
import os
import sys
import importlib
import inspect

# Load environment variables first - make sure this is at the very top
load_dotenv(override=True)

# Setup OpenAI globally
def setup_openai_api():
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

# Configure the model without patching
def configure_model(api_key):
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

async def entrypoint(ctx: JobContext):
    # Set up OpenAI API globally
    openai_api_key = setup_openai_api()
    
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
        
        assistant_fnc = AssistantFnc()
        assistant = MultimodalAgent(model=model, fnc_ctx=assistant_fnc)
        
        assistant.start(ctx.room)
        
        session = model.sessions[0]
        session.conversation.item.create(
            llm.ChatMessage(
                role="assistant",
                content=WELCOME_MESSAGE
            )
        )
        session.response.create()
        
        @session.on("user_speech_committed")
        def on_user_speech_committed(msg: llm.ChatMessage):
            if isinstance(msg.content, list):
                msg.content = "\n".join("[image]" if isinstance(x, llm.ChatImage) else x for x in msg)
                
            if assistant_fnc.has_profile():
                handle_query(msg)
            else:
                find_profile(msg)
            
        def find_profile(msg: llm.ChatMessage):
            session.conversation.item.create(
                llm.ChatMessage(
                    role="system",
                    content=SKILL_ASSESSMENT_MESSAGE(msg)
                )
            )
            session.response.create()
            
        def handle_query(msg: llm.ChatMessage):
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
    
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))