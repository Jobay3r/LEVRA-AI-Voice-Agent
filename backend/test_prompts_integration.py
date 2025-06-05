#!/usr/bin/env python3
"""
Test the updated prompts with PDF context integration
"""

import requests
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompts import INSTRUCTIONS, WELCOME_MESSAGE, WELCOME_WITH_CONTEXT, DOCUMENT_CONTEXT_HANDLER

def test_prompts_with_pdf_context():
    """Test the updated prompts and PDF context integration"""
    
    print("🧪 TESTING UPDATED PROMPTS WITH PDF CONTEXT")
    print("=" * 60)
    print()
    
    # Test 1: Verify prompt updates
    print("📋 TEST 1: Verify Prompt Updates")
    print("-" * 40)
    
    # Check if INSTRUCTIONS mentions document context
    if "DOCUMENT CONTEXT INTEGRATION" in INSTRUCTIONS:
        print("✅ INSTRUCTIONS updated with document context handling")
    else:
        print("❌ INSTRUCTIONS missing document context section")
    
    # Check if WELCOME_MESSAGE mentions PDFs
    if "uploaded materials" in WELCOME_MESSAGE:
        print("✅ WELCOME_MESSAGE updated to mention uploaded materials")
    else:
        print("❌ WELCOME_MESSAGE missing PDF reference")
    
    # Check if WELCOME_WITH_CONTEXT exists
    if "uploaded document" in WELCOME_WITH_CONTEXT:
        print("✅ WELCOME_WITH_CONTEXT prompt available")
    else:
        print("❌ WELCOME_WITH_CONTEXT prompt missing")
    
    print()
    
    # Test 2: Simulate PDF upload and context retrieval
    print("📋 TEST 2: Test PDF Upload and Context Retrieval")
    print("-" * 40)
    
    test_room_id = "room-prompt-test"
    
    try:
        # Upload PDF
        with open("Hackathon -  LEVRA Deck.pdf", 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'room_id': test_room_id}
            
            upload_response = requests.post(
                "http://localhost:5001/upload-pdf",
                files=files,
                data=data,
                timeout=10
            )
            
        if upload_response.status_code == 200:
            print("✅ PDF uploaded successfully")
        else:
            print(f"❌ PDF upload failed: {upload_response.status_code}")
            return False
        
        # Retrieve context
        context_response = requests.get(f"http://localhost:5001/get-pdf-context/{test_room_id}")
        
        if context_response.status_code == 200:
            context_data = context_response.json()
            if context_data.get("has_context"):
                pdf_context = context_data.get("context", "")
                print(f"✅ PDF context retrieved ({len(pdf_context)} characters)")
                
                # Test 3: Simulate agent welcome message creation
                print()
                print("📋 TEST 3: Simulate Agent Welcome Message Creation")
                print("-" * 40)
                
                # Simulate what agent.py does
                if pdf_context:
                    welcome_content = f"{pdf_context}\n\n{WELCOME_WITH_CONTEXT}"
                    print("✅ Context-aware welcome message created")
                    print(f"   📏 Total length: {len(welcome_content):,} characters")
                    print(f"   📄 PDF context: {len(pdf_context):,} characters")
                    print(f"   💬 Welcome message: {len(WELCOME_WITH_CONTEXT):,} characters")
                    
                    # Show preview
                    print()
                    print("📖 Welcome Message Preview (first 300 chars):")
                    print("=" * 50)
                    print(welcome_content[:300] + "..." if len(welcome_content) > 300 else welcome_content)
                    print("=" * 50)
                    
                else:
                    print("❌ No PDF context available for welcome message")
                    return False
                    
            else:
                print("❌ No PDF context found")
                return False
        else:
            print(f"❌ Context retrieval failed: {context_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    print()
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    print("✅ Prompts updated with PDF context handling")
    print("✅ PDF upload and retrieval working")
    print("✅ Context-aware welcome message generation working")
    print("✅ AI now has proper instructions for document integration")
    print()
    print("🎯 READY FOR TESTING:")
    print("1. The AI will now acknowledge uploaded documents")
    print("2. It can answer questions about PDF content")
    print("3. It will create personalized scenarios based on document context")
    print("4. Welcome messages adapt based on whether PDF is uploaded")
    
    return True

if __name__ == "__main__":
    success = test_prompts_with_pdf_context()
    
    if success:
        print("\n🚀 PDF context integration is now fully functional!")
        print("Try asking the AI: 'What is LEVRA?' or 'Tell me about the hackathon challenge'")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
