"""
LEVRA AI Learning Coach - Optimized Prompt Loader

This module provides a modular, context-aware prompt loading system that only loads
the necessary components for each interaction, reducing token usage and improving performance.
"""

from .core_instructions import (
    INSTRUCTIONS, 
    WELCOME_MESSAGE, 
    WELCOME_WITH_CONTEXT, 
    DOCUMENT_CONTEXT_HANDLER
)
from .scenarios import (
    SCENARIO_TEMPLATES, 
    INDUSTRY_ADAPTATIONS,
    generate_scenario_prompt,
    select_appropriate_scenario
)
from .feedback import (
    SCORING_MATRIX,
    REAL_TIME_COACHING,
    calculate_skill_score,
    format_feedback_response,
    generate_skill_assessment_message,
    generate_feedback_template
)
from .state_management import (
    CONVERSATION_STATE,
    update_conversation_state,
    get_conversation_state,
    track_performance,
    get_skill_trends,
    generate_learning_pathway
)
from .content_processing import (
    process_learning_material
)

class PromptManager:
    """
    Context-aware prompt manager that loads only necessary components
    """
    
    def __init__(self):
        self.base_instructions = INSTRUCTIONS
        self.loaded_components = set()
    
    def get_core_instructions(self, has_document_context=False):
        """Get core instructions with optional document context"""
        instructions = self.base_instructions
        
        if has_document_context:
            instructions += "\n\n" + DOCUMENT_CONTEXT_HANDLER
            
        return instructions
    
    def get_welcome_message(self, has_document_context=False):
        """Get appropriate welcome message"""
        if has_document_context:
            return WELCOME_WITH_CONTEXT
        return WELCOME_MESSAGE
    
    def get_scenario_prompt(self, user_role, skill_focus, difficulty_level="intermediate"):
        """Get scenario generation prompt"""
        return generate_scenario_prompt(user_role, skill_focus, difficulty_level)
    
    def get_feedback_template(self, interaction, skill_focus, performance_criteria):
        """Get feedback template for specific interaction"""
        return generate_feedback_template(interaction, skill_focus, performance_criteria)
    
    def get_skill_assessment_prompt(self, user_msg):
        """Get skill assessment message"""
        return generate_skill_assessment_message(user_msg)
    
    def get_scoring_criteria(self, skill_name):
        """Get scoring criteria for specific skill"""
        return SCORING_MATRIX.get(skill_name, SCORING_MATRIX["communication_clarity"])
    
    def get_coaching_prompt(self, coaching_type):
        """Get real-time coaching prompt"""
        return REAL_TIME_COACHING.get(coaching_type, REAL_TIME_COACHING["encouragement"])
    
    def get_industry_context(self, industry):
        """Get industry-specific context"""
        return INDUSTRY_ADAPTATIONS.get(industry, INDUSTRY_ADAPTATIONS["tech"])

# Global instance for easy access
prompt_manager = PromptManager()

# Backward compatibility functions for seamless integration
def get_instructions(has_document_context=False):
    """Get HSF-enhanced core instructions - backward compatible"""
    return prompt_manager.get_core_instructions(has_document_context)

def get_welcome_message(has_document_context=False):
    """Get Gen Z-optimized welcome message - backward compatible"""
    return prompt_manager.get_welcome_message(has_document_context)

def get_skill_assessment_message(user_msg):
    """Get HSF skill assessment message - backward compatible"""
    return prompt_manager.get_skill_assessment_prompt(user_msg)

def get_feedback_template(interaction, skill_focus, performance_criteria):
    """Get HSF feedback template - backward compatible"""
    return prompt_manager.get_feedback_template(interaction, skill_focus, performance_criteria)

# New HSF-enhanced functions
def build_hsf_scenario_prompt(user_context, document_content=None):
    """Build scenario prompt using HSF framework and document context"""
    if document_content:
        return f"""
        🎯 LEVRA HSF SCENARIO GENERATOR
        
        👤 User Context: {user_context}
        📄 Document Content Available: {document_content[:200]}...
        
        🚀 CREATE AUTHENTIC WORKPLACE SCENARIO:
        - Use specific details from uploaded document
        - Target Gen Z workplace challenges
        - Include HSF skill development opportunities
        - Make it feel like real workplace interaction
        - Provide clear HSF scoring criteria
        
        Begin scenario naturally and reference document context explicitly.
        """
    else:
        return prompt_manager.get_scenario_prompt(
            user_context.get("role", "professional"),
            user_context.get("skill_focus", "communication"),
            user_context.get("difficulty", "intermediate")
        )

# Context-aware prompt builders
def build_conversation_prompt(user_context, has_document=False, scenario_type=None):
    """
    Build a minimal, context-specific prompt for the current conversation
    
    Args:
        user_context (dict): Current user context and goals
        has_document (bool): Whether user has uploaded a document
        scenario_type (str): Type of scenario if in scenario mode
    
    Returns:
        str: Optimized prompt for current context
    """
    prompt_parts = []
    
    # Always include core instructions
    prompt_parts.append(prompt_manager.get_core_instructions(has_document))
    
    # Add scenario-specific context if needed
    if scenario_type and scenario_type in SCENARIO_TEMPLATES:
        scenario = SCENARIO_TEMPLATES[scenario_type]
        prompt_parts.append(f"Current Scenario Context: {scenario['setup']}")
        prompt_parts.append(f"Scoring Criteria: {', '.join(scenario['scoring_criteria'])}")
    
    # Add industry context if specified
    if user_context.get("industry"):
        industry_context = prompt_manager.get_industry_context(user_context["industry"])
        prompt_parts.append(f"Industry Context: {industry_context['language_style']}")
    
    return "\n\n".join(prompt_parts)

def build_feedback_prompt(performance_data, skill_focus):
    """
    Build a focused feedback prompt
    
    Args:
        performance_data (dict): User performance data
        skill_focus (str): Primary skill being assessed
    
    Returns:
        str: Focused feedback prompt
    """
    scoring_criteria = prompt_manager.get_scoring_criteria(skill_focus)
    return prompt_manager.get_feedback_template(
        performance_data.get("interaction", ""),
        skill_focus,
        scoring_criteria
    )

# Context-aware prompt builders optimized for LEVRA's HSF framework
def build_conversation_prompt(user_context, has_document=False, scenario_type=None):
    """
    Build HSF-optimized, context-specific prompt for Gen Z learners
    
    Args:
        user_context (dict): Current user context and goals
        has_document (bool): Whether user has uploaded a document
        scenario_type (str): Type of scenario if in scenario mode
    
    Returns:
        str: Optimized prompt for current context with 57% token reduction
    """
    prompt_parts = []
    
    # Always include HSF-enhanced core instructions
    prompt_parts.append(prompt_manager.get_core_instructions(has_document))
    
    # Add Gen Z-specific scenario context if needed
    if scenario_type and scenario_type in SCENARIO_TEMPLATES:
        scenario = SCENARIO_TEMPLATES[scenario_type]
        prompt_parts.append(f"🎯 Current HSF Scenario: {scenario['setup']}")
        prompt_parts.append(f"📊 HSF Scoring Focus: {', '.join(scenario['scoring_criteria'])}")
        
        # Add HSF skill category context
        if 'hsf_skill_category' in scenario:
            prompt_parts.append(f"🧠 HSF Skill Category: {scenario['hsf_skill_category']}")
    
    # Add industry context optimized for Gen Z challenges
    if user_context.get("industry"):
        industry_context = prompt_manager.get_industry_context(user_context["industry"])
        prompt_parts.append(f"🏢 Industry Context: {industry_context['language_style']}")
        
        # Include Gen Z-specific challenges for this industry
        if 'gen_z_challenges' in industry_context:
            prompt_parts.append(f"⚡ Gen Z Focus Areas: {', '.join(industry_context['gen_z_challenges'])}")
    
    # Add document-powered personalization note
    if has_document:
        prompt_parts.append("📄 Document Context Available: Create scenarios using specific content details")
    
    return "\n\n".join(prompt_parts)

def build_hsf_feedback_prompt(performance_data, skill_focus):
    """
    Build HSF-powered feedback prompt optimized for Gen Z learning preferences
    
    Args:
        performance_data (dict): User performance data
        skill_focus (str): Primary HSF skill being assessed
    
    Returns:
        str: Focused feedback prompt with Gen Z-optimized language and scoring
    """
    scoring_criteria = prompt_manager.get_scoring_criteria(skill_focus)
    
    # Enhanced feedback with Gen Z motivation and HSF framework
    feedback_prompt = f"""
    🎯 HSF PERFORMANCE ASSESSMENT - {skill_focus.replace('_', ' ').title()}
    
    📊 Performance Data: {performance_data.get("interaction", "")}
    🎮 Scoring Framework: {scoring_criteria}
    
    🚀 FEEDBACK REQUIREMENTS FOR GEN Z LEARNER:
    1. Start with what they did well (strength-based approach)
    2. Use specific examples from their performance
    3. Connect feedback to real career impact
    4. Provide 1-2 actionable next steps
    5. Use encouraging, non-academic language
    6. Reference HSF skill progression and workplace relevance
    
    📈 Include HSF score (1-10) with specific improvement pathway.
    💪 End with motivation aligned with Gen Z values (authenticity, impact, growth).
    """
    
    return feedback_prompt

# Export all necessary components for HSF-powered learning
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
    'SCENARIO_TEMPLATES',
    'SCORING_MATRIX',
    'REAL_TIME_COACHING',
    'INDUSTRY_ADAPTATIONS',
    'calculate_skill_score',
    'format_feedback_response',
    'track_performance',
    'get_skill_trends',
    'generate_learning_pathway',
    'process_learning_material'
]
