# Sports-Police

<div align="center">
<h3>YBIGTA DS 2024-Summer Project</h3>


<p>Project on predicting diving scores and servicing the results with RAG</p></div>

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

- **Dependencies Installation**
  - For Backend, Activate .venv and `pip install -r Backend/requirements.txt`
  - For NSAQA, Activate another conda env and `pip install -r NSAQA/requirements.txt`
- **Prerequisite:** `npm --version==10.8.2`
- **`ffmpeg` Installation:** You have to install `ffmpeg` for video precessing.
  (follow this: https://medium.com/@vladakuc/compile-opencv-4-7-0-with-ffmpeg-5-compiled-from-the-source-in-ubuntu-434a0bde0ab6)
- **API Keys:** You need to set up OPENAI_API_KEY in '.env' file

### Run the Project

1. Activate Backend and Frontend module first

```
$uvicorn main:app --reload # in ./Backend
```

``````
$npm run serve # in ./Frontend
``````

2. Run Inference Server module

``````
$uvicorn app:app --host 0.0.0.0 --port 8090 # in ./NSAQA
``````



## Team Members
|김대솔|김보담|김진형|김채현|박수연|양인혜|
|:---:|:---:|:---:|:---:|:---:|:---:|
|<img src="https://avatars.githubusercontent.com/u/155630439?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/88372309?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/69679512?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/108905986?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/109861031?v=4" width="150" height="150">|<img src="https://avatars.githubusercontent.com/u/128305836?v=4" width="150" height="150">|
|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/imsolsama)](https://github.com/imsolsama)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/qhdamm)](https://github.com/qhdamm)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/kjinh)](https://github.com/kjinh)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/chaehyun1)](https://github.com/chaehyun1)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/izayaki22)](https://github.com/izayaki22)|[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github&link=https://github.com/1nhye)](https://github.com/1nhye)|
