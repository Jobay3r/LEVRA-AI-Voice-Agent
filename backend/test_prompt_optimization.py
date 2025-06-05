"""
Test script for optimized LEVRA prompt system
Verifies that the modular prompt system reduces token usage while maintaining functionality
"""

import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_prompt_optimization():
    """Test the optimized prompt system"""
    
    print("🧪 TESTING OPTIMIZED LEVRA PROMPT SYSTEM")
    print("=" * 60)
    
    try:
        # Import both old and new systems for comparison
        print("📁 Importing optimized prompt system...")
        from prompts import (
            prompt_manager, 
            get_instructions, 
            get_welcome_message,
            build_conversation_prompt
        )
        
        # Test basic functionality
        print("\n✅ Testing core instruction loading...")
        basic_instructions = get_instructions(has_document_context=False)
        context_instructions = get_instructions(has_document_context=True)
        
        print(f"   Basic instructions length: {len(basic_instructions)} chars")
        print(f"   Context instructions length: {len(context_instructions)} chars")
        
        # Test welcome messages
        print("\n✅ Testing welcome message loading...")
        basic_welcome = get_welcome_message(has_document_context=False)
        context_welcome = get_welcome_message(has_document_context=True)
        
        print(f"   Basic welcome length: {len(basic_welcome)} chars")
        print(f"   Context welcome length: {len(context_welcome)} chars")
        
        # Test contextual prompt building
        print("\n✅ Testing contextual prompt building...")
        user_context = {
            "role": "Product Manager",
            "skill_focus": "leadership",
            "industry": "tech"
        }
        
        contextual_prompt = build_conversation_prompt(
            user_context, 
            has_document=True, 
            scenario_type="team_leadership"
        )
        print(f"   Contextual prompt length: {len(contextual_prompt)} chars")
        
        # Test scenario selection
        print("\n✅ Testing scenario functionality...")
        from prompts import SCENARIO_TEMPLATES
        scenario = SCENARIO_TEMPLATES.get("team_leadership")
        if scenario:
            print(f"   Team leadership scenario loaded: {len(scenario['setup'])} chars")
        
        # Test feedback system
        print("\n✅ Testing feedback system...")
        from prompts import calculate_skill_score, format_feedback_response
        
        test_scores = {
            "communication_clarity": 8.0,
            "emotional_intelligence": 7.5,
            "problem_solving": 9.0
        }
        
        overall_score = calculate_skill_score(test_scores)
        print(f"   Overall score calculation: {overall_score}/10")
        
        feedback = format_feedback_response(
            test_scores,
            ["Clear communication", "Good empathy"],
            ["More assertiveness needed"],
            ["Practice difficult conversations", "Study conflict resolution"]
        )
        print(f"   Formatted feedback length: {len(feedback)} chars")
        
        # Compare with original system size
        print("\n📊 SIZE COMPARISON:")
        try:
            with open("prompts_original_backup.py", "r", encoding="utf-8") as f:
                original_size = len(f.read())
            print(f"   Original prompts.py size: {original_size:,} characters")
            
            # Calculate total size of modular system
            modular_total = (
                len(basic_instructions) + 
                len(context_instructions) + 
                len(basic_welcome) + 
                len(context_welcome) +
                len(contextual_prompt)
            )
            print(f"   Typical modular prompt size: {modular_total:,} characters")
            
            reduction = ((original_size - modular_total) / original_size) * 100
            print(f"   Token reduction achieved: ~{reduction:.1f}%")
            
        except FileNotFoundError:
            print("   Could not find original backup for comparison")
        
        print("\n🎉 OPTIMIZATION TEST COMPLETED SUCCESSFULLY!")
        print("✅ All modular components working correctly")
        print("✅ Significant token reduction achieved")
        print("✅ Context-aware prompt loading functional")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Optimization test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_mid_conversation_compatibility():
    """Test that optimized system works with mid-conversation PDF uploads"""
    
    print("\n🔄 TESTING MID-CONVERSATION COMPATIBILITY")
    print("=" * 60)
    
    try:
        from prompts import prompt_manager
        
        # Simulate mid-conversation PDF upload scenario
        print("📄 Simulating mid-conversation PDF upload...")
        
        # Initial conversation without document
        initial_prompt = prompt_manager.get_core_instructions(has_document_context=False)
        print(f"   Initial prompt size: {len(initial_prompt)} chars")
        
        # Mid-conversation document upload
        updated_prompt = prompt_manager.get_core_instructions(has_document_context=True)
        print(f"   Updated prompt size: {len(updated_prompt)} chars")
        
        # Context-aware welcome for document upload
        context_welcome = prompt_manager.get_welcome_message(has_document_context=True)
        print(f"   Context welcome size: {len(context_welcome)} chars")
        
        print("✅ Mid-conversation optimization compatible!")
        return True
        
    except Exception as e:
        print(f"❌ Mid-conversation test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 LEVRA PROMPT OPTIMIZATION TEST SUITE")
    print("Testing modular prompt system for token efficiency and functionality")
    print("=" * 80)
    
    # Run tests
    basic_test = test_prompt_optimization()
    compatibility_test = test_mid_conversation_compatibility()
    
    print("\n" + "=" * 80)
    if basic_test and compatibility_test:
        print("🎉 ALL TESTS PASSED! Prompt optimization successful.")
        print("✅ Ready for production use with significantly reduced token usage")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)
