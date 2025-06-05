"""
LEVRA AI Learning Coach - HSF-Powered Feedback and Assessment Module

Proprietary Human Skills Framework scoring system designed to close the £6.9T 
global soft skills gap through precise, actionable feedback for Gen Z learners.
"""

# LEVRA Human Skills Framework (HSF) - Proprietary Scoring Matrix
SCORING_MATRIX = {
    "communication_clarity": {
        "excellent": {"score": 9-10, "indicators": ["Used Gen Z-appropriate directness", "Avoided unnecessary corporate speak", "Confirmed understanding actively", "Adapted style to audience"]},
        "good": {"score": 7-8, "indicators": ["Generally clear and direct", "Minor generational disconnect", "Mostly accessible language"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Too formal/informal for context", "Generational style mismatch", "Needed clarification"]},
        "poor": {"score": 1-4, "indicators": ["Communication style alienated audience", "Failed to bridge generational gap", "Unclear core message"]}
    },
    
    "digital_leadership": {
        "excellent": {"score": 9-10, "indicators": ["Leveraged technology for team connection", "Adapted to different digital preferences", "Led virtual collaboration effectively"]},
        "good": {"score": 7-8, "indicators": ["Good digital facilitation", "Included most team members", "Used tech appropriately"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Basic digital skills", "Some team members excluded", "Missed tech opportunities"]},
        "poor": {"score": 1-4, "indicators": ["Poor digital presence", "Failed to connect virtually", "Technology hindered communication"]}
    },
    
    "generational_bridge_building": {
        "excellent": {"score": 9-10, "indicators": ["Respected different generational perspectives", "Found common ground", "Leveraged diverse strengths", "Built mutual respect"]},
        "good": {"score": 7-8, "indicators": ["Showed generational awareness", "Some successful bridging", "Respectful interactions"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Limited generational empathy", "Occasional age-based assumptions", "Missed bridge-building opportunities"]},
        "poor": {"score": 1-4, "indicators": ["Reinforced generational stereotypes", "Created age-based conflict", "Failed to find common ground"]}
    },
      "purpose_driven_communication": {
        "excellent": {"score": 9-10, "indicators": ["Connected Gen Z values to outcomes", "Articulated meaningful impact", "Inspired digital-age vision", "Balanced authenticity with professionalism"]},
        "good": {"score": 7-8, "indicators": ["Clear Gen Z value alignment", "Good impact articulation", "Professional digital presence"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Vague generational values", "Struggled with digital storytelling", "Either too casual or too formal"]},
        "poor": {"score": 1-4, "indicators": ["No Gen Z connection", "Failed to inspire digitally", "Purpose disconnected from modern work"]}
    },
      "cultural_intelligence": {
        "excellent": {"score": 9-10, "indicators": ["Adapted digital communication across cultures", "Showed Gen Z global mindset", "Navigated generational-cultural nuances", "Built digital-inclusive environment"]},
        "good": {"score": 7-8, "indicators": ["Good generational-cultural awareness", "Digital adaptations across cultures", "Gen Z inclusive approach"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Basic digital-cultural sensitivity", "Missed generational-cultural cues", "Limited cross-cultural digital skills"]},
        "poor": {"score": 1-4, "indicators": ["Digital-cultural misunderstandings", "Gen Z-insensitive communication", "Failed at digital global inclusion"]}
    },
      "emotional_intelligence": {
        "excellent": {"score": 9-10, "indicators": ["Recognized Gen Z emotional context", "Digital empathy in action", "Led mental health conversations", "Created generational psychological safety"]},
        "good": {"score": 7-8, "indicators": ["Good digital emotional awareness", "Gen Z supportive responses", "Strong digital empathy"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Basic generational emotion recognition", "Digital emotional cues missed", "Limited virtual support skills"]},
        "poor": {"score": 1-4, "indicators": ["Poor digital emotional awareness", "Gen Z-inappropriate responses", "Failed at virtual support"]}
    },
      "future_ready_mindset": {
        "excellent": {"score": 9-10, "indicators": ["Led Gen Z digital transformation", "Balanced digital innovation with ethics", "Modeled generational adaptability", "Digital change leadership"]},
        "good": {"score": 7-8, "indicators": ["Good digital adaptability", "Gen Z innovative thinking", "Digital future preparation"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Digital hesitancy", "Limited Gen Z perspective", "Generational adaptability gaps"]},
        "poor": {"score": 1-4, "indicators": ["Digital resistance", "Anti-Gen Z mindset", "Failed generational transition"]}
    }
}

# Real-time coaching prompts optimized for Gen Z learning preferences
REAL_TIME_COACHING = {
    "encouragement": [
        "That's the kind of authentic leadership Gen Z brings! Keep going...",
        "Perfect example of bridging generational differences - continue with that approach!",
        "You're showing strong digital-native communication skills here!",
        "Great way to balance purpose with professionalism!"
    ],
    
    "redirect": [
        "Think about how this might land with different generations...",
        "What would make this more psychologically safe for everyone?",
        "How could you leverage your digital fluency here?",
        "What's the underlying purpose driving this conversation?"
    ],    "gen_z_specific_guidance": [
        "Your fresh digital perspective brings unique value",
        "Stay authentically direct while showing respect",
        "Your digital-native leadership can drive change",
        "Bridge gaps with your tech-savvy perspective",
        "Remember - your authentic voice is valuable"
    ],      "hsf_skill_nudges": [
        "This is your chance to show authentic digital leadership...",
        "Use your Gen Z perspective to bridge perspectives...",
        "Demonstrate your digital-native approach here...",
        "Let your authentic communication style shine..."
    ],
    
    "skill_prompt": [        "This is a great moment to demonstrate [specific skill]...",
        "Remember your goal of [learning objective]...",
        "How might you use [skill technique] here?"
    ],
    
    "reflection": [
        "What do you think went well in that interaction?",
        "How did that feel compared to your usual approach?",
        "What would you do differently next time?"
    ]
}

def calculate_skill_score(performance_indicators):
    """
    Calculate overall skill score based on performance indicators
    
    Args:
        performance_indicators (dict): Scores for each skill dimension
    
    Returns:
        float: Overall skill score (1-10)
    """
    if not performance_indicators:
        return 0.0
    
    total_score = sum(performance_indicators.values())
    average_score = total_score / len(performance_indicators)
    return round(average_score, 1)

def format_feedback_response(skill_scores, strengths, improvements, next_steps):
    """
    Format comprehensive feedback response for user
    
    Args:
        skill_scores (dict): Scores for each skill dimension
        strengths (list): Observed positive behaviors
        improvements (list): Areas for development
        next_steps (list): Recommended actions
    
    Returns:
        str: Formatted feedback message
    """
    overall_score = calculate_skill_score(skill_scores)
    
    feedback = f"""
    🎯 LEVRA PERFORMANCE FEEDBACK
    
    Overall Skill Score: {overall_score}/10
    
    ✨ STRENGTHS DEMONSTRATED:
    {chr(10).join([f"• {strength}" for strength in strengths])}
    
    📈 IMPROVEMENT OPPORTUNITIES:
    {chr(10).join([f"• {improvement}" for improvement in improvements])}
    
    📊 DETAILED SCORES:
    {chr(10).join([f"• {skill.replace('_', ' ').title()}: {score}/10" for skill, score in skill_scores.items()])}
    
    🚀 NEXT STEPS:
    {chr(10).join([f"{i+1}. {step}" for i, step in enumerate(next_steps)])}
    
    Ready for another scenario to continue building these skills? 💪
    """
    return feedback

# Template functions for dynamic feedback generation
def generate_skill_assessment_message(user_msg):
    """Generate skill assessment message based on user input"""
    return f"""As LEVRA's AI Learning Coach, analyze the user's context and create an engaging, 
    realistic workplace scenario for skill development.
    
    Based on their input: "{user_msg}"
    
    YOUR TASK:
    1. Identify their role/industry context and current skill focus
    2. Create an authentic workplace scenario that challenges this specific skill
    3. Set clear success criteria for the interaction
    4. Prepare to provide real-time coaching during the scenario
    
    SCENARIO DESIGN PRINCIPLES:
    - Make it feel like a real workplace situation they might encounter
    - Include realistic characters, settings, and challenges
    - Ensure the scenario has clear learning objectives
    - Build in opportunities for the user to demonstrate the target skill
    - Prepare specific feedback criteria for scoring their performance
    
    RESPONSE FORMAT:
    1. Set the scene with realistic details
    2. Introduce the characters/situation
    3. Present the challenge or interaction opportunity
    4. Guide them into the scenario naturally
    
    Remember: Gen Z learners engage best with authentic, relatable scenarios that feel genuinely useful for their career growth.
    Make this feel like practice for real life, not an academic exercise.
    """

def generate_feedback_template(interaction, skill_focus, performance_criteria):
    """Generate feedback template for specific interaction"""
    return f"""
    LEVRA LEARNING COACH - PERFORMANCE FEEDBACK
    
    Skill Focus: {skill_focus}
    Scenario Completed: {interaction}
    
    PERFORMANCE ANALYSIS:
    
    🎯 STRENGTHS DEMONSTRATED:
    - [Identify 2-3 specific positive behaviors observed]
    - [Link to real workplace impact]
    
    📈 IMPROVEMENT OPPORTUNITIES:
    - [1-2 specific areas for development]
    - [Practical suggestions for immediate improvement]
    
    SKILL SCORE: __/10
    
    📊 SCORING BREAKDOWN:
    - Communication Clarity: __/10
    - Emotional Intelligence: __/10  
    - Problem-Solving Approach: __/10
    - Professional Presence: __/10
    
    🚀 NEXT STEPS:
    1. [Specific action to practice before next scenario]
    2. [Micro-learning suggestion for continued growth]
    
    Ready for another scenario to practice this skill, or want to focus on a different human skill?
    
    Performance Criteria Used: {performance_criteria}
    """
