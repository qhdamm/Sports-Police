import os
import pandas as pd
import numpy as np
from numpy import dot
import re
from numpy.linalg import norm
from dotenv import load_dotenv
from openai import OpenAI
import pickle
import argparse
import openai

# pip install --upgrade openai
# .env 파일에 api key 저장하기 

parser = argparse.ArgumentParser()
parser.add_argument(
    "--user_prompt",
    type=str,    
    default="I scored a total of 4.5 points in diving. Please explain in detail the reasons for this score based on the judging criteria without mentioning which document this content corresponds to."
)


def get_embedding(text, engine):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI() 
    
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=engine).data[0].embedding


def cos_sim(A, B):
    # 두 임베딩간 유사도 계산
    return dot(A, B)/(norm(A)*norm(B))


def return_answer_candidate(df, query):
    query_embedding = get_embedding(
        query,
        engine="text-embedding-ada-002"
    )
    
    # 입력된 질문과 각 문서의 유사도
    df['similarity'] = df['embedding'].apply(lambda x: cos_sim(np.array(query_embedding), np.array(x)))
    
    # 유사도 높은 순으로 정렬
    top = df.sort_values("similarity", ascending=False)
    return top


def create_prompt(df, query):
    # 질문에 대한 가장 유사한 문서 9개 가져와서, messages셋 만들어서 리턴
    # 질문과 가장 유사한 문서 9개 가져오기
    result = return_answer_candidate(df, query)
    
    # Document content message construction
    documents = [f"document{i+1}: {result.iloc[i]['text']}" for i in range(len(result))]
    documents_content = "\n".join(documents)
    
    system_message = f"""
    Please answer in detail, referring to the provided document.
    document content:
    {documents_content}
    Gather the details as thorouhly as possible, then categorize them according to the following format:
    - Fact: { }
    - Your opinion: { }
    Please explain each item in one or two sentences.
    """

    user_message = f"""User question: "{str(query)}". """

    messages =[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    return messages


def generate_response(messages):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    
    # 완성된 질문에 대한 답변 생성
    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.4,
        max_tokens=500)
    return result.choices[0].message.content
    
    
if __name__ == '__main__':
    args = parser.parse_args()

    with open('./data/refined_text.pkl', 'rb') as file:
        text = pickle.load(file)
    
    # 전처리 
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

    # openai embedding실행
    df['embedding'] = df.apply(lambda row: get_embedding(row.text, engine="text-embedding-ada-002"), axis=1) # axis=1이므로 행단위로 get_embedding함수를 실행, row은 arg로 해당 함수에 전달

    # 파일로 저장
    folder_path = './data'
    file_name = 'embedding.csv'
    file_path = os.path.join(folder_path, file_name)
    df.to_csv(file_path, index=False)

    # 답변 
    user_input = args.user_prompt
    prompt = create_prompt(df, user_input)
    chatbot_response = generate_response(prompt)
    print(chatbot_response)