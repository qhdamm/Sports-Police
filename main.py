import argparse
import pickle
import os
from dotenv import load_dotenv
import openai
import chromadb
from chromadb.config import Settings
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import re
import pandas as pd
from rag.rag_utils import *
from NSAQA.nsaqa import main as nsaqa_main



client = chromadb.PersistentClient()
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# 섹션 제목 리스트 정의
section_titles = [
    "GENERAL", "COMPETITIONS", "COMPETITION FORMAT", "STATEMENT OF DIVES",
    "COMPETITION PROCEDURE", "DUTIES OF THE REFEREE AND ASSISTANT REFEREES",
    "DUTIES OF THE SECRETARIAT", "JUDGING", 
    "REFEREEING AND JUDGING SYNCHRONISED DIVING",
    "SUMMARY OF THE PENALTIES", 
    "DIVING AT THE WORLD AQUATICS CHAMPIONSHIPS AND OLYMPIC GAMES",
    "AGE GROUP RULES - DIVING", "DIVING FACILITIES AND EQUIPMENT",
    "MEDICAL AND SAFETY SPECIFIC REQUIREMENT FOR DIVING"
]

pdf_path = './rag/data/Competition-Regulations.pdf'
sections = split_pdf_by_section_titles(pdf_path, section_titles)

# 텍스트 임베딩 생성
model = SentenceTransformer('all-MiniLM-L6-v2') # 임베딩 모델 로드

# PDF에서 추출한 텍스트 임베딩 생성
sections = split_pdf_by_section_titles(pdf_path, section_titles)
embeddings = model.encode(sections)

# 2. 고정 데이터: 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection("pdf_collection") # 고정 데이터 

# 임베딩된 텍스트를 컬렉션에 추가
for i, section in enumerate(sections):
    collection.add(
        documents=[section],
        embeddings=[embeddings[i].tolist()],  # 임베딩을 리스트로 변환
        ids=[f"pdf_section_{i}"]
    )
    


new_parser = argparse.ArgumentParser(description="Extract dive data to be used for scoring.")
new_parser.add_argument("video_path", type=str, help="Path to dive video (mp4 format).")
# difficulty 추가 부분
new_parser.add_argument("difficulty", type=float)
new_parser.add_argument("-d", "--html_info_delete", action="store_true")
meta_program_args = new_parser.parse_args()

video_path = meta_program_args.video_path
# difficulty 추가 부분
difficulty = meta_program_args.difficulty
html_id, save_path_html, summary_html_id, save_path_summary_html = nsaqa_main(video_path, difficulty)
with open(save_path_html, 'r') as file:
    html_content = file.read()

# Start RAG
text_content = extract_text_from_html(html_content)
embedding = generate_embeddings(text_content)
db_handler = ChromaDBHandler()
db_handler.store_embedding(document_id, text_content, embedding)
print("Document stored successfully.")
# Example RAG Query
response = generate_response_with_rag("Explain the performance analysis.", db_handler)
print(f"Response: {response}")
if meta_program_args.html_info_delete:
    db_handler.delete_document(document_id)
    print("Document deleted successfully.")
