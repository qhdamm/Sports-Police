# pip install ragas
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
import chromadb
import fitz
import re
import pandas as pd
from bs4 import BeautifulSoup
from chromadb.config import Settings
import openai
import numpy as np
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from rag_utils import *
from datasets import Dataset

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

pdf_path = './data/Competition-Regulations.pdf'
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
    
def generate_response(query_text, db_handler, context):
    # Generate embedding for the query
    query_embedding = generate_embeddings(query_text)

    # Generate a response using OpenAI's language model
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query_text}"}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    
    return response['choices'][0]['message']['content'].strip()

    

if __name__ == "__main__":
    
    eval_questions = [
                'How is diving scored?',
                'I think the score is too low, why?',
                'How do you feel about receiving a score of 72?'
                ]
    eval_answers = [
                "Fact: In diving competitions, a panel of seven judges submits scores for each dive. The highest two and lowest two scores are discarded, leaving three scores that are summed to determine the diver's execution score. This execution score is then multiplied by the dive's degree of difficulty to calculate the diver's total score.\
                Your opinion: This scoring system appears well-designed to minimize the impact of outlier scores, ensuring that a diver's performance is evaluated more consistently and fairly.",
                "Fact: Your entry angle deviated from the vertical by 48°, placing you in the 1st percentile. This means that 99% of other competitors had a more vertical entry. Additionally, the straightness of your body during entry deviated by 99°, which placed you in the 0th percentile, indicating a significant misalignment of your body during entry.\
                Your opinion: The substantial deviations in both entry angle and body alignment were critical factors that significantly impacted your score, leading to the lower result.",
                "Fact: The final score is calculated by multiplying the sum of the scores from three judges by the difficulty level. Based on this, the predicted final score should have been 43.2 (4.5 * 3 * 3.2).\
                Your opinion: While there might be some bias involved, it's not conclusive enough to make a definitive judgment."
                ]
    answers=[]; contexts=[]
    # inference
    db_handler = ChromaDBHandler()
    for query in eval_questions:
        context_retrieved , _ = db_handler.retrieve_similar(generate_embeddings(query))
        context = " ".join([doc['text'] for doc in context_retrieved[0]])
        print(context)
        contexts.append([context])
        answers.append(generate_response(query, db_handler, context))
    data = {
        "question": eval_questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": eval_answers
    }
    dataset = Dataset.from_dict(data)
    result = evaluate(
        dataset = dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
        ]
    )
    
    df = result.to_pandas()
    print(df)