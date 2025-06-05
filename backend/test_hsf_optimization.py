#!/usr/bin/env python3
"""
LEVRA HSF Optimization Test Suite

Comprehensive testing of the Human Skills Framework optimizations
designed to address the £6.9T global soft skills gap through
Gen Z-optimized learning experiences.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_hsf_core_instructions():
    """Test HSF-enhanced core instructions"""
    print("🧠 Testing HSF Core Instructions...")
    
    try:
        from prompts import get_instructions
        
        # Test basic instructions
        basic_instructions = get_instructions(has_document_context=False)
        assert "Human Skills Framework (HSF)" in basic_instructions
        assert "£6.9T soft skills gap" in basic_instructions
        assert "Gen Z" in basic_instructions
        assert "psychologically safe" in basic_instructions
        
        # Test document-enhanced instructions
        doc_instructions = get_instructions(has_document_context=True)
        assert len(doc_instructions) > len(basic_instructions)
        assert "multi-modal" in doc_instructions.lower()
        
        print("✅ HSF Core Instructions: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ HSF Core Instructions: FAILED - {e}")
        return False

def test_gen_z_welcome_messages():
    """Test Gen Z-optimized welcome messages"""
    print("🚀 Testing Gen Z Welcome Messages...")
    
    try:
        from prompts import get_welcome_message
        
        # Test basic welcome
        basic_welcome = get_welcome_message(has_document_context=False)
        assert "95% of e-learning gets abandoned" in basic_welcome
        assert "99% of Gen Z prefer" in basic_welcome
        assert "HSF-based feedback" in basic_welcome
        assert "superpower" in basic_welcome
        
        # Test document-context welcome
        doc_welcome = get_welcome_message(has_document_context=True)
        assert "hyper-personalized training" in doc_welcome
        assert "interactive, relevant, and immediately applicable" in doc_welcome
        assert "superpowers" in doc_welcome
        
        print("✅ Gen Z Welcome Messages: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Gen Z Welcome Messages: FAILED - {e}")
        return False

def test_gen_z_scenarios():
    """Test Gen Z-focused workplace scenarios"""
    print("🎭 Testing Gen Z Workplace Scenarios...")
    
    try:
        from prompts.scenarios import SCENARIO_TEMPLATES
        
        # Test new Gen Z scenarios exist
        gen_z_scenarios = [
            "gen_z_leadership_emergence",
            "remote_team_connection", 
            "ai_ethics_workplace_discussion",
            "cultural_fluency_global_team",
            "social_impact_business_case",
            "mental_health_workplace_conversation"
        ]
        
        for scenario in gen_z_scenarios:
            assert scenario in SCENARIO_TEMPLATES, f"Missing scenario: {scenario}"
            scenario_data = SCENARIO_TEMPLATES[scenario]
            assert "hsf_skill_category" in scenario_data, f"Missing HSF category in {scenario}"
            assert "Gen Z" in scenario_data["setup"] or "AI" in scenario_data["setup"] or "remote" in scenario_data["setup"]
        
        # Test scenario content quality
        test_scenario = SCENARIO_TEMPLATES["gen_z_leadership_emergence"]
        assert "generational_bridge_building" in test_scenario["scoring_criteria"]
        assert "Leadership Presence" == test_scenario["hsf_skill_category"]
        
        print("✅ Gen Z Workplace Scenarios: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Gen Z Workplace Scenarios: FAILED - {e}")
        return False

def test_hsf_scoring_matrix():
    """Test HSF scoring framework"""
    print("📊 Testing HSF Scoring Matrix...")
    
    try:
        from prompts.feedback import SCORING_MATRIX
          # Test new HSF skills exist
        hsf_skills = [
            "digital_leadership",
            "generational_bridge_building",
            "purpose_driven_communication",
            "cultural_intelligence",
            "future_ready_mindset",
            "emotional_intelligence"
        ]
        
        for skill in hsf_skills:
            assert skill in SCORING_MATRIX, f"Missing HSF skill: {skill}"
            skill_data = SCORING_MATRIX[skill]
            
            # Verify scoring levels
            for level in ["excellent", "good", "needs_improvement", "poor"]:
                assert level in skill_data, f"Missing scoring level {level} in {skill}"
                assert "Gen Z" in str(skill_data[level]["indicators"]) or "digital" in str(skill_data[level]["indicators"]) or "generational" in str(skill_data[level]["indicators"])
        
        print("✅ HSF Scoring Matrix: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ HSF Scoring Matrix: FAILED - {e}")
        return False

def test_gen_z_coaching_prompts():
    """Test Gen Z-optimized coaching prompts"""
    print("💪 Testing Gen Z Coaching Prompts...")
    
    try:
        from prompts.feedback import REAL_TIME_COACHING
        
        # Test new Gen Z coaching categories
        coaching_categories = [
            "gen_z_specific_guidance",
            "hsf_skill_nudges"
        ]
        
        for category in coaching_categories:
            assert category in REAL_TIME_COACHING, f"Missing coaching category: {category}"
            prompts = REAL_TIME_COACHING[category]
            assert len(prompts) > 0, f"Empty coaching category: {category}"
            
            # Verify Gen Z-relevant content
            combined_prompts = " ".join(prompts)
            assert "authentic" in combined_prompts or "digital" in combined_prompts or "perspective" in combined_prompts
        
        print("✅ Gen Z Coaching Prompts: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Gen Z Coaching Prompts: FAILED - {e}")
        return False

def test_industry_adaptations():
    """Test updated industry adaptations with Gen Z focus"""
    print("🏢 Testing Industry Adaptations...")
    
    try:
        from prompts.scenarios import INDUSTRY_ADAPTATIONS
        
        # Test enhanced industries
        for industry, data in INDUSTRY_ADAPTATIONS.items():
            assert "gen_z_challenges" in data, f"Missing Gen Z challenges for {industry}"
            assert len(data["gen_z_challenges"]) > 0, f"Empty Gen Z challenges for {industry}"
            
            # Verify realistic Gen Z workplace challenges
            challenges = " ".join(data["gen_z_challenges"])
            assert any(keyword in challenges.lower() for keyword in [
                "credibility", "authenticity", "technology", "senior", 
                "traditional", "innovation", "mentoring", "leadership"
            ]), f"Unrealistic Gen Z challenges for {industry}"
        
        print("✅ Industry Adaptations: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Industry Adaptations: FAILED - {e}")
        return False

def test_hsf_state_management():
    """Test HSF-enhanced state management"""
    print("📈 Testing HSF State Management...")
    
    try:
        from prompts.state_management import (
            CONVERSATION_STATE, 
            track_performance, 
            get_skill_trends,
            generate_learning_pathway
        )
        
        # Test HSF skill profile structure
        hsf_profile = CONVERSATION_STATE["hsf_skill_profile"]
        required_skills = [
            "communication_clarity",
            "digital_leadership", 
            "generational_bridge_building",
            "purpose_driven_communication",
            "cultural_intelligence",
            "emotional_intelligence",
            "future_ready_mindset"
        ]
        
        for skill in required_skills:
            assert skill in hsf_profile, f"Missing HSF skill in profile: {skill}"
            skill_data = hsf_profile[skill]
            assert all(key in skill_data for key in ["current_level", "target_level", "trend"])
        
        # Test performance tracking
        test_scores = {"communication_clarity": 8, "digital_leadership": 7}
        performance = track_performance("gen_z_leadership_emergence", test_scores)
        assert "gen_z_engagement_factors" in performance
        
        # Test skill trends with Gen Z messaging
        trend_result = get_skill_trends("communication_clarity")
        assert isinstance(trend_result, dict)
        assert "message" in trend_result
        assert any(emoji in trend_result["message"] for emoji in ["🚀", "📈", "💪"])
        
        print("✅ HSF State Management: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ HSF State Management: FAILED - {e}")
        return False

def test_content_processing():
    """Test HSF-powered content processing"""
    print("📄 Testing HSF Content Processing...")
    
    try:
        from prompts.content_processing import process_learning_material, process_multimodal_content
        
        # Test learning material processing
        test_material = "LEVRA presentation about closing skills gap"
        test_context = {"role": "CEO", "industry": "edtech"}
        
        processed = process_learning_material(test_material, test_context)
        assert "HSF" in processed
        assert "Gen Z" in processed
        assert "99% engagement" in processed
        assert "£6.9T" in processed
        
        # Test multimodal processing
        multimodal = process_multimodal_content("PDF", "Company training manual", test_context)
        assert "LEVRA HSF" in multimodal
        assert "psychologically safe" in multimodal
        assert "authentic workplace conversations" in multimodal
        
        print("✅ HSF Content Processing: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ HSF Content Processing: FAILED - {e}")
        return False

def test_prompt_optimization_performance():
    """Test that HSF optimization maintains token reduction"""
    print("⚡ Testing HSF Optimization Performance...")
    
    try:
        from prompts import build_conversation_prompt, build_hsf_feedback_prompt
        
        # Test basic conversation prompt length
        basic_context = {"industry": "tech", "role": "developer"}
        basic_prompt = build_conversation_prompt(basic_context, has_document=False)
        
        # Should be significantly shorter than original 26,849 characters
        assert len(basic_prompt) < 5000, f"Basic prompt too long: {len(basic_prompt)} chars"
        
        # Test document context prompt
        doc_prompt = build_conversation_prompt(basic_context, has_document=True, scenario_type="gen_z_leadership_emergence")
        assert len(doc_prompt) < 7000, f"Document prompt too long: {len(doc_prompt)} chars"
        
        # Test HSF feedback prompt
        performance_data = {"interaction": "Led team meeting effectively"}
        feedback_prompt = build_hsf_feedback_prompt(performance_data, "digital_leadership")
        assert len(feedback_prompt) < 2000, f"Feedback prompt too long: {len(feedback_prompt)} chars"
        assert "🎯" in feedback_prompt  # Should include Gen Z-friendly formatting
        
        print("✅ HSF Optimization Performance: PASSED")
        print(f"   📊 Basic prompt: {len(basic_prompt)} chars")
        print(f"   📊 Document prompt: {len(doc_prompt)} chars") 
        print(f"   📊 Feedback prompt: {len(feedback_prompt)} chars")
        return True
        
    except Exception as e:
        print(f"❌ HSF Optimization Performance: FAILED - {e}")
        return False

def test_backward_compatibility():
    """Test that HSF changes maintain backward compatibility"""
    print("🔄 Testing Backward Compatibility...")
    
    try:
        # Test all original function imports still work
        from prompts import (
            get_instructions,
            get_welcome_message,
            get_skill_assessment_message, 
            get_feedback_template,
            build_conversation_prompt
        )
        
        # Test basic function calls
        instructions = get_instructions()
        welcome = get_welcome_message()
        assessment = get_skill_assessment_message("I want to improve communication")
        
        assert len(instructions) > 0
        assert len(welcome) > 0
        assert len(assessment) > 0
        
        print("✅ Backward Compatibility: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Backward Compatibility: FAILED - {e}")
        return False

def main():
    """Run complete HSF optimization test suite"""
    print("🎯 LEVRA HSF OPTIMIZATION TEST SUITE")
    print("=" * 50)
    print("Testing Human Skills Framework optimizations for Gen Z learners")
    print("Target: Address £6.9T global soft skills gap through authentic practice\n")
    
    tests = [
        test_hsf_core_instructions,
        test_gen_z_welcome_messages,
        test_gen_z_scenarios,
        test_hsf_scoring_matrix,
        test_gen_z_coaching_prompts,
        test_industry_adaptations,
        test_hsf_state_management,
        test_content_processing,
        test_prompt_optimization_performance,
        test_backward_compatibility    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAILED - {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 50)
    print(f"🎯 HSF OPTIMIZATION TEST RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🚀 ALL TESTS PASSED! HSF optimization is ready for Gen Z learners!")
        print("💪 LEVRA is equipped to close the global human skills gap!")
    else:
        print(f"\n⚠️  {failed} tests failed. Review issues before deployment.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
