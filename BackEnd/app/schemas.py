from pydantic import BaseModel

class YouTubeLink(BaseModel):
    url: str
    start_time: str
    end_time: str
    gt_score: float

class AnalysisResult(BaseModel):
    gt_score: float
    report: bytes # html report of model output


class QAResults(BaseModel):
    answer: str
