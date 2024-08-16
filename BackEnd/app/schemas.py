from pydantic import BaseModel

class YouTubeLink(BaseModel):
    url: str
    gt_score: int

class AnalysisResult(BaseModel):
    report: bytes # html report of model output


class QAResults(BaseModel):
    answer: str
