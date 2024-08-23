import os
import shutil
from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import HTMLResponse, JSONResponse
from nsaqa import main as nsaqa_main


app = FastAPI()

SAVE_DIR = "/root/Sports-Police/NSAQA/sources"
REPORT_DIR = "/root/Sports-Police/NSAQA/output"


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):

    try:
        
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        video_path = os.path.join(SAVE_DIR, file.filename)
        
        # save uploaded video to model server
        with open(video_path, "wb") as video_file:
            shutil.copyfileobj(file.file, video_file)
        
        # run NSAQA
        html_id, save_path_html, summary_html_id, save_path_summary_html = nsaqa_main(video_path)
        print("NSAQA done")
        print(f"save_path_html: {save_path_html}")
        print(f"save_path_summary_html: {save_path_summary_html}")
        print(f"Type of html_id: {type(html_id)}")
        print("-"*80)
        
        # Sanity check and Open result files
        if not os.path.exists(save_path_html) or not os.path.exists(save_path_summary_html):
            raise HTTPException(status_code=500, detail="Report generation failed")

        
        with open(save_path_html, "r") as report_file:
            gpt_html = report_file.read()
        
        with open(save_path_summary_html, "r") as summary_file:
            html_content = summary_file.read()
        
        
        return JSONResponse(
            content={
                "document_id" : html_id, # RAG DB flag
                "html_content" : html_content, # for user
                "gpt_html" : gpt_html # RAG DB input
            }
        )
        
        
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
