#!/usr/bin/env python3
"""
Test script to verify PDF upload functionality
"""

import requests
import os
import json

def test_pdf_upload():
    """Test uploading the LEVRA Deck PDF"""
    
    # File path
    pdf_path = "Hackathon -  LEVRA Deck.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return False
    
    print(f"📄 Testing PDF upload: {pdf_path}")
    print(f"📊 File size: {os.path.getsize(pdf_path)} bytes")
    
    # Upload URL
    upload_url = "http://localhost:5001/upload-pdf"
    
    try:
        # Prepare form data
        with open(pdf_path, 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'room_id': 'test-room'}
            
            print("🚀 Uploading PDF...")
            response = requests.post(upload_url, files=files, data=data, timeout=30)
            
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"   Metadata: {json.dumps(result.get('metadata', {}), indent=2)}")
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def test_context_retrieval():
    """Test retrieving the uploaded PDF context"""
    
    context_url = "http://localhost:5001/get-pdf-context/test-room"
    
    try:
        print("\n🔍 Testing context retrieval...")
        response = requests.get(context_url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            has_context = result.get('has_context', False)
            context = result.get('context', '')
            metadata = result.get('metadata', {})
            
            print(f"📋 Has Context: {has_context}")
            if has_context:
                print(f"📊 Context Length: {len(context)} characters")
                print(f"📄 Metadata: {json.dumps(metadata, indent=2)}")
                print(f"📝 Context Preview (first 500 chars):")
                print("-" * 50)
                print(context[:500] + "..." if len(context) > 500 else context)
                print("-" * 50)
                return True
            else:
                print("❌ No context found")
                return False
        else:
            print(f"❌ Context retrieval failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error retrieving context: {e}")
        return False

if __name__ == "__main__":
    print("🧪 LEVRA PDF Upload Test")
    print("=" * 40)
    
    # Test 1: Upload PDF
    upload_success = test_pdf_upload()
    
    # Test 2: Retrieve context (only if upload succeeded)
    if upload_success:
        context_success = test_context_retrieval()
        
        if context_success:
            print("\n🎉 All tests passed! PDF upload functionality is working correctly.")
        else:
            print("\n⚠️  Upload succeeded but context retrieval failed.")
    else:
        print("\n❌ Upload test failed. Check server logs for details.")
