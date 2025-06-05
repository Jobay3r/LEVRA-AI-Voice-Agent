# Prerequisites:

Python 3.9+
Node.js and npm
LiveKit account and API credentials
OpenAI API key

# Create a virtual environment named 'ai' (can be any name)

python -m venv ai

# On Windows: (to activate the virtual environment)

ai\Scripts\activate

# On macOS/Linux: (to activate the virtual environment)

source ai/bin/activate

# Make sure your virtual environment is activated

cd backend
pip install -r ./ai/requirements.txt

# Check if the .env file contains all the required values in the backend directory

OPENAI_API_KEY
LIVEKIT_URL
LIVEKIT_API_SECRET
LIVEKIT_API_KEY

# Check if the .env file contains all the required values in the frontend directory

VITE_LIVEKIT_URL (same as LIVEKIT_URL)

# Install Frontend Dependencies

cd ../frontend
npm install

yarn add @livekit/components-react @livekit/components-styles livekit-client

# open 3 different terminal

### 1st terminal

ai\Scripts\activate

python .\backend\server.py

### 2nd terminal

ai\Scripts\activate

python .\backend\agent.py start

### 3rd terminal

cd frontend

npm run dev

# Navigate to the URL:

http://localhost:5173

# Using the Application:

1. **Launch the Application**: Navigate to `http://localhost:5173` in your web browser
2. **Start Your Session**: Click on "Start Career Mentoring Session" button
3. **Enter Your Details**: When prompted, enter your name (this will be stored on the LiveKit server for session management)

## Audio Setup

4. **Grant Microphone Access**:
   - Your browser will request microphone permissions
   - Click "Allow" when prompted
   - **Important**: Ensure your browser has permission to access your microphone in browser settings
   - Test your microphone beforehand to ensure it's working properly

## Interacting with LEVRA

5. **Begin Conversation**: Start speaking naturally with the AI voice assistant
6. **Follow the Flow**:
   - LEVRA will greet you and ask about your role and skills you want to practice
   - Engage in realistic workplace scenarios designed for your specific needs
   - Receive real-time feedback and scoring on your performance

## Tips for Best Experience

- **Speak Clearly**: Use a normal conversational tone
- **Wait for Responses**: Allow LEVRA to finish speaking before responding
- **Be Specific**: When asked about your role or skills, provide detailed information for better personalized scenarios
- **Practice Actively**: Engage fully in the scenarios as if they were real workplace situations
- **Use Feedback**: Pay attention to the scoring and suggestions provided after each interaction

## Troubleshooting

- **No Audio**: Check microphone permissions in browser settings
- **Connection Issues**: Ensure all three terminals are running (server, agent, frontend)
- **Performance Issues**: Close other browser tabs and applications for optimal performance
