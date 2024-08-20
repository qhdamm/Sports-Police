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
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from rag_utils import *
from datasets import Dataset

client_db = chromadb.PersistentClient()
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    
def generate_response(query_text, db_handler, context):
    # Generate embedding for the query
    query_embedding = generate_embeddings(query_text)

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
                ]
,
        max_tokens=1500,
        temperature=0.7
    )
    
    return response.choices[0].message.content
    

if __name__ == "__main__":
    db_handler = ChromaDBHandler()
    pdf_path = './data/Competition-Regulations.pdf'
    store_pdf(pdf_path, db_handler)
    with open('./data/diving2_report.html', 'r') as file:
        html_content = file.read()
    text_content = extract_text_from_html(html_content)
    embedding = generate_embeddings(text_content)
    db_handler.store_embedding(document_id="0", text_content=text_content, embedding=embedding)
    print("Document stored successfully.")

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
    for query in eval_questions:
        context_retrieved = db_handler.retrieve_similar(generate_embeddings(query))
        context = " ".join([doc['text'] for doc in context_retrieved[0]])
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
    print(result)
    print(df['answer'][0])
    print(df['answer'][1])
