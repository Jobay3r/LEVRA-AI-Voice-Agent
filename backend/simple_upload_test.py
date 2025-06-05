#!/usr/bin/env python3
"""
Simple PDF upload test
"""

import requests
import os

def simple_upload_test():
    pdf_path = "Hackathon -  LEVRA Deck.pdf"
    test_room_id = "room-test123"
    
    print("🧪 Simple PDF Upload Test")
    print(f"📄 File: {pdf_path}")
    print(f"🎯 Room: {test_room_id}")
    
    if not os.path.exists(pdf_path):
        print("❌ PDF file not found")
        return
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'room_id': test_room_id}
            
            print("🔄 Uploading...")
            response = requests.post(
                "http://localhost:5001/upload-pdf",
                files=files,
                data=data,
                timeout=10
            )
            
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"Result: {result}")
        else:
            print(f"❌ Upload failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_upload_test()
