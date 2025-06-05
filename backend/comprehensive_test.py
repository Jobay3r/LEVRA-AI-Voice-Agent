#!/usr/bin/env python3
"""
Comprehensive PDF Integration Test for LEVRA Voice Assistant
Tests all components: PDF processing, server endpoints, prompts, and agent integration
"""

print('=== COMPREHENSIVE PDF INTEGRATION TEST ===')

# Test 1: PDF processor functionality       
print('\n1. Testing PDF processor...')
try:
    from pdf_processor import PDFProcessor  
    processor = PDFProcessor()

    with open('Hackathon -  LEVRA Deck.pdf', 'rb') as f:
        text = processor.extract_text(f)

    print(f'✅ PDF text extraction successful: {len(text)} characters')
    print(f'First 150 chars: {text[:150]}...')
except Exception as e:
    print(f'❌ PDF processor error: {e}')     

# Test 2: Server endpoints (if running)     
print('\n2. Testing server endpoints...')
try:
    import requests

    # Test PDF upload
    with open('Hackathon -  LEVRA Deck.pdf', 'rb') as f:
        files = {'file': f}
        data = {'room_id': 'test_integration_123'}
        response = requests.post('http://localhost:3001/upload-pdf', files=files, data=data, timeout=5)

    print(f'Upload response: {response.status_code} - {response.text[:100]}...')

    # Test context retrieval
    context_response = requests.get('http://localhost:3001/get-pdf-context/test_integration_123', timeout=5)
    print(f'Context response: {context_response.status_code}')

    if context_response.status_code == 200:
        context_data = context_response.json()
        print(f'✅ Context length: {len(context_data.get("context", ""))} characters')
    else:
        print(f'❌ Context retrieval failed: {context_response.text}')

except requests.exceptions.ConnectionError: 
    print('⚠️ Server not running - endpoints not tested')
except Exception as e:
    print(f'❌ Server test error: {e}')

# Test 3: Prompts integration
print('\n3. Testing prompts integration...')
try:
    from prompts import INSTRUCTIONS, WELCOME_WITH_CONTEXT, DOCUMENT_CONTEXT_HANDLER       
    
    print(f'✅ INSTRUCTIONS loaded: {len(INSTRUCTIONS)} characters')
    print(f'✅ WELCOME_WITH_CONTEXT loaded: {len(WELCOME_WITH_CONTEXT)} characters')
    print(f'✅ DOCUMENT_CONTEXT_HANDLER loaded: {len(DOCUMENT_CONTEXT_HANDLER)} characters')

    # Check for document context integration
    if 'DOCUMENT CONTEXT INTEGRATION' in INSTRUCTIONS:
        print('✅ Document context integration found in INSTRUCTIONS')
    else:
        print('❌ Document context integration NOT found in INSTRUCTIONS')

except Exception as e:
    print(f'❌ Prompts integration error: {e}')

# Test 4: Agent imports
print('\n4. Testing agent integration...')  
try:
    from agent import VoiceAssistant        
    print('✅ VoiceAssistant class imported successfully')

    # Check if requests is imported in agent
    import agent
    import inspect
    
    # Look for PDF context fetching in agent code
    agent_source = inspect.getsource(agent)
    if 'get-pdf-context' in agent_source:
        print('✅ PDF context fetching code found in agent')
    else:
        print('❌ PDF context fetching code NOT found in agent')

    if 'WELCOME_WITH_CONTEXT' in agent_source:
        print('✅ Context-aware welcome message integration found')
    else:
        print('❌ Context-aware welcome message integration NOT found')

except Exception as e:
    print(f'❌ Agent integration error: {e}') 

# Test 5: End-to-end simulation
print('\n5. Testing end-to-end flow simulation...')
try:
    # Simulate agent fetching PDF context
    room_id = 'test_integration_123'
    
    # If server is running, simulate the agent's PDF context fetch
    try:
        import requests
        response = requests.get(f'http://localhost:3001/get-pdf-context/{room_id}', timeout=5)
        if response.status_code == 200:
            context_data = response.json()
            pdf_context = context_data.get('context', '')
            
            # Simulate welcome message generation
            from prompts import WELCOME_WITH_CONTEXT
            if pdf_context:
                welcome_content = f"{pdf_context}\n\n{WELCOME_WITH_CONTEXT}"
                print(f'✅ End-to-end simulation successful')
                print(f'Generated welcome message length: {len(welcome_content)} characters')
                print(f'Context included: {len(pdf_context)} chars, Welcome: {len(WELCOME_WITH_CONTEXT)} chars')
            else:
                print('⚠️ No PDF context retrieved for simulation')
        else:
            print('⚠️ Could not retrieve context for simulation')
    except:
        print('⚠️ Server not available for end-to-end simulation')

except Exception as e:
    print(f'❌ End-to-end simulation error: {e}')

print('\n=== INTEGRATION TEST COMPLETE ===')
print('\nSUMMARY:')
print('- PDF processing: Core functionality for text extraction')
print('- Server endpoints: PDF upload and context retrieval APIs') 
print('- Prompts integration: Context-aware instructions and welcome messages')
print('- Agent integration: PDF context fetching and welcome message generation')
print('- End-to-end flow: Complete user journey simulation')
print('\nIf all tests pass, the PDF upload feature is ready for voice testing! 🚀')
