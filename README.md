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
