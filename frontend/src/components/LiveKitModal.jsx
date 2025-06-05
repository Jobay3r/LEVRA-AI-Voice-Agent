import { useState, useCallback } from "react";
import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react";
import "@livekit/components-styles";
import SimpleVoiceAssistant from "./SimpleVoiceAssistant";

/**
 * LiveKitModal Component
 * 
 * A modal interface for connecting to a LiveKit room and 
 * interacting with the AI voice assistant.
 * 
 * Responsibilities:
 * 1. Handle user name collection
 * 2. Manage LiveKit room connection
 * 3. Provide modal interface with close functionality
 * 4. Integrate audio renderer and voice assistant components
 * 
 * @param {Object} props - Component properties
 * @param {Function} props.setShowSupport - Function to control modal visibility
 */
const LiveKitModal = ({ setShowSupport }) => {
  // State management for user flow
  const [isSubmittingName, setIsSubmittingName] = useState(true);
  const [name, setName] = useState("");
  const [token, setToken] = useState(null);

  /**
   * Request a LiveKit token from the backend API
   * 
   * @param {string} userName - The user's display name
   */
  const getToken = useCallback(async (userName) => {
    try {
      console.log("Connecting to Career Mentor")
      const response = await fetch(
        `/api/getToken?name=${encodeURIComponent(userName)}`
      );
      const token = await response.text();
      setToken(token);
      setIsSubmittingName(false);
    } catch (error) {
      console.error(error);
    }
  }, []);

  /**
   * Handle form submission for user name
   * Prevents default form behavior and requests token if name is valid
   * 
   * @param {Event} e - Form submit event
   */
  const handleNameSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      getToken(name);
    }
  };

  /**
   * Close the modal and reset state
   */
  const handleModalClose = () => {
    setShowSupport(false);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-button" onClick={handleModalClose}>×</button>
        <div className="support-room">
          {/* Step 1: Name collection form */}
          {isSubmittingName ? (
            <form onSubmit={handleNameSubmit} className="name-form">
              <h2>Start Your Human Skills Journey</h2>
              <p>Enter your name to begin immersive skills training</p>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
                required
              />
              <button type="submit">Begin Training</button>
              <button
                type="button"
                className="cancel-button"
                onClick={() => setShowSupport(false)}
              >
                Cancel
              </button>
            </form>
          ) : token ? (
            /* Step 2: LiveKit room connection */
            <LiveKitRoom
              serverUrl={import.meta.env.VITE_LIVEKIT_URL}
              token={token}
              connect={true}
              video={false}
              audio={true}
              onDisconnected={() => {
                setShowSupport(false);
                setIsSubmittingName(true);
              }}
              style={{ height: '100%', width: '100%' }}
            >
              {/* Audio rendering for room participants */}
              <RoomAudioRenderer />
              {/* Voice assistant UI with controls and visualization */}
              <SimpleVoiceAssistant />
            </LiveKitRoom>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default LiveKitModal;
