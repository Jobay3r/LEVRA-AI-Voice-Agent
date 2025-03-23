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

const Message = ({ type, text }) => {
  return (
    <div className={`message message-${type}`}>
      <span className="message-text">{text}</span>
    </div>
  );
};

const SimpleVoiceAssistant = () => {
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();
  const localParticipant = useLocalParticipant();
  const { segments: userTranscriptions } = useTrackTranscription({
    publication: localParticipant.microphoneTrack,
    source: Track.Source.Microphone,
    participant: localParticipant.localParticipant,
  });

  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const allMessages = [
      ...(agentTranscriptions?.map((t) => ({ ...t, type: "agent" })) ?? []),
      ...(userTranscriptions?.map((t) => ({ ...t, type: "user" })) ?? []),
    ].sort((a, b) => a.firstReceivedTime - b.firstReceivedTime);
    setMessages(allMessages);
  }, [agentTranscriptions, userTranscriptions]);

  return (
    <div className="voice-assistant-container">
      <div className="visualizer-container">
        <BarVisualizer state={state} barCount={12} trackRef={audioTrack} />
      </div>
      
      <div className="control-section">
        <VoiceAssistantControlBar />
        <div className="conversation">
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <Message key={msg.id || index} type={msg.type} text={msg.text} />
            ))
          ) : (
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
