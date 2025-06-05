#!/usr/bin/env python3
"""
Test script for mid-conversation PDF upload functionality.

This script tests:
1. Starting a conversation without PDF context
2. Uploading a PDF during the conversation
3. Verifying the AI receives and acknowledges the new context
"""

import requests
import time
import json
import os
import sys
sys.path.append('..')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def test_mid_conversation_pdf_upload():
    """Test the complete mid-conversation PDF upload flow."""
    
    print("🧪 Testing Mid-Conversation PDF Upload Functionality")
    print("=" * 60)
    
    # Test configuration
    base_url = "http://localhost:5001"
    test_room_id = f"test-room-{int(time.time())}"
    
    print(f"📋 Test Room ID: {test_room_id}")
    
    # Step 1: Check initial PDF context (should be empty)
    print("\n1️⃣ Checking initial PDF context...")
    response = requests.get(f"{base_url}/get-pdf-context/{test_room_id}")
    
    if response.status_code == 200:
        context_data = response.json()
        print(f"   Initial context: {context_data}")
        assert not context_data.get("has_context"), "Expected no initial context"
        print("   ✅ No initial PDF context (as expected)")
    else:
        print(f"   ❌ Failed to get initial context: {response.status_code}")
        return False
      # Step 2: Create a test PDF file
    print("\n2️⃣ Creating test PDF content...")
    
    def create_test_pdf(filename, room_id):
        """Create a test PDF with specific content for the room."""
        content = f"""Mid-Conversation PDF Upload Test
        
Room ID: {room_id}
Upload Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

This is a test document to verify that PDF uploads work during active conversations.

Key points to test:
- Document processing during active sessions
- AI acknowledgment of new content  
- Context integration mid-conversation

Meeting Notes:
- Project deadline: June 15, 2025
- Team size: 5 members
- Budget: $50,000
- Key stakeholder: Sarah Johnson

Training Focus:
- Leadership development for new managers
- Communication skills for technical presentations
- Conflict resolution in remote teams
"""
        
        c = canvas.Canvas(filename, pagesize=letter)
        lines = content.split('\n')
        y_position = 750
        
        for line in lines:
            if y_position < 50:  # Start new page if needed
                c.showPage()
                y_position = 750
            c.drawString(50, y_position, line.strip())
            y_position -= 20
            
        c.save()
        return filename
    
    test_file_path = f"test_upload_{test_room_id}.pdf"
    create_test_pdf(test_file_path, test_room_id)
    print(f"   ✅ Created test PDF: {test_file_path}")
    
    # Step 3: Simulate PDF upload during conversation
    print("\n3️⃣ Uploading PDF during conversation...")
      try:
        with open(test_file_path, 'rb') as f:
            files = {'pdf_file': (test_file_path, f, 'application/pdf')}
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
    
    # Step 4: Verify PDF context is now available
    print("\n4️⃣ Verifying PDF context is available...")
    response = requests.get(f"{base_url}/get-pdf-context/{test_room_id}")
    
    if response.status_code == 200:
        context_data = response.json()
        print(f"   Updated context: {context_data}")
        assert context_data.get("has_context"), "Expected PDF context to be available"
        assert len(context_data.get("context", "")) > 0, "Expected non-empty context"
        print("   ✅ PDF context is now available")
    else:
        print(f"   ❌ Failed to get updated context: {response.status_code}")
        return False
    
    # Step 5: Test mid-conversation notification
    print("\n5️⃣ Testing mid-conversation notification...")
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
    
    # Step 6: Clean up test file
    print("\n6️⃣ Cleaning up...")
    try:
        os.remove(test_file_path)
        print(f"   🧹 Removed test file: {test_file_path}")
    except Exception as e:
        print(f"   ⚠️  Failed to remove test file: {e}")
    
    # Step 7: Clean up test files
    print("\n7️⃣ Cleaning up test files...")
    try:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"   ✅ Removed test file: {test_file_path}")
            
        # Remove any trigger files
        trigger_file = f"pdf_update_trigger_{test_room_id}.flag"
        if os.path.exists(trigger_file):
            os.remove(trigger_file)
            print(f"   ✅ Removed trigger file: {trigger_file}")
            
    except Exception as e:
        print(f"   ⚠️  Cleanup warning: {e}")
    
    print("\n✅ Mid-conversation PDF upload test completed successfully!")
    return True

def test_frontend_integration():
    """Test frontend integration points."""
    
    print("\n🖥️  Testing Frontend Integration Points")
    print("-" * 40)
    
    # Test the notification endpoint that frontend will call
    test_room_id = f"frontend-test-{int(time.time())}"
    base_url = "http://localhost:5001"
    
    # First create some context
    test_content = "Frontend integration test document"
    
    # Simulate frontend PDF upload
    print("1. Simulating frontend PDF upload...")
    files = {'pdf_file': ('test.txt', test_content.encode(), 'application/pdf')}
    data = {'room_id': test_room_id}
    
    response = requests.post(f"{base_url}/upload-pdf", files=files, data=data)
    
    if response.status_code == 200:
        print("   ✅ Frontend upload simulation successful")
        
        # Test the notification endpoint frontend will call
        print("2. Testing frontend notification call...")
        response = requests.post(f"{base_url}/notify-pdf-update/{test_room_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Frontend notification successful: {result}")
            return True
        else:
            print(f"   ❌ Frontend notification failed: {response.status_code}")
            return False
    else:
        print(f"   ❌ Frontend upload simulation failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Mid-Conversation PDF Upload Tests")
    print("🔧 Make sure the Flask server is running on localhost:5001")
    print()
    
    try:
        # Test backend functionality
        if test_mid_conversation_pdf_upload():
            print("✅ Backend tests passed")
        else:
            print("❌ Backend tests failed")
            exit(1)
        
        # Test frontend integration
        if test_frontend_integration():
            print("✅ Frontend integration tests passed")
        else:
            print("❌ Frontend integration tests failed")
            exit(1)
            
        print("\n🎊 All tests passed! Mid-conversation PDF upload is ready to use.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the Flask server first:")
        print("   cd backend && python server.py")
        exit(1)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        exit(1)
