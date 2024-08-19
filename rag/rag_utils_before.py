import chromadb
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import re
import pandas as pd
import os
from bs4 import BeautifulSoup
from chromadb.config import Settings
import openai
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
client_db = chromadb.PersistentClient()
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def generate_embeddings(text):
    model = SentenceTransformer('paraphrase-mpnet-base-v2') 
    embeddings = model.encode([text])
    return np.array(embeddings[0])

class ChromaDBHandler:
    def __init__(self):
        self.client_db = chromadb.Client(Settings())
        self.collection = self.client_db.get_or_create_collection(name="report_tables",metadata={"hnsw:space": "cosine"})

    def store_embedding(self, document_id, text_content, embedding):
        # Ensure text_content is a string and embedding is a list of floats
        if isinstance(text_content, str):
            self.collection.add(
                documents=[text_content],  # Only the text content should be passed here
                embeddings=[embedding.tolist()],  # Embedding passed directly
                ids=[document_id],
                metadatas=[{"text": text_content}]
            )
        else:
            raise ValueError("text_content must be a string")

    def retrieve_similar(self, query_embedding, top_k=5):
        # Corrected the argument name from 'vectors' to 'embeddings'
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=["metadatas"]
        )
        return results['metadatas']
    
    def delete_document(self, document_id):
        # Delete the document with the given document_id from the collection
        self.collection.delete(ids=[document_id])

    def reset_chroma_db(self):
        # 모든 컬렉션 가져오기
        collections = self.client_db.list_collections()
        
        # 각 컬렉션 삭제
        for collection in collections:
            self.client_db.delete_collection(collection.name)

        print("All collections have been deleted.")
        

def generate_response_with_rag(query_text, db_handler):
    # Generate embedding for the query
    query_embedding = generate_embeddings(query_text)

    # Retrieve similar documents from ChromaDB
    retrieved_docs, _ = db_handler.retrieve_similar(query_embedding)
    # print(retrieved_docs)

    # Combine retrieved documents into a context string
    context = " ".join([doc['text'] for doc in retrieved_docs[0]])

    # Generate a response using OpenAI's language model
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", 
                    "content": f"Respond to the following given topic. Gather the details as thoroughly as possible, then categorize them according to the following format. Give me the response in one or two sentences.:\n\n\
                                - Fact: {{ }}\n\
                                - Your opinion: {{ }}\n\n\
                                - Topic: {context}. {query_text}"}
                ],
        max_tokens=1500,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def store_pdf(pdf_path, db_handler):
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

    
    sections = split_pdf_by_section_titles(pdf_path, section_titles)

    # 텍스트 임베딩 생성
    model = SentenceTransformer('paraphrase-mpnet-base-v2') # 임베딩 모델 로드

    # PDF에서 추출한 텍스트 임베딩 생성
    sections = split_pdf_by_section_titles(pdf_path, section_titles)
    embeddings = model.encode(sections)

    # 2. 고정 데이터: 컬렉션 생성 또는 가져오기
    collection_name = "diving_rule_collection"  # New collection name
    try:
        db_handler.collection = client_db.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists. Using existing collection.")
    except:
        db_handler.collection = client_db.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
        print(f"Collection '{collection_name}' does not exist. Creating new collection.")


    # 임베딩된 텍스트를 컬렉션에 추가
    for i, section in enumerate(sections):
        db_handler.store_embedding(
            document_id=f"pdf_section_{i}",
            text_content=section,
            embedding=embeddings[i]
        )

