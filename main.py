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
db_handler = ChromaDBHandler()
## pdf file -> db
pdf_path = './rag/data/Competition-Regulations.pdf'
store_pdf(pdf_path, db_handler)
## html file -> db
text_content = extract_text_from_html(html_content) 
text_content = preprocess_text(text_content) # 추가 
embedding = generate_embeddings(text_content)
db_handler.store_embedding(html_id, text_content, embedding)
print("Document stored successfully.")
# Example RAG Query
response = generate_response_with_rag("Explain the performance analysis.", db_handler)
print(f"Response: {response}")
if meta_program_args.html_info_delete:
    db_handler.delete_document(html_id)
    print("Document deleted successfully.")
