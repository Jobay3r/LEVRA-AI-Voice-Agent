import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

/**
 * Application Entry Point
 * 
 * Renders the main App component within React's StrictMode.
 * StrictMode enables additional development checks and warnings.
 * 
 * The createRoot API is part of React 18's concurrent rendering features.
 */
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
