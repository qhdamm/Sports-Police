# Sports-Police

<div align="center">
<h3>YBIGTA DS 2024-Summer Project</h3>

<p>Project on predicting diving scores and servicing the results with RAG</p>

</div>

## Project Initiation
In sports, biased judgments by referees have long been a source of controversy.  
To address this issue objectively, we propose the development of an AI-driven service that evaluates the performance of actions during games based on a rule-based system.  
This service aims to provide users not only with the AI model’s evaluation results but also with a detailed explanation of the scores assigned.  
By offering transparency in the decision-making process, this tool will enable users to determine whether a referee’s judgment was genuinely biased or fair, thus fostering greater trust and accountability in sports officiating.

## Core Features
**User Input**: diving video link (YouTube), specify the desired time segment, the actual score

The service will then process the video through a series of steps:

1. **OCR for Difficulty Identification**
2. **Video Analysis and Score Prediction**
3. **RAG-based Q&A**


<p align="center"><img src="assets/diagram.svg" alt="Pipeline" width="80%" /></p>

### RAG Implementation and Performance Evaluation

Our RAG (Retrieval-Augmented Generation) system was implemented using `chatgpt4o-mini` and `ChromaDB`. The performance of the RAG system was evaluated using RAGAS, yielding the following results:

- **Context Precision:** 1.0000
- **Context Recall:** 0.5167
- **Faithfulness:** 0.6935
- **Answer Relevancy:** 0.5916

These metrics reflect the effectiveness and accuracy of our RAG system in generating relevant and faithful responses based on the retrieved context.

## How to Run
### Environment Setup
- **Dependencies Installation:**  `pip install -r requirements.txt`
- **`ffmpeg` Installation:** You have to install `ffmpeg` for video precessing.
  (follow this: https://medium.com/@vladakuc/compile-opencv-4-7-0-with-ffmpeg-5-compiled-from-the-source-in-ubuntu-434a0bde0ab6)
- **API Keys:** You need to set up OPENAI_API_KEY in '.env' file
### Run the Project

## Team Members
@1nhye
@chaehyun1
@kjinh
@qhdamm 
@imsolsama
@izayaki22
