from bs4 import BeautifulSoup
import openai
import pickle
import argparse
from dotenv import load_dotenv
import os

# pip install openai==0.28
# openai.api_key: 노션 참고

parser = argparse.ArgumentParser()
parser.add_argument(
    "--html_path",
    type=str,    
    default="/root/rag/diving2_report.html"
)


def extract_text_from_html(html_file_path):
    with open(html_file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()
    
    
def preprocess_text(text):
    text = text.replace('\n', '')
    text = text.replace('ErrorDescriptionVisualsScore', '')
    
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Or use the latest available model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please extract meaningful content from the following text. Include additional details regarding the score, such as specific explanations like 'Your jump was a bit on the lower side.' Do not include percentile and just score like 2.6.:\n\n{text}"}
    ],
    max_tokens=1500,  # Adjust as needed
    temperature=0.7  # Adjust as needed for creativity
    )
    
    return response.choices[0].message['content'].strip()
    
    
if __name__ == '__main__':
    args = parser.parse_args()

    html_file_path = args.html_path

    text = extract_text_from_html(html_file_path)
    refined_text = preprocess_text(text)
    print("정돈된 문장:")
    print(refined_text)
    
    # pickle을 사용하여 문자열을 파일에 저장
    with open('./data/refined_text.pkl', 'wb') as file:
        pickle.dump(refined_text, file)

    