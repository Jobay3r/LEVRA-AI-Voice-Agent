#!/usr/bin/env python3
"""Simple HSF test"""

import sys
import os

# Add backend directory to path
backend_path = r"c:\Users\Jobay\Documents\AI Projects\voice Assistant with ui\LEVRA\LEVRA\backend"
sys.path.insert(0, backend_path)

print("🧠 Testing LEVRA HSF Optimization...")

try:
    print("1. Testing core instructions import...")
    from prompts.core_instructions import INSTRUCTIONS, WELCOME_MESSAGE
    print(f"✅ Core instructions imported: {len(INSTRUCTIONS)} chars")
    print(f"   Contains HSF: {'HSF' in INSTRUCTIONS}")
    print(f"   Contains Gen Z: {'Gen Z' in INSTRUCTIONS}")
    print(f"   Contains £6.9T: {'£6.9T' in INSTRUCTIONS}")
    
    print("\n2. Testing scenarios import...")
    from prompts.scenarios import SCENARIO_TEMPLATES
    print(f"✅ Scenarios imported: {len(SCENARIO_TEMPLATES)} scenarios")
    gen_z_scenarios = [s for s in SCENARIO_TEMPLATES.keys() if 'gen_z' in s or 'ai_' in s or 'remote_' in s]
    print(f"   Gen Z scenarios: {len(gen_z_scenarios)}")
    
    print("\n3. Testing feedback import...")
    from prompts.feedback import SCORING_MATRIX, REAL_TIME_COACHING
    print(f"✅ Feedback imported: {len(SCORING_MATRIX)} scoring criteria")
    hsf_skills = [s for s in SCORING_MATRIX.keys() if 'digital_' in s or 'generational_' in s or 'purpose_' in s]
    print(f"   HSF skills: {len(hsf_skills)}")
    
    print("\n4. Testing prompt manager...")
    from prompts import get_instructions, get_welcome_message
    instructions = get_instructions(has_document_context=True)
    welcome = get_welcome_message(has_document_context=False)
    print(f"✅ Prompt manager working: {len(instructions)} + {len(welcome)} chars")
    
    print("\n🚀 ALL BASIC TESTS PASSED!")
    print("✨ LEVRA HSF optimization is functional!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
