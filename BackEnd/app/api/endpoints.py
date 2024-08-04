from fastapi import APIRouter, HTTPException
from app.schemas import YouTubeLink, AnalysisResult

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_youtube_video(youtube_link: YouTubeLink):
    try:
        # video_path: url로 다운받은 동영상 파일 경로
        # score, analysis_text: 모델 비디오 분석 결과
        # image_url: 모델 이미지 생성 결과
        
        score = 200
        image_url = "http://example.com/example-image.jpg"
        analysis_text = "Example"
        
        return AnalysisResult(
            score=score,
            image_url=image_url,
            text=analysis_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))