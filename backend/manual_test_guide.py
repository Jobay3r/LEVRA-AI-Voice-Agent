#!/usr/bin/env python3
"""
Manual test instructions for PDF integration
"""

print("""
🧪 MANUAL PDF INTEGRATION TEST GUIDE
====================================

Follow these steps to test the PDF integration:

STEP 1: Start the Flask Server
------------------------------
1. Open a new terminal
2. cd "c:\\Users\\Jobay\\Documents\\AI Projects\\voice Assistant with ui\\LEVRA\\LEVRA\\backend"
3. python server.py
4. Verify you see: "Running on http://0.0.0.0:5001"

STEP 2: Start the Frontend
--------------------------
1. Open another terminal
2. cd "c:\\Users\\Jobay\\Documents\\AI Projects\\voice Assistant with ui\\LEVRA\\LEVRA\\frontend"
3. npm run dev
4. Open browser to http://localhost:5174

STEP 3: Test PDF Upload
-----------------------
1. Click "Start Your Human Skills Journey"
2. Enter your name and click "Begin Training"
3. Look for "Room ID: room-xxxxxxxx" display
4. Drag and drop the PDF file or click to upload
5. Check browser console for upload success message
6. Verify "📄 PDF context loaded" appears

STEP 4: Verify Backend Storage
------------------------------
1. In browser console, note the Room ID
2. Test the context endpoint:
   http://localhost:5001/get-pdf-context/[YOUR_ROOM_ID]
3. Should return: {"has_context": true, "context": "...", "metadata": {...}}

STEP 5: Test Agent Integration
------------------------------
1. Start the LiveKit agent:
   python agent.py start
2. In the browser, start talking to test the voice assistant
3. The agent should include PDF context in its responses

TROUBLESHOOTING:
================

❌ PDF upload fails:
   - Check Flask server is running on port 5001
   - Check PDF file exists in backend folder
   - Check browser console for error messages

❌ No Room ID shown:
   - Check browser console for room extraction logs
   - Manually refresh the page

❌ Agent doesn't use PDF context:
   - Check agent console logs for "PDF context loaded"
   - Verify room ID matches between upload and agent
   - Check agent can reach Flask server on localhost:5001

❌ Context not found:
   - Verify upload was successful first
   - Check if room ID in agent matches upload room ID
   - Try the context endpoint manually in browser

EXPECTED BEHAVIOR:
==================
✅ PDF uploads successfully
✅ Room ID is displayed and consistent
✅ Context endpoint returns PDF content
✅ Agent includes PDF context in welcome message
✅ Voice conversation references uploaded document

""")

# Quick server connectivity test
try:
    import requests
    response = requests.get("http://localhost:5001/get-pdf-context/test", timeout=2)
    print("🟢 Flask server is reachable")
    print(f"   Status: {response.status_code}")
except:
    print("🔴 Flask server is not reachable")
    print("   Start server.py first!")
