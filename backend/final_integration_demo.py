#!/usr/bin/env python3
"""
Final test demonstrating how the updated AI will handle PDF context and document questions
"""

import requests
from prompts import INSTRUCTIONS, WELCOME_MESSAGE, WELCOME_WITH_CONTEXT

def demonstrate_ai_document_integration():
    """Demonstrate how the AI will now handle document context and questions"""
    
    print("🎯 AI DOCUMENT INTEGRATION DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Test setup
    room_id = "room-final-demo"
    
    print("📤 STEP 1: Upload PDF Document")
    print("-" * 40)
    try:
        with open("Hackathon -  LEVRA Deck.pdf", 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'room_id': room_id}
            
            response = requests.post(
                "http://localhost:5001/upload-pdf",
                files=files,
                data=data
            )
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ PDF uploaded successfully")
            print(f"   📄 File: {result['metadata']['filename']}")
            print(f"   📊 Pages: {result['metadata']['num_pages']}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print()
    
    print("🤖 STEP 2: Retrieve Context (What Agent Does)")
    print("-" * 40)
    try:
        context_response = requests.get(f"http://localhost:5001/get-pdf-context/{room_id}")
        
        if context_response.status_code == 200:
            context_data = context_response.json()
            if context_data.get("has_context"):
                pdf_context = context_data.get("context", "")
                print(f"✅ Agent fetched PDF context ({len(pdf_context)} characters)")
                
                # Show how the AI will now respond
                print()
                print("💬 STEP 3: AI Response Examples with Document Context")
                print("-" * 40)
                
                # Welcome message with context
                welcome_with_context = f"{pdf_context}\n\n{WELCOME_WITH_CONTEXT}"
                print("🎉 CONTEXT-AWARE WELCOME MESSAGE:")
                print(f"   📏 Total length: {len(welcome_with_context):,} characters")
                print()
                print("📖 AI Welcome Preview:")
                print("=" * 50)
                print(WELCOME_WITH_CONTEXT[:400] + "..." if len(WELCOME_WITH_CONTEXT) > 400 else WELCOME_WITH_CONTEXT)
                print("=" * 50)
                
                print()
                print("🔍 EXAMPLE DOCUMENT-BASED Q&A:")
                print("-" * 40)
                
                example_questions = [
                    "What is LEVRA?",
                    "Tell me about the human skills gap",
                    "What's the hackathon challenge about?",
                    "Who are the founders of LEVRA?",
                    "How does VR help with Gen Z learning?"
                ]
                
                print("Questions the AI can now answer from the PDF:")
                for i, question in enumerate(example_questions, 1):
                    print(f"   {i}. {question}")
                
                print()
                print("📋 AI CAPABILITIES WITH DOCUMENT CONTEXT:")
                print("✅ References specific details from uploaded PDF")
                print("✅ Answers questions about LEVRA, team, mission")
                print("✅ Creates scenarios based on the £6.9T skills gap")
                print("✅ Discusses Gen Z learning preferences from document")
                print("✅ Role-plays hackathon-related conversations")
                print("✅ Provides coaching aligned with LEVRA's approach")
                
            else:
                print("❌ No context available")
        else:
            print(f"❌ Failed to retrieve context: {context_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("🎯 WHAT'S CHANGED:")
    print("=" * 60)
    print("✅ INSTRUCTIONS updated with document context handling")
    print("✅ New WELCOME_WITH_CONTEXT for when PDF is uploaded")
    print("✅ Agent uses context-aware welcome messages")
    print("✅ AI explicitly instructed to reference document details")
    print("✅ Enhanced prompts for document-based questions")
    print()
    print("🚀 READY FOR TESTING:")
    print("1. Start frontend and upload the PDF")
    print("2. Start the agent with: python agent.py start")
    print("3. Ask questions like 'What is LEVRA?' or 'Tell me about the hackathon'")
    print("4. The AI will now provide detailed answers from the document!")

if __name__ == "__main__":
    demonstrate_ai_document_integration()
