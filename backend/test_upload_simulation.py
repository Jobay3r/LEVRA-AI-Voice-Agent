#!/usr/bin/env python3
"""
Simple API test for PDF upload without external dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_processor import pdf_processor

def test_upload_simulation():
    """Simulate the upload process locally"""
    
    pdf_path = "Hackathon -  LEVRA Deck.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    print("🧪 Simulating PDF upload process...")
    print(f"📄 File: {pdf_path}")
    
    try:
        # Simulate file upload by reading the file
        with open(pdf_path, 'rb') as pdf_file:
            # Create a mock file object
            class MockFile:
                def __init__(self, file_data, filename):
                    self.data = file_data
                    self.filename = filename
                    self.content_length = len(file_data)
                
                def read(self):
                    return self.data
            
            file_data = pdf_file.read()
            mock_file = MockFile(file_data, pdf_path)
            
            print("🔄 Processing PDF...")
            result = pdf_processor.extract_text_from_pdf(mock_file)
            
            if result["success"]:
                print("✅ PDF processing successful!")
                print(f"   📄 Pages: {result['metadata']['num_pages']}")
                print(f"   📝 Text Length: {len(result['text'])} characters")
                
                # Create context prompt
                context = pdf_processor.create_context_prompt(
                    result["text"], 
                    result["metadata"]
                )
                
                print(f"   🧠 Context Length: {len(context)} characters")
                print("\n📖 Context Preview (first 400 chars):")
                print("-" * 50)
                print(context[:400] + "..." if len(context) > 400 else context)
                print("-" * 50)
                
                # Simulate storing in the global context (like the real upload would do)
                print("\n💾 Context would be stored for room 'test-room'")
                return True
            else:
                print(f"❌ PDF processing failed: {result['error']}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 PDF Upload Simulation Test")
    print("=" * 40)
    success = test_upload_simulation()
    
    if success:
        print("\n🎉 Simulation successful! The PDF upload process works correctly.")
        print("\n📋 Next steps:")
        print("1. Try uploading via frontend at http://localhost:5174")
        print("2. Check browser console for any errors")
        print("3. Monitor Flask server logs for upload requests")
    else:
        print("\n❌ Simulation failed. Check the error messages above.")
