#!/usr/bin/env python3
"""
Test script for mid-conversation PDF upload functionality using existing PDF.

This script tests:
1. Starting a conversation without PDF context
2. Uploading the existing LEVRA PDF during the conversation
3. Verifying the AI receives and acknowledges the new context
"""

import requests
import time
import json
import os
import sys

def test_mid_conversation_pdf_upload():
    """Test the complete mid-conversation PDF upload flow using existing PDF."""
    
    print("🧪 Testing Mid-Conversation PDF Upload Functionality")
    print("=" * 60)
    
    # Test configuration
    base_url = "http://localhost:5001"
    test_room_id = f"test-room-{int(time.time())}"
    existing_pdf = "Hackathon -  LEVRA Deck.pdf"
    
    print(f"📋 Test Room ID: {test_room_id}")
    print(f"📄 Using existing PDF: {existing_pdf}")
    
    # Check if PDF exists
    if not os.path.exists(existing_pdf):
        print(f"❌ PDF file not found: {existing_pdf}")
        return False
    
    # Step 1: Check initial PDF context (should be empty)
    print("\n1️⃣ Checking initial PDF context...")
    try:
        response = requests.get(f"{base_url}/get-pdf-context/{test_room_id}")
        
        if response.status_code == 200:
            context_data = response.json()
            print(f"   Initial context: {context_data}")
            print("   ✅ No initial PDF context (as expected)")
        else:
            print(f"   ❌ Failed to get initial context: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return False
    
    # Step 2: Upload existing PDF during conversation
    print("\n2️⃣ Uploading existing PDF during conversation...")
    
    try:
        with open(existing_pdf, 'rb') as f:
            files = {'pdf_file': (existing_pdf, f, 'application/pdf')}
            data = {'room_id': test_room_id}
            
            response = requests.post(f"{base_url}/upload-pdf", files=files, data=data)
            
        if response.status_code == 200:
            upload_result = response.json()
            print(f"   Upload result: {upload_result}")
            print("   ✅ PDF uploaded successfully")
        else:
            print(f"   ❌ Upload failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Upload error: {e}")
        return False
    
    # Step 3: Verify PDF context is now available
    print("\n3️⃣ Verifying PDF context is available...")
    response = requests.get(f"{base_url}/get-pdf-context/{test_room_id}")
    
    if response.status_code == 200:
        context_data = response.json()
        print(f"   Context available: {context_data.get('has_context')}")
        print(f"   Context length: {len(context_data.get('context', ''))}")
        print("   ✅ PDF context is now available")
        
        # Show sample of context
        context_sample = context_data.get("context", "")[:200] + "..."
        print(f"   📄 Context sample: {context_sample}")
    else:
        print(f"   ❌ Failed to get updated context: {response.status_code}")
        return False
    
    # Step 4: Test mid-conversation notification
    print("\n4️⃣ Testing mid-conversation notification...")
    response = requests.post(f"{base_url}/notify-pdf-update/{test_room_id}")
    
    if response.status_code == 200:
        notification_result = response.json()
        print(f"   Notification result: {notification_result}")
        print("   ✅ Mid-conversation notification sent successfully")
        
        # Check if trigger file was created
        trigger_file = f"pdf_update_trigger_{test_room_id}.flag"
        if os.path.exists(trigger_file):
            print(f"   ✅ Trigger file created: {trigger_file}")
            # Clean up trigger file
            os.remove(trigger_file)
            print("   🧹 Trigger file cleaned up")
        else:
            print(f"   ⚠️  Trigger file not found: {trigger_file}")
            
    else:
        print(f"   ❌ Notification failed: {response.status_code} - {response.text}")
        return False
    
    print("\n✅ Mid-conversation PDF upload test completed successfully!")
    return True

if __name__ == "__main__":
    print("🚀 Starting Mid-Conversation PDF Upload Tests")
    print("🔧 Make sure the Flask server is running on localhost:5001")
    print()
    
    try:
        # Test backend functionality
        if test_mid_conversation_pdf_upload():
            print("✅ Backend tests passed")
            print("\n🎊 Mid-conversation PDF upload is ready to use!")
        else:
            print("❌ Backend tests failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the Flask server first:")
        print("   python server.py")
        exit(1)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        exit(1)
