from pydantic import BaseModel

class YouTubeLink(BaseModel):
    url: str
    start_time: str
    end_time: str
    gt_score: float

class AnalysisResult(BaseModel):
    gt_score: float
    report: bytes # html report of model output
    document_id: str  # 문서 ID
    video_name: str

class QAInput(BaseModel):
    user_input: str
    document_id: str
    video_name: str

class QAResults(BaseModel):
    answer: str

class goHome(BaseModel):
    document_id: str
