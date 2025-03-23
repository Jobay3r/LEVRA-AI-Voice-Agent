import os
from livekit import api
from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
from livekit.api import LiveKitAPI, ListRoomsRequest
import uuid

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application with CORS support for all origins
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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

# APPLICATION ENTRY POINT
# ------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)