#!/usr/bin/env python3
"""
Test PDF upload and context retrieval integration
"""

import requests
import os

def test_pdf_upload_and_retrieval():
    """Test the complete PDF upload and context retrieval flow"""
    
    pdf_path = "Hackathon -  LEVRA Deck.pdf"
    test_room_id = "test-integration-room"
    base_url = "http://localhost:5001"
    
    print("🧪 Testing PDF Upload and Context Retrieval Integration")
    print("=" * 60)
    
    # Step 1: Check if PDF file exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    print(f"📄 PDF file found: {pdf_path}")
    
    # Step 2: Upload PDF
    print(f"\n🔄 Uploading PDF to room: {test_room_id}")
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'room_id': test_room_id}
            
            upload_response = requests.post(
                f"{base_url}/upload-pdf",
                files=files,
                data=data,
                timeout=10
            )
            
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            print("✅ PDF upload successful!")
            print(f"   📊 Metadata: {upload_result.get('metadata', {})}")
        else:
            print(f"❌ PDF upload failed: {upload_response.status_code}")
            print(f"   Response: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False
    
    # Step 3: Retrieve context
    print(f"\n🔄 Retrieving context for room: {test_room_id}")
    try:
        context_response = requests.get(
            f"{base_url}/get-pdf-context/{test_room_id}",
            timeout=5
        )
        
        if context_response.status_code == 200:
            context_result = context_response.json()
            print("✅ Context retrieval successful!")
            print(f"   📊 Has context: {context_result.get('has_context')}")
            print(f"   📝 Context length: {len(context_result.get('context', ''))}")
            
            if context_result.get('has_context'):
                context_preview = context_result.get('context', '')[:200]
                print(f"\n📖 Context preview:")
                print("-" * 40)
                print(context_preview + "..." if len(context_preview) == 200 else context_preview)
                print("-" * 40)
                return True
            else:
                print("❌ No context found after upload")
                return False
        else:
            print(f"❌ Context retrieval failed: {context_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Context retrieval error: {e}")
        return False

def test_agent_context_fetch():
    """Test the agent's ability to fetch context (simulating what agent.py does)"""
    
    test_room_id = "test-integration-room"
    
    print(f"\n🤖 Testing Agent Context Fetch for room: {test_room_id}")
    print("-" * 50)
    
    try:
        # This simulates what the agent does in agent.py
        response = requests.get(f"http://localhost:5001/get-pdf-context/{test_room_id}", timeout=5)
        
        if response.status_code == 200:
            context_data = response.json()
            if context_data.get("has_context"):
                pdf_context = context_data.get("context", "")
                print(f"✅ Agent successfully fetched PDF context")
                print(f"   📝 Context length: {len(pdf_context)} characters")
                print(f"   🧠 Agent would include this in welcome message")
                return True
            else:
                print(f"❌ Agent found no PDF context for room {test_room_id}")
                return False
        else:
            print(f"❌ Agent failed to fetch PDF context: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent context fetch error: {e}")
        return False

if __name__ == "__main__":
    # Test upload and retrieval
    upload_success = test_pdf_upload_and_retrieval()
    
    if upload_success:
        # Test agent simulation
        agent_success = test_agent_context_fetch()
        
        if agent_success:
            print("\n🎉 All tests passed! PDF integration is working correctly.")
            print("\n📋 What this means:")
            print("✅ PDF upload endpoint works")
            print("✅ PDF processing and storage works") 
            print("✅ Context retrieval endpoint works")
            print("✅ Agent can fetch PDF context")
            print("\n🔧 Next steps:")
            print("1. Test with frontend UI")
            print("2. Start LiveKit agent and test full flow")
        else:
            print("\n❌ Agent context fetch failed")
    else:
        print("\n❌ PDF upload/retrieval failed")
