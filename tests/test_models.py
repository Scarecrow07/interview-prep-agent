"""Pydantic 数据模型单元测试"""

from src.models.jd_analysis import JDAnalysis, TechnologyRequirement, ExperienceRequirement
from src.models.gap_analysis import GapAnalysis, SkillMatchItem, ResumeSummary
from src.models.self_intro import SelfIntroScript, SelfIntroductionVersion
from src.models.question_bank import QuestionBank, InterviewQuestion
from src.models.coding_problem import CodingProblemSet, CodingProblem
from src.models.learning_resource import LearningResources, LearningResource
from src.models.input_schema import InterviewPrepInput

import pytest


class TestJDAnalysis:
    def test_minimal_jd(self):
        """测试最小 JD 分析模型"""
        data = {
            "position_title": "Python工程师",
            "summary": "核心摘要",
            "core_responsibilities": ["负责后端开发"],
            "hard_skills": [
                {
                    "tech_name": "Python",
                    "proficiency_level": "精通",
                    "is_required": True,
                    "reason_from_jd": "JD中明确要求精通Python",
                }
            ],
            "soft_skills": [
                {"skill_name": "沟通能力", "context": "跨团队协作"}
            ],
            "experience_requirement": {
                "min_years": 3,
                "preferred_industry": ["互联网"],
            },
            "role_level": "高级",
            "key_evaluation_criteria": ["技术深度", "项目经验"],
        }
        model = JDAnalysis(**data)
        assert model.position_title == "Python工程师"
        assert model.experience_requirement.min_years == 3
        assert len(model.hard_skills) == 1
        assert model.hard_skills[0].tech_name == "Python"

    def test_jd_optional_fields(self):
        """测试可选字段为 None 的情况"""
        data = {
            "position_title": "工程师",
            "summary": "摘要",
            "core_responsibilities": ["开发"],
            "hard_skills": [],
            "soft_skills": [],
            "experience_requirement": {
                "min_years": 0,
                "preferred_industry": [],
            },
            "role_level": "初中级",
            "key_evaluation_criteria": ["技术"],
        }
        model = JDAnalysis(**data)
        assert model.company_industry is None
        assert model.education_requirement is None


class TestGapAnalysis:
    def test_minimal_gap(self):
        data = {
            "resume_summary": {
                "years_of_experience": 5,
                "current_role": "后端开发",
                "notable_projects": ["电商平台"],
            },
            "overall_match_score": 75,
            "skill_match_details": [
                {
                    "skill_name": "Python",
                    "skill_type": "tech",
                    "requirement_level": "精通",
                    "match_status": "matched",
                    "priority": 3,
                }
            ],
            "strengths": ["Python精通"],
            "top_gaps": ["Kubernetes不熟悉"],
            "risk_areas": ["系统设计"],
            "preparation_strategy": "重点准备系统设计",
        }
        model = GapAnalysis(**data)
        assert model.overall_match_score == 75
        assert len(model.strengths) == 1

    def test_match_score_range(self):
        with pytest.raises(Exception):
            GapAnalysis(
                resume_summary={
                    "years_of_experience": 0,
                    "notable_projects": [],
                },
                overall_match_score=150,  # 超范围
                skill_match_details=[],
                strengths=[],
                top_gaps=[],
                risk_areas=[],
                preparation_strategy="",
            )


class TestQuestionBank:
    def test_minimal_qa(self):
        data = {
            "total_questions": 10,
            "questions": [
                {
                    "question_number": 1,
                    "category": "tech_deep_dive",
                    "difficulty": "medium",
                    "question_text": "请解释Python的GIL",
                    "evaluation_dimension": "技术深度",
                    "reference_answer_key_points": ["GIL是全局解释器锁"],
                    "suggested_time_limit": "2分钟",
                }
                for _ in range(10)
            ],
            "focus_areas_advice": "重点准备Python",
        }
        model = QuestionBank(**data)
        assert model.total_questions == 10
        assert len(model.questions) == 10


class TestInputSchema:
    def test_valid_input(self):
        model = InterviewPrepInput(
            jd_text="a" * 50,
            resume_text="b" * 50,
        )
        assert model.job_type_hint == "unknown"

    def test_short_input_fails(self):
        with pytest.raises(Exception):
            InterviewPrepInput(
                jd_text="too short",
                resume_text="also short",
            )


class TestSelfIntro:
    def test_minimal(self):
        data = {
            "versions": [
                {
                    "duration": "1min",
                    "target_scenario": "一面",
                    "script": "大家好...",
                    "key_highlights": ["Python经验"],
                },
                {
                    "duration": "2min",
                    "target_scenario": "技术面",
                    "script": "大家好...",
                    "key_highlights": ["项目经验"],
                },
            ],
            "usage_tips": ["语速适中"],
            "common_mistakes_to_avoid": ["不要背稿"],
        }
        model = SelfIntroScript(**data)
        assert len(model.versions) == 2


class TestCodingProblem:
    def test_minimal(self):
        data = {
            "total_problems": 3,
            "language_recommendation": "Python",
            "problems": [
                {
                    "problem_number": 1,
                    "title": "两数之和",
                    "difficulty": "easy",
                    "estimated_time": "15分钟",
                    "topic_tags": ["数组", "哈希表"],
                    "problem_description": "找出两数之和",
                    "examples": [{"input": "[1,2,3]", "output": "[0,1]"}],
                    "constraints": ["数组长度≤10^4"],
                    "hints": ["使用哈希表"],
                    "solution_approach": "哈希表法",
                    "reference_code_language": "Python",
                    "reference_code_snippet": "def two_sum(nums, target): ...",
                    "complexity_analysis": "O(n)",
                }
            ],
            "preparation_tips": "多刷LeetCode",
        }
        model = CodingProblemSet(**data)
        assert model.total_problems == 3


class TestLearningResource:
    def _make_resource(self, i: int) -> dict:
        return {
            "resource_type": "book",
            "title": f"学习资源{i}",
            "target_skill": "Python",
            "reason": "巩固基础",
            "priority": "high",
            "difficulty_level": "beginner",
        }

    def test_minimal(self):
        data = {
            "resources": [self._make_resource(i) for i in range(5)],
            "study_plan_summary": "3天计划",
            "key_knowledge_points": ["Python基础"],
        }
        model = LearningResources(**data)
        assert len(model.resources) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])