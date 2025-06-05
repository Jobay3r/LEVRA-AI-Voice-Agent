import {
  useVoiceAssistant,
  BarVisualizer,
  VoiceAssistantControlBar,
  useTrackTranscription,
  useLocalParticipant,
} from "@livekit/components-react";
import { Track } from "livekit-client";
import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import "./SimpleVoiceAssistant.css";
import levraLogo from "../assets/LEVRA2.png";
import PDFUploader from "./PDFUploader";

/**
 * Message Component
 * 
 * A presentational component for displaying conversation messages
 * with different styling based on the sender type.
 * 
 * @param {Object} props - Component properties
 * @param {string} props.type - Message type ('agent' or 'user')
 * @param {string} props.text - Message content
 */
const Message = ({ type, text }) => {
  return (
    <div className={`message message-${type}`}>
      <span className="message-text">{text}</span>
    </div>
  );
};

Message.propTypes = {
  type: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired
};

/**
 * SimpleVoiceAssistant Component
 * 
 * Core UI for the voice assistant interaction, featuring:
 * - Audio visualization
 * - Control bar for mic/settings
 * - Real-time conversation display
 * - Interactive guidance for users
 * 
 * Uses LiveKit hooks to manage audio state, transcriptions,
 * and participant information.
 */
const SimpleVoiceAssistant = () => {
  // Access LiveKit voice assistant state and tracks
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();
  const localParticipant = useLocalParticipant();
  
  // Get transcriptions from the user's microphone
  const { segments: userTranscriptions } = useTrackTranscription({
    publication: localParticipant.microphoneTrack,
    source: Track.Source.Microphone,
    participant: localParticipant.localParticipant,
  });
  // Combined conversation messages state
  const [messages, setMessages] = useState([]);
  const [hasPdfContext, setHasPdfContext] = useState(false);
  const [showPdfUploader, setShowPdfUploader] = useState(true);
  const [showMidConversationUploader, setShowMidConversationUploader] = useState(false);
  const [roomId, setRoomId] = useState(null);  // Get room ID from LiveKit room with better debugging
  useEffect(() => {
    // Try multiple sources for room ID
    let extractedRoomId = null;
    
    console.log('Extracting room ID from:', localParticipant);
    
    // Method 1: From local participant room name
    if (localParticipant.localParticipant?.roomName) {
      extractedRoomId = localParticipant.localParticipant.roomName;
      console.log('Room ID from localParticipant.roomName:', extractedRoomId);
    }
    // Method 2: From room object (different property path)
    else if (localParticipant.localParticipant?.room?.name) {
      extractedRoomId = localParticipant.localParticipant.room.name;
      console.log('Room ID from room.name:', extractedRoomId);
    }
    // Method 3: Check if room info is available via different path
    else if (localParticipant.room?.name) {
      extractedRoomId = localParticipant.room.name;
      console.log('Room ID from room.name (alt path):', extractedRoomId);
    }
    // Method 4: From URL params as fallback
    else if (window.location.search) {
      const urlParams = new URLSearchParams(window.location.search);
      const roomFromUrl = urlParams.get('room');
      if (roomFromUrl) {
        extractedRoomId = roomFromUrl;
        console.log('Room ID from URL params:', extractedRoomId);
      }
    }
    
    if (extractedRoomId && extractedRoomId !== roomId) {
      console.log('Setting room ID:', extractedRoomId);
      setRoomId(extractedRoomId);    } else if (!extractedRoomId && !roomId) {
      // Generate a fallback room ID if none found
      const fallbackRoomId = 'room-' + Math.random().toString(36).substring(2, 10);
      console.log('Generated fallback room ID:', fallbackRoomId);
      setRoomId(fallbackRoomId);
    }
  }, [localParticipant, roomId]);

  // Merge and sort agent and user transcriptions by timestamp
  useEffect(() => {
    const allMessages = [
      ...(agentTranscriptions?.map((t) => ({ ...t, type: "agent" })) ?? []),
      ...(userTranscriptions?.map((t) => ({ ...t, type: "user" })) ?? []),
    ].sort((a, b) => a.firstReceivedTime - b.firstReceivedTime);
    setMessages(allMessages);
  }, [agentTranscriptions, userTranscriptions]);  // PDF Upload handlers
  const handlePdfUploadSuccess = (result) => {
    console.log('PDF uploaded successfully:', result);
    console.log('Room ID used for upload:', roomId);
    setHasPdfContext(true);
    setShowPdfUploader(false);
    setShowMidConversationUploader(false);
    
    // If this is a mid-conversation upload, notify the AI
    if (messages.length > 0) {
      console.log('Mid-conversation PDF upload detected, notifying AI...');
      notifyPdfUpdate(roomId);
    }
  };

  const notifyPdfUpdate = async (roomId) => {
    try {
      const response = await fetch(`http://localhost:5001/notify-pdf-update/${roomId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('PDF update notification sent:', result);
        
        // Add a system message to indicate the PDF has been uploaded
        const systemMessage = {
          id: `system-${Date.now()}`,
          type: 'system',
          text: '📄 New PDF document uploaded and processed. The AI now has access to additional context.',
          firstReceivedTime: Date.now()
        };
        
        setMessages(prevMessages => [...prevMessages, systemMessage]);
      } else {
        console.error('Failed to notify about PDF update');
      }
    } catch (error) {
      console.error('Error notifying about PDF update:', error);
    }
  };

  const handlePdfUploadError = (error) => {
    console.error('PDF upload error:', error);
    console.error('Room ID when error occurred:', roomId);
    // Keep uploader visible on error so user can try again
  };

  const resetPdfUploader = () => {
    setHasPdfContext(false);
    setShowPdfUploader(true);
    setShowMidConversationUploader(false);
  };

  const toggleMidConversationUploader = () => {
    setShowMidConversationUploader(!showMidConversationUploader);
  };
  return (
    <div className="voice-assistant-container">      {/* PDF Upload Section - Show before conversation starts */}
      {showPdfUploader && messages.length === 0 && (
        <div>
          {/* Debug info for room ID */}
          {roomId && (
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '10px' }}>
              Room ID: {roomId}
            </div>
          )}
          <PDFUploader
            onUploadSuccess={handlePdfUploadSuccess}
            onUploadError={handlePdfUploadError}
            roomId={roomId}
          />
        </div>
      )}      {/* PDF Context Indicator */}
      {hasPdfContext && (
        <div className="pdf-context-indicator">
          <span>📄 PDF context loaded</span>
          <div>
            <button onClick={resetPdfUploader} className="reset-pdf-btn">
              Upload different PDF
            </button>
            {messages.length > 0 && (
              <button onClick={toggleMidConversationUploader} className="reset-pdf-btn" style={{marginLeft: '8px'}}>
                {showMidConversationUploader ? 'Hide uploader' : 'Add more PDFs'}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Mid-conversation PDF uploader */}
      {showMidConversationUploader && messages.length > 0 && (
        <div className="mid-conversation-uploader">
          <h4 style={{color: '#86efac', margin: '0 0 10px 0', fontSize: '14px'}}>
            📄 Add additional document context:
          </h4>
          <PDFUploader
            onUploadSuccess={handlePdfUploadSuccess}
            onUploadError={handlePdfUploadError}
            roomId={roomId}
          />
        </div>
      )}
      
      {/* Branding and logo section */}
      <div className="logo-container">
        <img src={levraLogo} alt="LEVRA - Human Skills Training Platform" className="logo-animation" />
      </div>
      
      {/* Audio visualization component */}
      <div className="visualizer-container">
        <BarVisualizer state={state} barCount={14} trackRef={audioTrack} />
      </div>
      
      {/* Controls and conversation section */}
      <div className="control-section">
        {/* Microphone controls, settings and status */}
        <VoiceAssistantControlBar />
          {/* Conversation display area */}
        <div className="conversation">
          {messages.length > 0 ? (
            <div>
              {/* Mid-conversation PDF upload option for conversations without context */}
              {!hasPdfContext && !showMidConversationUploader && (
                <div className="mid-conversation-pdf-suggestion">
                  <button onClick={toggleMidConversationUploader} className="add-pdf-mid-conversation-btn">
                    📄 Add PDF context to enhance this conversation
                  </button>
                </div>
              )}
              
              {/* Render conversation messages when available */}
              {messages.map((msg, index) => (
                <Message key={msg.id || index} type={msg.type} text={msg.text} />
              ))}
            </div>
          ) : (
            /* Show guidance tips when no conversation has started */
            <div className="tips-section">
              <h3>Ready for Immersive Human Skills Training? 🚀</h3>
              <ul className="tips-list">
                <li>🎯 Choose your focus: communication, leadership, teamwork, or conflict resolution</li>
                <li>🏢 Tell me your role/industry for realistic workplace scenarios</li>
                <li>💪 Jump into interactive practice situations</li>
                <li>📊 Get instant feedback with specific skill scores</li>
                <li>🔄 Adapt your learning path based on real-time performance</li>
                <li>🛡️ Practice safely - make mistakes and learn without consequences</li>
              </ul>
              {!showPdfUploader && !hasPdfContext && (
                <div className="upload-suggestion">
                  <p>💡 <strong>Tip:</strong> Upload a PDF document to make our conversation more relevant to your specific needs!</p>
                  <button onClick={resetPdfUploader} className="upload-pdf-btn">
                    📄 Upload PDF
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SimpleVoiceAssistant;
