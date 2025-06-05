import { useState } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';
import levraLogo from "./assets/LEVRA2.png";

/**
 * App Component
 * 
 * Main application component for LEVRA - Human Skills Training Platform.
 * Provides immersive VR and AI-powered learning experiences for Gen Z.
 * 
 * Component Structure:
 * - Hero section with LEVRA branding and value proposition
 * - Call-to-action button to start training session
 * - Modal for LiveKit integration (appears when session starts)
 */
function App() {
  // State to control the visibility of the support modal
  const [showSupport, setShowSupport] = useState(false);

  /**
   * Handler for the training session button click
   * Shows the LiveKit modal for starting an AI-powered learning session
   */
  const handleSupportClick = () => {
    setShowSupport(true)
  }

  return (
    <div className="app">
      <main className="main-content">
        {/* Logo and branding section */}
        <div className="logo-container-main">
          <img src={levraLogo} alt="LEVRA - Human Skills Training Platform" className="logo-animation-main" />
        </div>
        
        {/* Hero section with main messaging */}
        <div className="hero-section">
          <h1 className="hero-headline">There's a growing Soft Skills Gap.</h1>
          <h2 className="hero-solution">LEVRA is here to solve it.</h2>
          
          <p className="hero-description">
            LEVRA trains employees' Human Skills through immersive and personalised learning.<br />
            We focus on soft skills training for Gen Z.
          </p>
          
          {/* Primary call-to-action */}
          <button className="hero-cta-button" onClick={handleSupportClick}>
            START TRAINING NOW
          </button>
        </div>
      </main>

      {/* Conditionally render the LiveKit modal when showSupport is true */}
      {showSupport && <LiveKitModal setShowSupport={setShowSupport}/>}
    </div>
  )
}

export default App
