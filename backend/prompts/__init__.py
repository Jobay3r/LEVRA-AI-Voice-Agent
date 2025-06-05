"""
LEVRA AI Learning Coach - Modularized Prompts Package

This package provides an optimized, modular prompt system that loads only necessary
components for each interaction, significantly reducing token usage and improving performance.

Usage:
    from prompts import prompt_manager, get_instructions, build_conversation_prompt
    
    # Get context-aware instructions
    instructions = build_conversation_prompt(user_context, has_document=True)
    
    # Or use individual components
    welcome = prompt_manager.get_welcome_message(has_document_context=True)
"""

from .prompt_manager import (
    prompt_manager,
    get_instructions,
    get_welcome_message,
    get_skill_assessment_message,
    get_feedback_template,
    build_conversation_prompt,
    build_feedback_prompt,
    build_hsf_feedback_prompt,
    build_hsf_scenario_prompt,
    SCENARIO_TEMPLATES,
    SCORING_MATRIX,
    REAL_TIME_COACHING,
    INDUSTRY_ADAPTATIONS,
    calculate_skill_score,
    format_feedback_response,
    track_performance,
    get_skill_trends
)

# Backward compatibility - import everything that was in the original prompts.py
from .core_instructions import INSTRUCTIONS, WELCOME_MESSAGE, WELCOME_WITH_CONTEXT
from .scenarios import generate_scenario_prompt, select_appropriate_scenario, SCENARIO_TEMPLATES as SCENARIO_TEMPLATES_DIRECT
from .feedback import generate_skill_assessment_message as SKILL_ASSESSMENT_MESSAGE, SCORING_MATRIX as SCORING_MATRIX_DIRECT, REAL_TIME_COACHING as REAL_TIME_COACHING_DIRECT
from .content_processing import process_learning_material as CONTENT_PROCESSOR, process_multimodal_content as MULTIMODAL_PROCESSOR

# For legacy code that might import specific functions
def PROVIDE_FEEDBACK(interaction, skill_focus, performance_criteria):
    """Legacy function for backward compatibility"""
    return get_feedback_template(interaction, skill_focus, performance_criteria)

def LEARNING_PATHWAY(skills_assessment, user_goals):
    """Legacy function for backward compatibility"""
    from .state_management import generate_learning_pathway
    return generate_learning_pathway(skills_assessment, user_goals)

__all__ = [
    'prompt_manager',
    'get_instructions', 
    'get_welcome_message',
    'get_skill_assessment_message',
    'get_feedback_template',
    'build_conversation_prompt',
    'build_feedback_prompt',
    'build_hsf_feedback_prompt',
    'build_hsf_scenario_prompt',
    'INSTRUCTIONS',
    'WELCOME_MESSAGE',
    'WELCOME_WITH_CONTEXT',
    'SCENARIO_TEMPLATES',
    'SCENARIO_TEMPLATES_DIRECT',
    'SCORING_MATRIX',
    'SCORING_MATRIX_DIRECT',
    'REAL_TIME_COACHING',
    'REAL_TIME_COACHING_DIRECT',
    'INDUSTRY_ADAPTATIONS',
    'calculate_skill_score',
    'format_feedback_response',
    'track_performance',
    'get_skill_trends',
    'SKILL_ASSESSMENT_MESSAGE',
    'PROVIDE_FEEDBACK',
    'LEARNING_PATHWAY',
    'CONTENT_PROCESSOR',
    'MULTIMODAL_PROCESSOR',
    'generate_scenario_prompt',
    'select_appropriate_scenario'
]

# Also make direct imports available without _DIRECT suffix for tests
SCENARIO_TEMPLATES = SCENARIO_TEMPLATES if 'SCENARIO_TEMPLATES' in locals() else SCENARIO_TEMPLATES_DIRECT
SCORING_MATRIX = SCORING_MATRIX if 'SCORING_MATRIX' in locals() else SCORING_MATRIX_DIRECT  
REAL_TIME_COACHING = REAL_TIME_COACHING if 'REAL_TIME_COACHING' in locals() else REAL_TIME_COACHING_DIRECT
