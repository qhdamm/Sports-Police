# pip install chromadb
# pip install PyMuPDF
# pip install sentence-transformers

import chromadb
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import re
from html_preprocessing import extract_text_from_html, preprocess_text
import pandas as pd

client = chromadb.PersistentClient()

# 1. pdf 파일 -> 여러 섹션으로 분할
def split_pdf_by_section_titles(pdf_path, section_titles):
    # PDF에서 텍스트를 추출하고, 섹션 제목을 기준으로 섹션을 나누는 함수
    doc = fitz.open(pdf_path)
    sections = []
    current_section = ""
    section_found = False
    
    # 페이지별로 텍스트 추출 및 섹션 분할
    for page in doc:
        text = page.get_text()
        lines = text.split('\n')
        
        for line in lines:
            # 섹션 제목 탐지
            if line.strip() in section_titles:
                if section_found:  # 이전 섹션이 있다면 저장
                    sections.append(current_section.strip())
                    current_section = ""
                section_found = True
            current_section += line + "\n"
    
    # 마지막 섹션 추가
    if current_section:
        sections.append(current_section.strip())
    
    return sections

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

pdf_path = './data/Competition-Regulations.pdf'
sections = split_pdf_by_section_titles(pdf_path, section_titles)

# 텍스트 임베딩 생성
model = SentenceTransformer('all-MiniLM-L6-v2') # 임베딩 모델 로드

# PDF에서 추출한 텍스트 임베딩 생성
sections = split_pdf_by_section_titles(pdf_path, section_titles)
embeddings = model.encode(sections)

# -----------------------------------------------------------------------------------------------

# 2. 고정 데이터: 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection("pdf_collection") # 고정 데이터 

# 임베딩된 텍스트를 컬렉션에 추가
for i, section in enumerate(sections):
    collection.add(
        documents=[section],
        embeddings=[embeddings[i].tolist()],  # 임베딩을 리스트로 변환
        ids=[f"pdf_section_{i}"]
    )
    
# query_text = "What is the score criteria for diving?"
# query_embedding = model.encode([query_text])

# results = collection.query(
#     query_embeddings=query_embedding,
#     n_results=3  # 반환할 결과 수
# )


# -----------------------------------------------------------------------------------------------

html_file_path = './data/diving2_report.html'

# 3. html 파일에서 불필요한 내용 제거 
text = extract_text_from_html(html_file_path)
refined_text = preprocess_text(text)

text = refined_text
lines = text.strip().split('\n')  # Split the text by lines and remove unnecessary symbols
data = []
for line in lines:
    # Remove bullet points, asterisks, parentheses, and excess spaces
    line = re.sub(r'^-+', '', line).strip()  # Remove leading bullet points
    line = re.sub(r'\*\*', '', line)  # Remove bold asterisks
    line = re.sub(r'\(.*?\)', '', line)  # Remove parentheses and their content
    line = re.sub(r':', '.', line)  # Replace colons with periods
    data.append(line.strip())

df = pd.DataFrame(data, columns=['text'])
df_cleaned = df[df['text'].str.strip() != '']
df_cleaned = df_cleaned.dropna(subset=['text'])
df = df_cleaned 
df = df.reset_index(drop=True)

# -----------------------------------------------------------------------------------------------

# 4. 임시 데이터 - 갱신 
temp_collection = client.get_or_create_collection("temp_collection") 

new_embeddings = model.encode(df['text'].tolist())

# 기존 데이터를 식별하고 갱신
for i, text in enumerate(df['text']):
    # 기존 문서가 있는 경우 업데이트
    if collection.get(ids=[f"temp_document_{i}"]):
        collection.update(
            ids=[f"temp_document_{i}"],
            documents=[text],
            embeddings=[new_embeddings[i].tolist()]
        )
    else:
        # 기존 문서가 없는 경우 새로 추가
        collection.add(
            documents=[text],
            embeddings=[new_embeddings[i].tolist()],
            ids=[f"temp_document_{i}"]
        )