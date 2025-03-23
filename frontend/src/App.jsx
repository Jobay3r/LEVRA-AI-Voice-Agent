import { useState } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';
import logoGif from "./assets/Reputy_Logo_full_animation_BIG.gif";

/**
 * App Component
 * 
 * Main application component that serves as the entry point for the UI.
 * Handles the display of the landing page and initializes the mentoring session.
 * 
 * Component Structure:
 * - Hero section with logo, tagline and description
 * - Call-to-action button to start mentoring
 * - Modal for LiveKit integration (appears when session starts)
 */
function App() {
  // State to control the visibility of the support modal
  const [showSupport, setShowSupport] = useState(false);

  /**
   * Handler for the support button click
   * Shows the LiveKit modal for starting a mentoring session
   */
  const handleSupportClick = () => {
    setShowSupport(true)
  }

  return (
    <div className="app">
      <main className="main-content">
        {/* Logo and branding section */}
        <div className="logo-container-main">
          <img src={logoGif} alt="Reputy Logo Animation" className="logo-animation-main" />
        </div>
        
        {/* Main marketing content */}
        <h1 className="tagline">AI-Powered Career Guidance</h1>
        
        <p className="description">
          Connect with our intelligent assistant to explore career opportunities, 
          develop essential skills, and create a personalized path to professional success.
        </p>
        
        {/* Primary call-to-action */}
        <button className="mentor-button" onClick={handleSupportClick}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm-1-5h2v2h-2v-2zm2-1.645V14h-2v-1.5a1 1 0 0 1 1-1 1.5 1.5 0 1 0-1.471-1.794l-1.962-.393A3.5 3.5 0 1 1 13 13.355z"/>
          </svg>
          Start Career Mentoring Session
        </button>
      </main>

      {/* Conditionally render the LiveKit modal when showSupport is true */}
      {showSupport && <LiveKitModal setShowSupport={setShowSupport}/>}
    </div>
  )
}

export default App
