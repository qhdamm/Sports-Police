import requests, os, sys
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.schemas import YouTubeLink, AnalysisResult, QAInput, QAResults, goHome
from app.process_video import download_clip

from dotenv import load_dotenv
import openai

sys.path.append('./app/api')
from rag_utils import *
import chromadb


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()
MODEL_SERVER_URL = "http://165.132.46.85:31260/upload"
base_path = "/Users/kjinh/Desktop/Sports-Police/BackEnd/html_output/"
pdf_path = '/Users/kjinh/Desktop/Sports-Police/BackEnd/app/api/Competition-Regulations.pdf'

client = chromadb.PersistentClient()
db_handler = ChromaDBHandler()
store_pdf(pdf_path, db_handler)



@router.post("/analyze", response_model=AnalysisResult)
async def analyze_youtube_video(youtube_link: YouTubeLink):
    try:
        # 1. 비디오 다운로드
        video_path = download_clip(youtube_link.url, youtube_link.start_time, youtube_link.end_time)

        # 2. 모델 서버로 비디오 파일 전송
        with open(video_path, "rb") as video_file:
            files = {'file': open(video_path, 'rb')}
            print("Sending video file to model server...")
            print("-"*80)
            response = requests.post(MODEL_SERVER_URL, files=files)
            print(f"Model server response: {response.status_code}")
            
        # 3. 모델 서버 응답 처리
        if response.status_code == 200:
            response_json = response.json()  # JSON 응답 파싱
            print("Successfully parsed JSON response.")
            
            document_id = response_json.get("document_id") # gpt_html_id
            model_report = response_json.get("html_content") # summary for user
            gpt_report = response_json.get("gpt_html") # html to gpt
            
            # HTML 파일 저장 (to Backend local, for QA)
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            save_path_html = base_path+f"{video_name}_{document_id}.html"
            
            with open(save_path_html, 'wb') as f:
                f.write(gpt_report.encode('utf-8'))
            
            print("HTML report for GPT input saved successfully.")
            



            return AnalysisResult(
                gt_score=youtube_link.gt_score,
                report=model_report.encode('utf-8'), # html for user
                document_id=document_id,  # html id for QA(GPT)
                video_name=video_name
            )

        else:
            raise HTTPException(status_code=500, detail="Model server error")
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/qa", response_model=QAResults)
async def qa_with_res(qa_input: QAInput):
    try:
        document_id = qa_input.document_id
        video_name = qa_input.video_name
        user_input = qa_input.user_input
        
        html_path = base_path+f"{video_name}_{document_id}.html" # summary 말고 전체 html report 의미
        with open(html_path, 'rb') as f:
            html_content = f.read()

        # 1. 해당 html에 대해 embedding이 존재하는지 확인
        if not db_handler.document_exists(document_id):
            text_content = extract_text_from_html(html_content)
            embedding = generate_embeddings(text_content)

            db_handler.store_embedding(document_id, text_content, embedding)
            print("Document stored successfully.")
        
        # RAG 모델 input
        response = generate_response_with_rag(user_input, db_handler)
        
        return QAResults(answer=response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/home")
async def reset_system(goHome: goHome):
    try:
        document_id = goHome.document_id
        # ChromaDB에서 문서 삭제
        db_handler.delete_document(document_id)
        print(f"Document with ID {document_id} deleted from ChromaDB.")

        # HTML 파일 삭제
        files = [f for f in os.listdir(base_path) if f"{document_id}" in f]
        for file in files:
            os.remove(os.path.join(base_path, file))
            print(f"Deleted HTML report: {file}")

        return {"message": "System reset successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset system: {str(e)}")
