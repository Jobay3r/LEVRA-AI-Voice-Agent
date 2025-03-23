import enum
from typing import Annotated, Dict, Any
import logging
from livekit import agents
from livekit.agents import llm  # Correct import for FunctionContext
from db_driver import DB

logger = logging.getLogger(__name__)

class ProfileDetails(enum.Enum):
    ID = "id"
    DreamJob = "dream_job"
    CurrentSkills = "current_skills"
    Education = "education"
    
class CareerSkills(enum.Enum):
    COMMUNICATION = "communication"
    LEADERSHIP = "leadership"
    TEAMWORK = "teamwork"
    PROBLEM_SOLVING = "problem_solving"
    ADAPTABILITY = "adaptability"
    TIME_MANAGEMENT = "time_management"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    CRITICAL_THINKING = "critical_thinking"

class AssistantFnc(llm.FunctionContext):  # Now this should work with the correct import
    def __init__(self):
        # Call the parent class's __init__ method to properly initialize _fncs
        super().__init__()
        
        self._profile_details = {
            ProfileDetails.ID: "",
            ProfileDetails.DreamJob: "",
            ProfileDetails.CurrentSkills: "",
            ProfileDetails.Education: ""
        }
        self._recommended_skills = []
        
    def get_profile_str(self):
        if not self.has_profile():
            return "No profile available"
        
        return f"User with ID {self._profile_details[ProfileDetails.ID]} " \
               f"has a dream job as {self._profile_details[ProfileDetails.DreamJob]}, " \
               f"with skills in {self._profile_details[ProfileDetails.CurrentSkills]}, " \
               f"and educational background: {self._profile_details[ProfileDetails.Education]}."
    
    @llm.ai_callable(description="lookup a career profile by ID")
    def lookup_profile(self, id: Annotated[str, llm.TypeInfo(description="The ID of the user to lookup")]):
        logger.info("lookup profile - id: %s", id)
        
        result = DB.get_profile_by_id(id)
        if result is None:
            return "Profile not found"
        
        self._profile_details = {
            ProfileDetails.ID: result.id,
            ProfileDetails.DreamJob: result.dream_job,
            ProfileDetails.CurrentSkills: result.current_skills,
            ProfileDetails.Education: result.education
        }
        
        return f"The profile details are: {self.get_profile_str()}"
    
    @llm.ai_callable(description="get the details of the current profile")
    def get_profile_details(self):
        if not self.has_profile():
            return "No profile available"
        
        return self.get_profile_str()
    
    @llm.ai_callable(description="create a new career profile")
    def create_profile(
        self, 
        id: Annotated[str, llm.TypeInfo(description="The unique ID for the user")],
        dream_job: Annotated[str, llm.TypeInfo(description="The user's dream job or career aspiration")],
        current_skills: Annotated[str, llm.TypeInfo(description="The user's current skills")],
        education: Annotated[str, llm.TypeInfo(description="The user's educational background")]
    ):
        logger.info("create profile - id: %s, dream_job: %s, current_skills: %s, education: %s", 
                   id, dream_job, current_skills, education)
        
        result = DB.create_career_profile(id, dream_job, current_skills, education)
        if result is None:
            return "Failed to create profile"
        
        self._profile_details = {
            ProfileDetails.ID: result.id,
            ProfileDetails.DreamJob: result.dream_job,
            ProfileDetails.CurrentSkills: result.current_skills,
            ProfileDetails.Education: result.education
        }
        
        return f"Successfully created profile for {id} with dream job: {dream_job}"
    
    @llm.ai_callable(description="identify recommended skills for dream job")
    def recommend_skills(
        self,
        skills: Annotated[list[str], llm.TypeInfo(description="List of soft skills recommended for the dream job")]
    ):
        if not self.has_profile():
            return "No profile available to recommend skills for"
        
        self._recommended_skills = skills
        
        skills_str = ", ".join(skills)
        return f"Based on the dream job of {self._profile_details[ProfileDetails.DreamJob]}, " \
               f"the following skills are recommended: {skills_str}"
    
    @llm.ai_callable(description="provide suggestions for developing specific skills")
    def get_skill_suggestions(
        self,
        skill: Annotated[str, llm.TypeInfo(description="The specific skill to get suggestions for")]
    ):
        if not self.has_profile():
            return "No profile available"
        
        dream_job = self._profile_details[ProfileDetails.DreamJob]
        
        # Here we would normally do database lookup for suggestions
        # For now, returning placeholders
        suggestions = {
            "communication": {
                "importance": f"Strong communication is crucial for success as a {dream_job}",
                "exercise": "Practice public speaking by recording yourself explaining complex topics simply",
                "resource": "Book: 'Crucial Conversations' by Kerry Patterson"
            },
            "leadership": {
                "importance": f"Leadership skills help you advance in your {dream_job} career",
                "exercise": "Take initiative on a small project and practice delegating tasks",
                "resource": "Course: Leadership Fundamentals on Coursera"
            },
            "teamwork": {
                "importance": f"Collaboration is key in most {dream_job} environments",
                "exercise": "Join a community project requiring coordination with others",
                "resource": "Book: 'The Five Dysfunctions of a Team' by Patrick Lencioni"
            },
            "problem_solving": {
                "importance": f"Problem-solving is a daily requirement in {dream_job} roles",
                "exercise": "Practice the IDEAL method (Identify, Define, Explore, Act, Look back) with real issues",
                "resource": "Website: Practice puzzles on Brilliant.org"
            }
        }
        
        skill_lower = skill.lower()
        if skill_lower in suggestions:
            skill_info = suggestions[skill_lower]
            return f"SKILL: {skill.upper()}\n" \
                   f"Importance: {skill_info['importance']}\n" \
                   f"Exercise: {skill_info['exercise']}\n" \
                   f"Resource: {skill_info['resource']}"
        else:
            return f"I don't have specific suggestions for {skill} yet, but I can help you research development methods."
    
    def has_profile(self):
        return self._profile_details[ProfileDetails.ID] != ""