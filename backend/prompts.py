"""
LEVRA AI Learning Coach Configuration Module

This module defines the conversational behavior, adaptive learning patterns, and interactive 
response systems for LEVRA's AI-powered Human Skills Learning Coach. Designed specifically 
for Gen Z learners who prefer immersive, experiential learning over traditional methods.

Core Features:
1. Multi-modal conversation simulation (voice, text, scenario-based interactions)
2. Real-time adaptive feedback with scoring mechanisms
3. Context-aware interactions across varied learning materials
4. Authentic, realistic conversational scenarios
5. Personalized learning pathways with continuous skills tracking

This system bridges the Human Skills gap through engaging, data-driven learning experiences
that simulate real-world professional interactions.
"""

# Core AI Learning Coach instructions optimized for LEVRA's immersive learning platform
# These instructions define the AI's role as an adaptive, context-aware learning coach
INSTRUCTIONS = """
    You are LEVRA's AI Learning Coach, specifically designed to train Gen Z professionals in Human Skills 
    through immersive, realistic conversational experiences. You excel at creating authentic workplace 
    scenarios that feel genuine and engaging.
    
    YOUR CORE MISSION:
    - Simulate realistic workplace conversations and situations
    - Provide immediate, personalized feedback with specific scoring
    - Adapt scenarios based on learner's industry, role, and skill level
    - Create psychologically safe practice environments
    - Deliver bite-sized, actionable insights that stick
    
    INTERACTION PRINCIPLES:
    1. AUTHENTICITY: Every scenario should feel like a real workplace interaction
    2. ADAPTIVITY: Adjust complexity and context based on user's responses and progress
    3. ENGAGEMENT: Use conversational patterns that resonate with Gen Z learning preferences
    4. FEEDBACK: Provide immediate, specific, and constructive feedback with clear scoring
    5. GROWTH: Focus on practical application and skill building, not just theory
    
    RESPONSE FRAMEWORK:
    - Always respond naturally and conversationally
    - Avoid formal academic language - use modern, accessible communication
    - Provide specific, actionable feedback after interactions
    - Score interactions based on predefined criteria (communication clarity, emotional intelligence, problem-solving approach)
    - Adapt subsequent scenarios based on identified skill gaps
    
    IMPORTANT: You understand various educational inputs (PDFs, curriculum materials, prompts) and can create 
    relevant questions and scenarios from any learning context. You work across subjective cultural nuances 
    to technical content with equal effectiveness.
"""

# Welcome message for LEVRA's immersive learning experience
# Designed to immediately engage Gen Z learners and set expectations for interactive training
WELCOME_MESSAGE = """Hey! Welcome to LEVRA - your AI Learning Coach for Human Skills training! 🚀

I'm here to help you level up your soft skills through realistic workplace scenarios and conversations. Think of me as your practice partner who creates authentic situations where you can build confidence and get real-time feedback.

Here's what makes our training different:
✨ Real workplace scenarios, not boring theory
🎯 Instant feedback with specific scores
🔄 Adaptive learning that adjusts to your progress
🛡️ Safe space to practice and make mistakes

Ready to start? Tell me:
1. What's your current role or the position you're aiming for?
2. Which human skill do you want to focus on today? (communication, leadership, teamwork, conflict resolution, etc.)

Let's make this training session count! 💪"""

# Dynamic scenario generator that creates realistic workplace interactions
# Adapts based on user input, role, and skill level for authentic learning experiences
SKILL_ASSESSMENT_MESSAGE = lambda msg: f"""As LEVRA's AI Learning Coach, analyze the user's context and create an engaging, 
    realistic workplace scenario for skill development.
    
    Based on their input: "{msg}"
    
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

# Interactive feedback system for real-time learning and improvement
# Provides immediate, specific, and actionable feedback with scoring mechanisms
PROVIDE_FEEDBACK = lambda interaction, skill_focus, performance_criteria: f"""
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

# Adaptive content generator for multi-modal learning experiences
# Processes various educational inputs (PDFs, curriculum, prompts) into interactive scenarios
CONTENT_PROCESSOR = lambda learning_material, user_context: f"""
    LEVRA AI Learning Coach - Content Adaptation Engine
    
    Processing learning material: {learning_material}
    User context: {user_context}
    
    TASK: Transform this educational content into an engaging, interactive learning experience
    
    ADAPTATION STRATEGY:
    1. Extract key learning objectives from the material
    2. Identify practical application opportunities
    3. Create realistic scenarios that demonstrate these concepts
    4. Design interactive elements that engage Gen Z learning preferences
    5. Establish clear success metrics for skill assessment
    
    OUTPUT REQUIREMENTS:
    - Conversational scenarios based on the content
    - Interactive challenges that test understanding
    - Real-time feedback mechanisms
    - Progressive difficulty levels
    - Cultural and contextual adaptations as needed
    
    Focus on making theoretical concepts practical and applicable through authentic workplace interactions.
"""

# Advanced scenario templates for specific workplace situations
# These create immersive, role-specific learning experiences
SCENARIO_TEMPLATES = {
    "difficult_conversation": {
        "setup": """You're about to have a challenging conversation with a colleague who missed an important deadline, 
                   affecting your project timeline. The colleague seems defensive and stressed. Your goal is to address 
                   the issue while maintaining a positive working relationship.""",
        "scoring_criteria": ["empathy_demonstration", "clear_communication", "solution_focus", "relationship_preservation"],
        "character_context": "Colleague is overwhelmed with multiple projects and feeling criticized"
    },
    
    "team_leadership": {
        "setup": """Your team is divided on a critical decision that needs to be made today. Two team members have 
                   completely different approaches, and tension is rising. As the team leader, you need to facilitate 
                   a resolution that everyone can support.""",
        "scoring_criteria": ["facilitation_skills", "conflict_resolution", "decision_making", "team_unity"],
        "character_context": "Team members have valid but conflicting perspectives based on their expertise"
    },
    
    "client_presentation": {
        "setup": """You're presenting a project proposal to a potential client who is known for asking tough questions 
                   and being skeptical of new approaches. They've just questioned the feasibility of your main recommendation.""",
        "scoring_criteria": ["confidence_under_pressure", "clear_explanation", "handling_objections", "professional_presence"],
        "character_context": "Client is detail-oriented, risk-averse, and needs thorough convincing"
    },
    
    "cross_cultural_communication": {
        "setup": """You're working with international team members from different cultural backgrounds. There's been 
                   a misunderstanding about project expectations, and you need to clarify roles and responsibilities 
                   while being culturally sensitive.""",
        "scoring_criteria": ["cultural_awareness", "inclusive_communication", "clarity", "respect_demonstration"],
        "character_context": "Team members have different communication styles and hierarchical expectations"
    }
}

# Scoring matrix for comprehensive skill assessment
# Maps behaviors to quantifiable scores across multiple dimensions
SCORING_MATRIX = {
    "communication_clarity": {
        "excellent": {"score": 9-10, "indicators": ["Used clear, specific language", "Avoided jargon", "Confirmed understanding"]},
        "good": {"score": 7-8, "indicators": ["Generally clear", "Minor ambiguity", "Mostly accessible language"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Some confusion", "Used unclear terms", "Needed clarification"]},
        "poor": {"score": 1-4, "indicators": ["Unclear communication", "Confusing language", "Failed to convey message"]}
    },
    
    "emotional_intelligence": {
        "excellent": {"score": 9-10, "indicators": ["Recognized emotions", "Responded appropriately", "Managed own reactions"]},
        "good": {"score": 7-8, "indicators": ["Showed awareness", "Generally appropriate responses", "Good self-control"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Limited emotional awareness", "Some inappropriate reactions"]},
        "poor": {"score": 1-4, "indicators": ["Ignored emotional cues", "Inappropriate responses", "Poor self-regulation"]}
    },
    
    "problem_solving": {
        "excellent": {"score": 9-10, "indicators": ["Identified root cause", "Generated creative solutions", "Considered consequences"]},
        "good": {"score": 7-8, "indicators": ["Good analysis", "Reasonable solutions", "Some consideration of impact"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Surface-level analysis", "Limited solution options"]},
        "poor": {"score": 1-4, "indicators": ["Failed to identify issues", "No clear solutions", "Ignored consequences"]}
    },
    
    "adaptability": {
        "excellent": {"score": 9-10, "indicators": ["Adjusted approach quickly", "Embraced change", "Found new opportunities"]},
        "good": {"score": 7-8, "indicators": ["Adapted reasonably well", "Showed flexibility", "Managed change"]},
        "needs_improvement": {"score": 5-6, "indicators": ["Slow to adapt", "Some resistance to change"]},
        "poor": {"score": 1-4, "indicators": ["Rigid thinking", "Resisted change", "Failed to adjust"]}
    }
}

# Learning pathway generator for continuous skill development
# Creates personalized learning journeys based on assessment results
LEARNING_PATHWAY = lambda skills_assessment, user_goals: f"""
    LEVRA PERSONALIZED LEARNING PATH
    
    Based on your assessment: {skills_assessment}
    Your goals: {user_goals}
    
    🎯 RECOMMENDED LEARNING SEQUENCE:
    
    IMMEDIATE FOCUS (This Week):
    - [Skill with lowest score] - Interactive scenarios + daily practice
    - Micro-learning: 5-minute daily exercises
    
    SHORT-TERM GOALS (2-4 Weeks):
    - [Second priority skill] - Progressive scenario complexity
    - Peer practice opportunities
    
    LONG-TERM DEVELOPMENT (1-3 Months):
    - Advanced scenarios combining multiple skills
    - Leadership simulations
    - Cross-cultural communication practice
    
    📊 TRACKING METRICS:
    - Weekly scenario completion rate
    - Skill score improvements
    - Real-world application feedback
    - Confidence self-assessment
    
    🔄 ADAPTIVE MILESTONES:
    The pathway adjusts based on your progress and performance in each scenario.
"""

# Multi-modal interaction handler for various input types
# Processes different types of educational content and user inputs
MULTIMODAL_PROCESSOR = lambda input_type, content, user_context: f"""
    LEVRA MULTIMODAL CONTENT PROCESSOR
    
    Input Type: {input_type}
    Content: {content}
    User Context: {user_context}
    
    PROCESSING STRATEGY:
    
    If PDF/Document:
    - Extract key learning concepts
    - Identify practical application scenarios
    - Create interactive Q&A based on content
    - Design role-play situations from material
    
    If Audio/Video:
    - Analyze communication patterns
    - Extract best practices demonstrated
    - Create practice scenarios based on examples
    - Generate feedback criteria from content
    
    If Curriculum Material:
    - Map theoretical concepts to practical scenarios
    - Create progressive skill-building exercises
    - Design assessment criteria aligned with objectives
    - Generate adaptive learning pathways
    
    OUTPUT: Interactive learning experience with immediate applicability
"""

# Real-time coaching prompts for in-scenario guidance
# Provides adaptive coaching during active learning scenarios
REAL_TIME_COACHING = {
    "encouragement": [
        "Great approach! Keep building on that...",
        "I can see you're thinking through this well...",
        "That's showing strong [skill] - continue with that energy!"
    ],
    
    "redirect": [
        "Let's try a different approach here...",
        "Consider how the other person might be feeling...",
        "What if you focused on [specific skill] in this moment?"
    ],
    
    "skill_prompt": [
        "This is a great moment to demonstrate [specific skill]...",
        "Remember your goal of [learning objective]...",
        "How might you use [skill technique] here?"
    ],
    
    "reflection": [
        "What do you think went well in that interaction?",
        "How did that feel compared to your usual approach?",
        "What would you do differently next time?"
    ]
}

# Industry-specific adaptations for contextual relevance
# Customizes scenarios and language for different professional contexts
INDUSTRY_ADAPTATIONS = {
    "tech": {
        "language_style": "Direct, efficient, innovation-focused",
        "common_scenarios": ["sprint planning", "code review discussions", "stakeholder demos", "technical debt negotiations"],
        "cultural_notes": "Fast-paced, data-driven decisions, flat hierarchies"
    },
    
    "healthcare": {
        "language_style": "Empathetic, precise, patient-centered",
        "common_scenarios": ["patient communication", "interdisciplinary team meetings", "family consultations", "error disclosure"],
        "cultural_notes": "High stakes, collaborative, evidence-based, compassionate"
    },
    
    "finance": {
        "language_style": "Analytical, confident, risk-aware",
        "common_scenarios": ["client advisory meetings", "risk assessments", "regulatory discussions", "investment presentations"],
        "cultural_notes": "Results-oriented, compliance-focused, relationship-driven"
    },
    
    "education": {
        "language_style": "Supportive, clear, development-focused",
        "common_scenarios": ["parent conferences", "student counseling", "faculty meetings", "curriculum planning"],
        "cultural_notes": "Student-centered, collaborative, growth-minded, inclusive"
    }
}

# Helper functions for scenario generation and assessment
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

# Conversation state management for adaptive learning
CONVERSATION_STATE = {
    "current_scenario": None,
    "user_context": {},
    "performance_history": [],
    "learning_pathway": None,
    "session_goals": []
}

def update_conversation_state(key, value):
    """Update conversation state for adaptive learning"""
    CONVERSATION_STATE[key] = value

def get_conversation_state(key):
    """Retrieve conversation state value"""
    return CONVERSATION_STATE.get(key, None)

# Performance tracking utilities
def track_performance(scenario_type, skill_scores, user_feedback=None):
    """Track user performance for adaptive learning"""
    performance_entry = {
        "scenario_type": scenario_type,
        "skill_scores": skill_scores,
        "overall_score": calculate_skill_score(skill_scores),
        "timestamp": "current_session",  # Could be replaced with actual timestamp
        "user_feedback": user_feedback
    }
    
    current_history = get_conversation_state("performance_history") or []
    current_history.append(performance_entry)
    update_conversation_state("performance_history", current_history)
    
    return performance_entry

def get_skill_trends(skill_name):
    """Analyze skill improvement trends over time"""
    history = get_conversation_state("performance_history") or []
    skill_scores = [entry["skill_scores"].get(skill_name, 0) for entry in history if skill_name in entry["skill_scores"]]
    
    if len(skill_scores) < 2:
        return "insufficient_data"
    
    recent_avg = sum(skill_scores[-3:]) / len(skill_scores[-3:])  # Last 3 scores
    earlier_avg = sum(skill_scores[:-3]) / len(skill_scores[:-3]) if len(skill_scores) > 3 else skill_scores[0]
    
    if recent_avg > earlier_avg + 0.5:
        return "improving"
    elif recent_avg < earlier_avg - 0.5:
        return "declining"
    else:
        return "stable"