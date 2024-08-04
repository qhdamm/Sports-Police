from pydantic import BaseModel

class YouTubeLink(BaseModel):
    url: str

class AnalysisResult(BaseModel):
    score: int
    image_url: str
    text: str