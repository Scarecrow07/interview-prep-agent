from pydantic import BaseModel, Field
from typing import Optional


class InterviewPrepInput(BaseModel):
    """面试准备方案的输入"""
    jd_text: str = Field(
        min_length=50, max_length=50000,
        description="JD (职位描述) 文本",
    )
    resume_text: str = Field(
        min_length=50, max_length=50000,
        description="简历文本",
    )
    candidate_name: Optional[str] = Field(
        default=None,
        description="候选人姓名",
    )
    job_type_hint: Optional[str] = Field(
        description="岗位类型提示: tech / non_tech / unknown",
        default="unknown",
    )