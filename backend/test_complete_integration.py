#!/usr/bin/env python3
"""
Comprehensive test to simulate the complete PDF upload and agent integration flow
"""

import requests
import os
import json
import time
from datetime import datetime

def test_complete_pdf_integration():
    """Test the complete PDF integration flow"""
    
    pdf_path = "Hackathon -  LEVRA Deck.pdf"
    test_room_id = "room-12345678"  # Simulate the format used by the backend
    base_url = "http://localhost:5001"
    
    print("🧪 COMPREHENSIVE PDF INTEGRATION TEST")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Testing room ID: {test_room_id}")
    print(f"📄 PDF file: {pdf_path}")
    print("")
    
    # Step 1: Verify PDF file exists
    print("📋 STEP 1: Verify PDF file exists")
    print("-" * 30)
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    print(f"✅ PDF file found: {os.path.getsize(pdf_path)} bytes")
    print("")
    
    # Step 2: Test Flask server connectivity
    print("📋 STEP 2: Test Flask server connectivity")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/get-pdf-context/test", timeout=5)
        if response.status_code == 200:
            print("✅ Flask server is running and responsive")
        else:
            print(f"❌ Flask server returned unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Flask server: {e}")
        print("💡 Make sure server.py is running on port 5001")
        return False
    print("")
    
    # Step 3: Upload PDF
    print("📋 STEP 3: Upload PDF to Flask server")
    print("-" * 30)
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'room_id': test_room_id}
            
            print(f"🔄 Uploading PDF to room: {test_room_id}")
            upload_response = requests.post(
                f"{base_url}/upload-pdf",
                files=files,
                data=data,
                timeout=15
            )
            
        print(f"📊 Upload response status: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            print("✅ PDF upload successful!")
            print(f"   📄 Metadata: {upload_result.get('metadata', {})}")
            print(f"   🎯 Stored for room: {upload_result.get('room_id')}")
        else:
            print(f"❌ PDF upload failed: {upload_response.status_code}")
            print(f"   Response: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False
    print("")
    
    # Step 4: Verify context storage
    print("📋 STEP 4: Verify PDF context storage")
    print("-" * 30)
    try:
        context_response = requests.get(
            f"{base_url}/get-pdf-context/{test_room_id}",
            timeout=5
        )
        
        print(f"📊 Context response status: {context_response.status_code}")
        
        if context_response.status_code == 200:
            context_result = context_response.json()
            print("✅ Context retrieval successful!")
            print(f"   📊 Has context: {context_result.get('has_context')}")
            print(f"   📝 Context length: {len(context_result.get('context', ''))}")
            print(f"   📄 Metadata: {context_result.get('metadata', {})}")
            
            if context_result.get('has_context'):
                context_preview = context_result.get('context', '')[:300]
                print(f"\n📖 Context preview (first 300 chars):")
                print("-" * 50)
                print(context_preview + "..." if len(context_preview) == 300 else context_preview)
                print("-" * 50)
            else:
                print("❌ No context found after upload - this is a problem!")
                return False
        else:
            print(f"❌ Context retrieval failed: {context_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Context retrieval error: {e}")
        return False
    print("")
    
    # Step 5: Simulate agent context fetch
    print("📋 STEP 5: Simulate agent context fetch")
    print("-" * 30)
    try:
        # This simulates what the agent does in agent.py
        agent_response = requests.get(f"{base_url}/get-pdf-context/{test_room_id}", timeout=5)
        
        print(f"📊 Agent fetch status: {agent_response.status_code}")
        
        if agent_response.status_code == 200:
            agent_context_data = agent_response.json()
            if agent_context_data.get("has_context"):
                pdf_context = agent_context_data.get("context", "")
                print(f"✅ Agent successfully fetched PDF context")
                print(f"   📝 Context length: {len(pdf_context)} characters")
                print(f"   🧠 Agent would include this in welcome message")
                
                # Simulate what agent would do with the context
                welcome_message = "Welcome to LEVRA! I'm your AI career coach."
                combined_message = f"{pdf_context}\n\n{welcome_message}"
                print(f"   💬 Combined message length: {len(combined_message)} characters")
                
            else:
                print(f"❌ Agent found no PDF context for room {test_room_id}")
                return False
        else:
            print(f"❌ Agent failed to fetch PDF context: {agent_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent context fetch error: {e}")
        return False
    print("")
    
    # Step 6: Test with different room ID (negative test)
    print("📋 STEP 6: Test with non-existent room ID")
    print("-" * 30)
    try:
        fake_room_id = "room-nonexistent"
        fake_response = requests.get(f"{base_url}/get-pdf-context/{fake_room_id}", timeout=5)
        
        if fake_response.status_code == 200:
            fake_result = fake_response.json()
            if not fake_result.get('has_context'):
                print(f"✅ Correctly returns no context for non-existent room")
                print(f"   📊 Response: {fake_result}")
            else:
                print(f"❌ Unexpectedly found context for non-existent room")
                return False
        else:
            print(f"❌ Unexpected status for non-existent room: {fake_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing non-existent room: {e}")
        return False
    print("")
    
    # Summary
    print("📋 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print("✅ All tests passed! PDF integration is working correctly.")
    print("")
    print("🔧 VERIFIED COMPONENTS:")
    print("✅ Flask server is running and accessible")
    print("✅ PDF upload endpoint accepts and processes files")
    print("✅ PDF processing extracts text successfully")
    print("✅ PDF context is stored with correct room ID")
    print("✅ Context retrieval endpoint returns stored data")
    print("✅ Agent can fetch PDF context using room ID")
    print("✅ Non-existent rooms correctly return no context")
    print("")
    print("🎯 READY FOR TESTING:")
    print("1. Start the frontend: npm run dev")
    print("2. Upload a PDF through the UI")
    print("3. Start the LiveKit agent")
    print("4. Verify PDF context appears in conversation")
    print("")
    return True

if __name__ == "__main__":
    success = test_complete_pdf_integration()
    
    if not success:
        print("\n❌ INTEGRATION TEST FAILED")
        print("Check the error messages above and fix the issues.")
        exit(1)
    else:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        exit(0)
