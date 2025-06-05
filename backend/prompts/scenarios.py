"""
LEVRA AI Learning Coach - Scenario Templates Module

This module contains pre-defined scenario templates for workplace situations.
"""

"""
LEVRA AI Learning Coach - HSF-Powered Scenario Templates Module

Gen Z-focused workplace scenarios designed for LEVRA's Human Skills Framework,
addressing the £6.9T global soft skills gap through authentic practice experiences.
"""

# HSF-aligned scenario templates targeting critical Gen Z workplace challenges
SCENARIO_TEMPLATES = {
    "gen_z_leadership_emergence": {
        "setup": """You're a Gen Z professional (25) leading a mixed-age team on a digital transformation project. 
                   A Boomer colleague (58) just dismissed your AI-integration proposal as "unnecessary tech complexity" 
                   in front of the whole team. You need to address this generational divide while establishing your 
                   leadership credibility and moving the project forward.""",
        "scoring_criteria": ["generational_bridge_building", "confident_leadership", "respectful_assertiveness", "innovation_advocacy"],
        "character_context": "Experienced colleague feels threatened by new technology and younger leadership",
        "hsf_skill_category": "Leadership Presence"
    },
    
    "remote_team_connection": {
        "setup": """You're managing a fully remote team where engagement has dropped significantly. Team members are 
                   camera-off in meetings, missing deadlines, and seem disconnected. You've noticed your Gen Z teammates 
                   prefer quick Slack messages while older colleagues want formal meetings. You need to re-energize the team 
                   and create better connection across communication preferences.""",
        "scoring_criteria": ["digital_empathy", "inclusive_communication", "team_motivation", "adaptive_management"],
        "character_context": "Team members have different communication styles and varying levels of remote work comfort",
        "hsf_skill_category": "Digital Leadership"
    },
    
    "ai_ethics_workplace_discussion": {
        "setup": """You're a Gen Z data scientist leading a discussion about AI ethics in your company. An older teammate 
                   suggests "we don't need all these new AI safeguards" while a Gen X manager worries about job displacement. 
                   You need to bridge these perspectives while advocating for responsible AI development.""",
        "scoring_criteria": ["digital_leadership", "ethical_reasoning", "generational_bridge_building", "future_advocacy"],
        "character_context": "Multi-generational team with varying AI comfort levels",
        "hsf_skill_category": "Digital Ethics Leadership"
    },

    "cultural_fluency_global_team": {
        "setup": """You're collaborating with a global remote team spanning three continents. As a Gen Z team member, 
                   you notice cultural misunderstandings around communication styles and work norms. You need to help 
                   bridge these gaps while maintaining team productivity.""",
        "scoring_criteria": ["cultural_intelligence", "digital_communication", "inclusive_leadership", "adaptability"],
        "character_context": "Diverse global team with different cultural approaches",
        "hsf_skill_category": "Cultural Intelligence"
    },

    "social_impact_business_case": {
        "setup": """As a Gen Z product manager, you're pitching a sustainability initiative that could temporarily 
                   impact short-term profits. Senior leadership seems skeptical of the "purpose over profit" approach. 
                   You need to make a compelling business case while staying true to your values.""",
        "scoring_criteria": ["purpose_driven_communication", "business_acumen", "change_leadership", "value_alignment"],
        "character_context": "Traditional business leaders focused on conventional metrics",
        "hsf_skill_category": "Purpose-Driven Leadership"
    },

    "mental_health_workplace_conversation": {
        "setup": """A Gen Z colleague confides in you about their mental health struggles affecting work. Your 
                   traditional manager has expressed skepticism about mental health accommodations. You need to 
                   support your colleague while helping create a more understanding workplace culture.""",
        "scoring_criteria": ["emotional_intelligence", "empathetic_leadership", "culture_change", "psychological_safety"],
        "character_context": "Traditional workplace transitioning to modern wellbeing practices",
        "hsf_skill_category": "Wellbeing Leadership"
    }
}

# Dynamic scenario generator functions
def generate_scenario_prompt(user_role, skill_focus, difficulty_level="intermediate"):
    """
    Generate a contextual scenario prompt based on user parameters
    
    Args:
        user_role (str): User's professional role or industry
        skill_focus (str): Target skill for development
        difficulty_level (str): Scenario complexity level
    
    Returns:
        str: Formatted scenario prompt for AI generation
    """
    base_prompt = f"""
    CREATE REALISTIC WORKPLACE SCENARIO
    
    User Role: {user_role}
    Skill Focus: {skill_focus}
    Difficulty: {difficulty_level}
    
    Requirements:
    1. Create authentic workplace situation relevant to {user_role}
    2. Design clear opportunities to practice {skill_focus}
    3. Include realistic characters with believable motivations
    4. Set clear success criteria for assessment
    5. Ensure scenario feels genuinely useful for career development
    
    Begin the scenario naturally and guide the user into the interaction.
    """
    return base_prompt

def select_appropriate_scenario(user_context, previous_scenarios=None):
    """
    Select most appropriate scenario based on user context and history
    
    Args:
        user_context (dict): User role, skill focus, performance history
        previous_scenarios (list): Previously completed scenarios
    
    Returns:
        dict: Selected scenario template with customizations
    """
    skill_focus = user_context.get("skill_focus", "communication")
    
    # Map skills to appropriate scenario types
    skill_scenario_mapping = {
        "communication": ["difficult_conversation", "client_presentation"],
        "leadership": ["team_leadership", "difficult_conversation"],
        "teamwork": ["team_leadership", "cross_cultural_communication"],
        "conflict_resolution": ["difficult_conversation", "team_leadership"],
        "presentation": ["client_presentation"],
        "cultural_awareness": ["cross_cultural_communication"]
    }
    
    available_scenarios = skill_scenario_mapping.get(skill_focus, ["difficult_conversation"])
    
    # Avoid repeating recent scenarios
    if previous_scenarios:
        available_scenarios = [s for s in available_scenarios if s not in previous_scenarios[-2:]]
    
    # Select first available scenario (could be enhanced with more sophisticated logic)
    selected_scenario_key = available_scenarios[0] if available_scenarios else "difficult_conversation"
    selected_scenario = SCENARIO_TEMPLATES.get(selected_scenario_key, SCENARIO_TEMPLATES["difficult_conversation"])
    
    return {
        "type": selected_scenario_key,
        "setup": selected_scenario["setup"],
        "scoring_criteria": selected_scenario["scoring_criteria"],
        "character_context": selected_scenario["character_context"]
    }

# Gen Z-focused industry adaptations addressing modern workplace challenges
INDUSTRY_ADAPTATIONS = {
    "tech": {
        "language_style": "Direct, innovative, purpose-driven with technical depth",
        "common_scenarios": ["AI ethics discussions", "remote team leadership", "cross-functional collaboration", "technical debt vs innovation trade-offs"],
        "cultural_notes": "Fast-paced innovation, flat hierarchies, work-life integration, continuous learning mindset",
        "gen_z_challenges": ["Imposter syndrome in senior roles", "Balancing speed with ethics", "Leading older colleagues"]
    },
    
    "edtech": {
        "language_style": "Empathetic, data-driven, learner-focused with innovation emphasis",
        "common_scenarios": ["stakeholder buy-in for new learning methods", "addressing learning accessibility", "ROI discussions for educational innovation"],
        "cultural_notes": "Mission-driven, evidence-based, collaborative, inclusive design thinking",
        "gen_z_challenges": ["Proving credibility to traditional educators", "Balancing technology with human connection"]
    },
    
    "consulting": {
        "language_style": "Analytical, confident, client-focused with fresh perspectives",
        "common_scenarios": ["challenging senior client assumptions", "presenting innovative solutions", "navigating hierarchy while adding value"],
        "cultural_notes": "Results-oriented, relationship-driven, intellectual rigor, adaptability",
        "gen_z_challenges": ["Building trust with C-level executives", "Balancing authenticity with professionalism"]
    },
    
    "healthcare": {
        "language_style": "Empathetic, precise, patient-centered with digital fluency",
        "common_scenarios": ["digital health advocacy", "interdisciplinary team communication", "patient education with technology"],
        "cultural_notes": "High stakes, collaborative, evidence-based, compassionate care focus",
        "gen_z_challenges": ["Technology integration resistance", "Communicating across generational patient preferences"]
    },
    
    "finance": {
        "language_style": "Analytical, confident, ESG-conscious with traditional rigor",
        "common_scenarios": ["sustainable investing discussions", "fintech adoption advocacy", "risk assessment presentations"],
        "cultural_notes": "Results-oriented, compliance-focused, relationship-driven, increasingly values-based",
        "gen_z_challenges": ["Balancing profit with purpose", "Modernizing traditional practices"]
    },
    
    "startup": {
        "language_style": "Agile, visionary, impact-focused with resource consciousness",
        "common_scenarios": ["investor pitches", "pivot discussions", "team scaling challenges", "work-life boundary setting"],
        "cultural_notes": "High energy, risk-tolerant, mission-driven, rapid iteration mindset",
        "gen_z_challenges": ["Maintaining mental health under pressure", "Building credibility without extensive experience"]
    }
}
