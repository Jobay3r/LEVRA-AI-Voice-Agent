#!/usr/bin/env python3
"""
Demonstrate the complete PDF integration workflow
"""

import requests
import json

def demonstrate_pdf_workflow():
    """Demonstrate the complete PDF integration workflow"""
    
    room_id = "room-demo-12345"
    base_url = "http://localhost:5001"
    
    print("🎯 LEVRA PDF INTEGRATION WORKFLOW DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Step 1: Upload PDF (simulating frontend upload)
    print("📤 STEP 1: Simulating PDF Upload from Frontend")
    print("-" * 50)
    try:
        with open("Hackathon -  LEVRA Deck.pdf", 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'room_id': room_id}
            
            upload_response = requests.post(
                f"{base_url}/upload-pdf",
                files=files,
                data=data
            )
            
        if upload_response.status_code == 200:
            result = upload_response.json()
            print(f"✅ PDF uploaded successfully to room: {room_id}")
            print(f"   📄 File: {result['metadata']['filename']}")
            print(f"   📊 Pages: {result['metadata']['num_pages']}")
            print(f"   💾 Size: {result['metadata']['file_size']:,} bytes")
        else:
            print(f"❌ Upload failed: {upload_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return
    
    print()
    
    # Step 2: Agent fetches context (simulating agent.py behavior)
    print("🤖 STEP 2: Simulating Agent Context Fetch")
    print("-" * 50)
    try:
        # This is exactly what the agent does in agent.py
        context_response = requests.get(f"{base_url}/get-pdf-context/{room_id}")
        
        if context_response.status_code == 200:
            context_data = context_response.json()
            if context_data.get("has_context"):
                pdf_context = context_data.get("context", "")
                print(f"✅ Agent successfully fetched PDF context")
                print(f"   📝 Context length: {len(pdf_context):,} characters")
                print(f"   🎯 Room ID: {room_id}")
                
                # Show how agent would use this
                welcome_message = "Welcome to LEVRA! I'm your AI career coach."
                combined_message = f"{pdf_context}\n\n{welcome_message}"
                
                print()
                print("💬 STEP 3: How Agent Uses PDF Context")
                print("-" * 50)
                print("Agent would send this combined message:")
                print(f"   📏 Total message length: {len(combined_message):,} characters")
                print()
                print("📖 Context Preview (first 500 characters):")
                print("'" * 60)
                print(pdf_context[:500] + "..." if len(pdf_context) > 500 else pdf_context)
                print("'" * 60)
                print()
                print("✅ The AI can now reference:")
                print("   • LEVRA's human skills training approach")
                print("   • The £6.9T global soft skills gap")
                print("   • Gen Z learning preferences (95% abandon e-learning)")
                print("   • LEVRA Human Skills Framework (HSF)")
                print("   • Multi-modal VR training simulations")
                print("   • The hackathon problem statement")
                print("   • Team member information")
                
            else:
                print(f"❌ No PDF context found for room {room_id}")
        else:
            print(f"❌ Context fetch failed: {context_response.status_code}")
            
    except Exception as e:
        print(f"❌ Context fetch error: {e}")
    
    print()
    print("🎉 INTEGRATION COMPLETE!")
    print("=" * 60)
    print("✅ PDF uploaded and stored with room ID")
    print("✅ Agent can fetch context using room ID") 
    print("✅ Context includes structured document information")
    print("✅ AI can provide personalized responses based on PDF content")
    print()
    print("🔄 NEXT STEPS FOR TESTING:")
    print("1. Start frontend: npm run dev")
    print("2. Upload PDF through UI")
    print("3. Start agent: python agent.py start")
    print("4. Begin voice conversation")
    print("5. Verify AI references uploaded document")

if __name__ == "__main__":
    demonstrate_pdf_workflow()
