import os
from livekit import api
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from livekit.api import LiveKitAPI, ListRoomsRequest
import uuid
from pdf_processor import pdf_processor

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application with CORS support for all origins
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global storage for PDF context (in production, use Redis/database)
pdf_contexts = {}

# ROOM MANAGEMENT FUNCTIONS
# ------------------------------------------------------------------------

async def generate_room_name():
    """
    Generate a unique room name with UUID to ensure uniqueness.
    Verifies the name doesn't already exist in LiveKit.
    
    Returns:
        str: A unique room name in the format "room-{uuid}"
    """
    name = "room-" + str(uuid.uuid4())[:8]
    rooms = await get_rooms()
    while name in rooms:
        name = "room-" + str(uuid.uuid4())[:8]
    return name

async def get_rooms():
    """
    Retrieve a list of all room names currently in LiveKit server.
    
    Returns:
        list: List of room names as strings
    """
    api = LiveKitAPI()
    rooms = await api.room.list_rooms(ListRoomsRequest())
    await api.aclose()
    return [room.name for room in rooms.rooms]

# API ENDPOINTS
# ------------------------------------------------------------------------

@app.route("/getToken")
async def get_token():
    """
    Endpoint to generate LiveKit tokens for clients.
    
    Query parameters:
        name: User's display name (defaults to "my name")
        room: Room ID (generates new room if not provided)
        
    Returns:
        str: JWT token for LiveKit authentication
    """
    name = request.args.get("name", "my name")
    room = request.args.get("room", None)
    
    if not room:
        room = await generate_room_name()
        
    token = api.AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET")) \
        .with_identity(name)\
        .with_name(name)\
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room
        ))
    
    return token.to_jwt()

@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    """
    Endpoint to handle PDF file uploads and extract text content.
    
    Form data:
        pdf_file: PDF file to process
        room_id: Optional room ID to associate with the PDF context
        
    Returns:
        JSON: Processing result with extracted text metadata
    """
    try:
        # Check if file is present
        if 'pdf_file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No PDF file provided"
            }), 400
        
        pdf_file = request.files['pdf_file']
        room_id = request.form.get('room_id', 'default')
        
        # Validate file
        if pdf_file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({
                "success": False,
                "error": "Only PDF files are supported"
            }), 400
        
        # Process PDF
        result = pdf_processor.extract_text_from_pdf(pdf_file)
        
        if result["success"]:
            # Store context for the room/session
            context_prompt = pdf_processor.create_context_prompt(
                result["text"], 
                result["metadata"]
            )
            pdf_contexts[room_id] = {
                "context": context_prompt,
                "metadata": result["metadata"],
                "timestamp": "2025-06-05"  # You can use datetime.now()
            }
            
            return jsonify({
                "success": True,
                "message": "PDF processed successfully",
                "metadata": result["metadata"],
                "room_id": room_id
            })
        else:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/get-pdf-context/<room_id>")
def get_pdf_context(room_id):
    """
    Retrieve PDF context for a specific room.
    
    Args:
        room_id: Room identifier
        
    Returns:
        JSON: PDF context data or empty if not found
    """
    context = pdf_contexts.get(room_id, {})
    return jsonify({
        "has_context": bool(context),
        "context": context.get("context", ""),
        "metadata": context.get("metadata", {})
    })

@app.route("/notify-pdf-update/<room_id>", methods=["POST"])
def notify_pdf_update(room_id):
    """
    Notify about a PDF context update during an active conversation.
    This endpoint can be used to trigger re-initialization or context refresh
    for ongoing AI sessions.
    
    Args:
        room_id: Room identifier
        
    Returns:
        JSON: Update notification result
    """
    try:
        # Check if context exists for the room
        context = pdf_contexts.get(room_id, {})
        
        if context:
            # Create a trigger file for the agent to detect
            trigger_file = f"pdf_update_trigger_{room_id}.flag"
            
            try:
                with open(trigger_file, 'w') as f:
                    f.write(f"PDF update trigger for room {room_id} at {os.getcwd()}")
                
                print(f"📄 Created PDF update trigger file: {trigger_file}")
                
            except Exception as e:
                print(f"❌ Error creating trigger file: {e}")
            
            print(f"📄 PDF context update notification for room {room_id}")
            return jsonify({
                "success": True,
                "message": "PDF context update notification sent",
                "room_id": room_id,
                "has_context": True,
                "context_length": len(context.get("context", ""))
            })
        else:
            return jsonify({
                "success": False,
                "error": "No PDF context found for this room"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

# APPLICATION ENTRY POINT
# ------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)