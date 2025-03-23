# Prerequisites:

Python 3.9+
Node.js and npm
LiveKit account and API credentials
OpenAI API key

# Create a virtual environment named 'ai'

python -m venv ai

# On Windows: (to activate the virtual environment)

ai\Scripts\activate

# On macOS/Linux: (to activate the virtual environment)

source ai/bin/activate

# Make sure your virtual environment is activated

cd backend
pip install -r requirements.txt

yarn add @livekit/components-react @livekit/components-styles livekit-client

# Check if the .env file contains all the required values in the backend directory

OPENAI_API_KEY
LIVEKIT_URL
LIVEKIT_API_SECRET
LIVEKIT_API_KEY

# Check if the .env file contains all the required values in the frontend directory

VITE_LIVEKIT_URL (same as LIVEKIT_URL)

# Step 4: Install Frontend Dependencies

cd ../frontend
npm install

### open 3 different terminal

### 1st terminal

ai\Scripts\activate

cd backend
python server.py

### 2nd terminal

ai\Scripts\activate

cd backend
python agent.py start

### 3rd terminal

cd frontend
npm run dev

# Navigate to the URL:

http://localhost:5173

# Using the Application:

1.Click on "Start Career Mentoring Session"
2.Enter your name when prompted (it will store in the livekit server)
3.Make sure you allow microphone access when requested (Make sure your browser has permission to use your microphone)
4.Start speaking with the AI voice assistant
