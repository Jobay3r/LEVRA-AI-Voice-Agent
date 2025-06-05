#!/usr/bin/env python3
"""
Quick HSF Test - Identify specific failures
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_scenarios():
    print("Testing scenarios...")
    try:
        from prompts.scenarios import SCENARIO_TEMPLATES
        
        test_scenario = SCENARIO_TEMPLATES["gen_z_leadership_emergence"]
        print(f"✓ Scenario exists")
        print(f"  Scoring criteria: {test_scenario['scoring_criteria']}")
        print(f"  HSF category: {test_scenario['hsf_skill_category']}")
        
        # Check specific assertion
        assert "generational_bridge_building" in test_scenario["scoring_criteria"]
        print("✓ generational_bridge_building found")
        
        assert "Leadership Presence" == test_scenario["hsf_skill_category"]
        print("✓ Leadership Presence category found")
        
        # Check setup content
        setup_check = "Gen Z" in test_scenario["setup"] or "AI" in test_scenario["setup"] or "remote" in test_scenario["setup"]
        print(f"✓ Setup check passed: {setup_check}")
        print(f"  Setup content: {test_scenario['setup'][:100]}...")
        
    except Exception as e:
        print(f"❌ Scenario test failed: {e}")
        import traceback
        traceback.print_exc()

def test_scoring():
    print("\nTesting scoring matrix...")
    try:
        from prompts.feedback import SCORING_MATRIX
        
        hsf_skills = [
            "digital_leadership",
            "generational_bridge_building", 
            "purpose_driven_communication",
            "cultural_intelligence",
            "future_ready_mindset",
            "emotional_intelligence"
        ]
        
        for skill in hsf_skills:
            if skill in SCORING_MATRIX:
                print(f"✓ {skill} found")
                skill_data = SCORING_MATRIX[skill]
                
                # Check levels exist
                for level in ["excellent", "good", "needs_improvement", "poor"]:
                    if level in skill_data:
                        print(f"  ✓ {level} level exists")
                        indicators = str(skill_data[level]["indicators"])
                        has_keywords = "Gen Z" in indicators or "digital" in indicators or "generational" in indicators
                        print(f"    Keywords check: {has_keywords}")
                    else:
                        print(f"  ❌ {level} level missing")
            else:
                print(f"❌ {skill} not found")
                
    except Exception as e:
        print(f"❌ Scoring test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scenarios()
    test_scoring()
