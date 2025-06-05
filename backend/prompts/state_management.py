"""
LEVRA AI Learning Coach - State Management Module

This module handles conversation state and performance tracking.
"""

"""
LEVRA AI Learning Coach - HSF-Powered State Management Module

Continuous skills tracking and adaptive learning pathways designed for Gen Z learners,
supporting LEVRA's mission to close the £6.9T global human skills gap.
"""

# HSF-enhanced conversation state for personalized Gen Z learning journeys
CONVERSATION_STATE = {
    "current_scenario": None,
    "user_context": {
        "generation": "gen_z",
        "learning_preferences": ["interactive", "bite_sized", "authentic", "purpose_driven"],
        "industry": None,
        "role": None,
        "skill_gaps": [],
        "document_context": None
    },
    "performance_history": [],
    "hsf_skill_profile": {
        "communication_clarity": {"current_level": 0, "target_level": 8, "trend": "baseline"},
        "digital_leadership": {"current_level": 0, "target_level": 8, "trend": "baseline"},
        "generational_bridge_building": {"current_level": 0, "target_level": 8, "trend": "baseline"},
        "purpose_driven_communication": {"current_level": 0, "target_level": 8, "trend": "baseline"},
        "cultural_intelligence": {"current_level": 0, "target_level": 8, "trend": "baseline"},
        "emotional_intelligence": {"current_level": 0, "target_level": 8, "trend": "baseline"},
        "future_ready_mindset": {"current_level": 0, "target_level": 8, "trend": "baseline"}
    },
    "learning_pathway": {
        "current_module": "assessment",
        "completed_scenarios": [],
        "next_recommended_skills": [],
        "engagement_score": 10  # Start high for Gen Z motivation
    },
    "session_goals": [],
    "document_integration": {
        "has_uploaded_content": False,
        "content_type": None,
        "scenarios_generated": 0,
        "personalization_level": "basic"
    }
}

def update_conversation_state(key, value):
    """Update conversation state for adaptive learning"""
    CONVERSATION_STATE[key] = value

def get_conversation_state(key):
    """Retrieve conversation state value"""
    return CONVERSATION_STATE.get(key, None)

def track_performance(scenario_name, skill_scores):
    """Track scenario performance with Gen Z engagement metrics"""
    state = CONVERSATION_STATE
    
    # Update skill levels and calculate avg improvement
    total_improvement = 0
    improvements = 0
    
    for skill, score in skill_scores.items():
        if skill in state["hsf_skill_profile"]:
            current = state["hsf_skill_profile"][skill]["current_level"]
            # Calculate improvement
            if score > current:
                total_improvement += (score - current)
                improvements += 1
            state["hsf_skill_profile"][skill]["current_level"] = score
            state["hsf_skill_profile"][skill]["trend"] = "improving" if score > current else "maintaining"
    
    # Calculate dynamic engagement factors based on actual performance
    avg_score = sum(skill_scores.values()) / len(skill_scores) if skill_scores else 0
    avg_improvement = total_improvement / improvements if improvements > 0 else 0
    
    engagement_factors = {
        "authenticity": skill_scores.get("purpose_driven_communication", avg_score),
        "digital_fluency": skill_scores.get("digital_leadership", avg_score),
        "purpose_alignment": skill_scores.get("cultural_intelligence", avg_score),
        "psychological_safety": skill_scores.get("emotional_intelligence", avg_score),
        "improvement_trend": avg_improvement
    }
    
    # Update performance history
    performance_entry = {
        "scenario": scenario_name,
        "skill_scores": skill_scores,
        "timestamp": "2025-06-06",  # Current date
        "gen_z_engagement_factors": engagement_factors
    }
    
    state["performance_history"].append(performance_entry)
    return performance_entry

def get_skill_trends(skill_name):
    """Get Gen Z-optimized skill development trends"""
    state = CONVERSATION_STATE
    skill_data = state["hsf_skill_profile"].get(skill_name, {})
    
    emojis = {
        "improving": "🚀",
        "maintaining": "💪",
        "baseline": "📈"
    }
    
    trend = skill_data.get("trend", "baseline")
    emoji = emojis.get(trend, "📈")
    
    trend_message = {
        "message": f"{emoji} Your {skill_name.replace('_', ' ')} is {trend}! Keep crushing it! {emojis['improving']}",
        "current_level": skill_data.get("current_level", 0),
        "target_level": skill_data.get("target_level", 8),
        "trend": trend
    }
    
    return trend_message

def get_gen_z_performance_insights(scenario_type=None):
    """Get Gen Z-specific performance insights with optional scenario filtering"""
    state = CONVERSATION_STATE
    history = state["performance_history"]
    
    # Filter by scenario type if provided
    if scenario_type:
        history = [entry for entry in history if entry["scenario"] == scenario_type]
    
    if not history:
        return {
            "trends": "No performance data available yet",
            "engagement_level": "baseline",
            "recommendations": ["Start with an initial assessment"]
        }
    
    # Calculate average scores and engagement
    avg_scores = {}
    total_engagement = 0
    
    for entry in history:
        # Aggregate skill scores
        for skill, score in entry["skill_scores"].items():
            if skill not in avg_scores:
                avg_scores[skill] = []
            avg_scores[skill].append(score)
        
        # Sum up engagement factors
        engagement_factors = entry["gen_z_engagement_factors"]
        total_engagement += sum(engagement_factors.values()) / len(engagement_factors)
    
    # Calculate final averages
    avg_engagement = total_engagement / len(history)
    skill_averages = {
        skill: sum(scores) / len(scores)
        for skill, scores in avg_scores.items()
    }
    
    return {
        "trends": {
            "skill_averages": skill_averages,
            "engagement_trend": "improving" if avg_engagement > 7.5 else "maintaining"
        },
        "engagement_level": "high" if avg_engagement > 8.5 else "medium" if avg_engagement > 7 else "needs_attention",
        "recommendations": _generate_engagement_recommendations(skill_averages, avg_engagement)
    }

def update_skill_profile(skill_name, new_score):
    """Update HSF skill profile with new performance data"""
    profile = CONVERSATION_STATE["hsf_skill_profile"]
    if skill_name in profile:
        old_level = profile[skill_name]["current_level"]
        profile[skill_name]["current_level"] = new_score
        profile[skill_name]["trend"] = "improving" if new_score > old_level else "maintaining"
    return profile

# Learning pathway generator for continuous skill development
def generate_learning_pathway(user_context, hsf_profile):
    """Generate personalized learning pathway optimized for Gen Z engagement"""
    
    # Identify skill gaps (where current_level < target_level)
    skill_gaps = []
    for skill, data in hsf_profile.items():
        gap_size = data["target_level"] - data["current_level"]
        if gap_size > 2:
            skill_gaps.append({"skill": skill, "gap": gap_size, "priority": "high"})
        elif gap_size > 0:
            skill_gaps.append({"skill": skill, "gap": gap_size, "priority": "medium"})
    
    # Sort by gap size for priority
    skill_gaps.sort(key=lambda x: x["gap"], reverse=True)
    
    # Generate Gen Z-optimized learning pathway
    pathway = {
        "next_focus_skill": skill_gaps[0]["skill"] if skill_gaps else "communication_clarity",
        "recommended_scenarios": _get_gen_z_scenarios_for_skill(skill_gaps[0]["skill"] if skill_gaps else "communication_clarity"),
        "motivation_message": _generate_motivation_message(skill_gaps, user_context),
        "estimated_sessions": len(skill_gaps) * 2,  # 2 sessions per skill gap
        "gamification_elements": {
            "current_streak": 1,
            "skills_mastered": len([s for s in hsf_profile.values() if s["current_level"] >= s["target_level"]]),
            "next_achievement": "First Skill Mastery" if all(s["current_level"] < s["target_level"] for s in hsf_profile.values()) else "Multi-Skill Expert"
        }
    }
    
    return pathway

def _get_gen_z_scenarios_for_skill(skill_name):
    """Map HSF skills to Gen Z-relevant scenarios"""
    scenario_mapping = {
        "communication_clarity": ["gen_z_leadership_emergence", "remote_team_connection"],
        "digital_leadership": ["remote_team_connection", "ai_ethics_workplace_discussion"],
        "generational_bridge_building": ["gen_z_leadership_emergence", "cultural_fluency_global_team"],
        "purpose_driven_communication": ["social_impact_business_case", "ai_ethics_workplace_discussion"],
        "cultural_intelligence": ["cultural_fluency_global_team", "remote_team_connection"],
        "emotional_intelligence": ["mental_health_workplace_conversation", "remote_team_connection"],
        "future_ready_mindset": ["ai_ethics_workplace_discussion", "social_impact_business_case"]
    }
    
    return scenario_mapping.get(skill_name, ["gen_z_leadership_emergence"])

def _generate_motivation_message(skill_gaps, user_context):
    """Generate motivational message aligned with Gen Z values"""
    if not skill_gaps:
        return "🎉 You're absolutely killing it! All your HSF skills are at target levels. Ready to become a mentor?"
    
    top_skill = skill_gaps[0]["skill"].replace("_", " ").title()
    industry = user_context.get("industry", "your field")
    
    messages = [
        f"💪 Ready to level up your {top_skill}? This is exactly what will set you apart in {industry}!",
        f"🚀 Your {top_skill} development is going to be a game-changer for your career impact!",
        f"✨ Mastering {top_skill} will help you bridge generational gaps and lead with authenticity!",
        f"🎯 Focus on {top_skill} and you'll see immediate results in your workplace interactions!"
    ]
    
    # Simple selection based on skill type
    return messages[0]  # Could be enhanced with more sophisticated selection logic

def generate_learning_pathway(skills_assessment, user_goals):
    """Generate personalized learning pathway based on assessment results"""
    return f"""
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

def _generate_engagement_recommendations(skill_averages, avg_engagement):
    """Generate tailored recommendations based on skill averages and engagement"""
    recommendations = []
    
    # Engagement-based recommendations
    if avg_engagement < 7:
        recommendations.extend([
            "Try more interactive scenarios",
            "Set shorter, more focused learning sessions",
            "Connect skills to real-world impact"
        ])
    elif avg_engagement < 8.5:
        recommendations.extend([
            "Challenge yourself with advanced scenarios",
            "Share your progress with peers",
            "Explore leadership opportunities"
        ])
    else:
        recommendations.extend([
            "Mentor others in your strongest skills",
            "Create custom scenarios",
            "Lead group learning sessions"
        ])
    
    # Skill-based recommendations
    lowest_skill = min(skill_averages.items(), key=lambda x: x[1])
    if lowest_skill[1] < 7:
        recommendations.append(f"Focus on improving {lowest_skill[0].replace('_', ' ')}")
    
    return recommendations
