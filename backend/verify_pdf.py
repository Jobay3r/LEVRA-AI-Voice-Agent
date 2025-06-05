#!/usr/bin/env python3
"""
Simple verification script to check if PDF processing works
without requiring external libraries
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_pdf_processor():
    """Test the PDF processor directly"""
    
    pdf_path = "Hackathon -  LEVRA Deck.pdf"
    
    print("🧪 LEVRA PDF Processing Test")
    print("=" * 40)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return False
    
    file_size = os.path.getsize(pdf_path)
    print(f"📄 PDF File: {pdf_path}")
    print(f"📊 File Size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    
    # Test if we can import the PDF processor
    try:
        from pdf_processor import pdf_processor
        print("✅ PDF processor module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PDF processor: {e}")
        return False
    
    # Test PDF processing
    try:
        print("\n🔍 Testing PDF text extraction...")
        
        # Simulate a file object
        class MockFile:
            def __init__(self, file_path):
                self.filename = os.path.basename(file_path)
                self.content_length = os.path.getsize(file_path)
                self._file_path = file_path
                
            def read(self):
                with open(self._file_path, 'rb') as f:
                    return f.read()
        
        mock_file = MockFile(pdf_path)
        result = pdf_processor.extract_text_from_pdf(mock_file)
        
        if result["success"]:
            print("✅ PDF processing successful!")
            print(f"   📄 Pages: {result['metadata'].get('num_pages', 'Unknown')}")
            print(f"   📝 Text Length: {len(result['text'])} characters")
            print(f"   📋 Filename: {result['metadata'].get('filename', 'Unknown')}")
            
            # Test context creation
            context = pdf_processor.create_context_prompt(result["text"], result["metadata"])
            print(f"   🧠 Context Length: {len(context)} characters")
            
            # Show preview
            print(f"\n📖 Text Preview (first 300 characters):")
            print("-" * 50)
            print(result["text"][:300] + "..." if len(result["text"]) > 300 else result["text"])
            print("-" * 50)
            
            return True
        else:
            print(f"❌ PDF processing failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Error during PDF processing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_processor()
    
    if success:
        print("\n🎉 PDF processing test passed!")
        print("\n📝 Next steps:")
        print("1. Test upload via frontend at http://localhost:5174")
        print("2. Upload the PDF file through the drag-and-drop interface")
        print("3. Start a voice conversation to test AI context integration")
    else:
        print("\n❌ PDF processing test failed!")
        print("Check the error messages above for troubleshooting.")
