"""数据模型导出"""

from .jd_analysis import JDAnalysis, TechnologyRequirement, ExperienceRequirement, SoftSkillRequirement
from .resume_analysis import ResumeAnalysis, WorkExperience, ProjectExperience, Education
from .gap_analysis import GapAnalysis, SkillMatchItem, ResumeSummary
from .self_intro import SelfIntroScript, SelfIntroductionVersion, SourceReference
from .project_intro import ProjectIntroSet, ProjectIntroDetail, ProjectSourceReference
from .question_bank import QuestionBank, InterviewQuestion, QuestionCategory, QuestionSourceReference, AnswerFramework
from .coding_problem import CodingProblemSet, CodingProblem, LeetCodeReference, ScoringCriteria
from .learning_resource import LearningResources, LearningResource
from .input_schema import InterviewPrepInput

__all__ = [
    # JD分析
    "JDAnalysis",
    "TechnologyRequirement",
    "ExperienceRequirement",
    "SoftSkillRequirement",
    
    # 简历分析
    "ResumeAnalysis",
    "WorkExperience",
    "ProjectExperience",
    "Education",
    
    # 匹配度分析
    "GapAnalysis",
    "SkillMatchItem",
    "ResumeSummary",
    
    # 自我介绍
    "SelfIntroScript",
    "SelfIntroductionVersion",
    "SourceReference",
    
    # 项目介绍
    "ProjectIntroSet",
    "ProjectIntroDetail",
    "ProjectSourceReference",
    
    # 面试问答
    "QuestionBank",
    "InterviewQuestion",
    "QuestionCategory",
    "QuestionSourceReference",
    "AnswerFramework",
    
    # 笔试题目
    "CodingProblemSet",
    "CodingProblem",
    "LeetCodeReference",
    "ScoringCriteria",
    
    # 学习资源
    "LearningResources",
    "LearningResource",
    
    # 输入
    "InterviewPrepInput",
]