import {
  useVoiceAssistant,
  BarVisualizer,
  VoiceAssistantControlBar,
  useTrackTranscription,
  useLocalParticipant,
} from "@livekit/components-react";
import { Track } from "livekit-client";
import { useEffect, useState } from "react";
import "./SimpleVoiceAssistant.css";
import logoGif from "../assets/Reputy_Logo_full_animation_BIG.gif";

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

  // Merge and sort agent and user transcriptions by timestamp
  useEffect(() => {
    const allMessages = [
      ...(agentTranscriptions?.map((t) => ({ ...t, type: "agent" })) ?? []),
      ...(userTranscriptions?.map((t) => ({ ...t, type: "user" })) ?? []),
    ].sort((a, b) => a.firstReceivedTime - b.firstReceivedTime);
    setMessages(allMessages);
  }, [agentTranscriptions, userTranscriptions]);

  return (
    <div className="voice-assistant-container">
      {/* Branding and logo section */}
      <div className="logo-container">
        <img src={logoGif} alt="Reputy Logo Animation" className="logo-animation" />
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
            /* Render conversation messages when available */
            messages.map((msg, index) => (
              <Message key={msg.id || index} type={msg.type} text={msg.text} />
            ))
          ) : (
            /* Show guidance tips when no conversation has started */
            <div className="tips-section">
              <h3>Tips for your career discussion:</h3>
              <ul className="tips-list">
                <li>Share your dream job or career aspiration</li>
                <li>Mention your educational background and current skills</li>
                <li>Ask about specific soft skills you want to develop</li>
                <li>Request resources for skill development</li>
                <li>Discuss how to overcome career challenges</li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SimpleVoiceAssistant;
