<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
      <div v-html="report"></div>
      <!-- 추가 질문을 위한 섹션 -->
      <div v-if="qaEnabled">
        <h2>Ask a Question:</h2>
        <input v-model="question" placeholder="Enter your question here" />
        <button @click="submitQuestion">Submit</button>

        <p v-if="answer">Answer: {{ answer }}</p>
      </div>
    </div>
  </template>
  



  <script>
  import axios from "axios";

  export default {
    data() {
      return {
        report: null, // 모델의 HTML report
        question: '',
        answer: '',
        qaEnabled: true // 기본적으로 QA 기능 활성화
      };
    },
    created() {
      this.report = this.$route.query.report;
    },
    methods: {
      async submitQuestion() {
        try {
          const response = await axios.post('http://localhost:8000/qa', {
            question: this.question,
          });
          this.answer = response.data.answer;
        } catch (error) {
          console.error('Error: ', error);
          alert('Failed to get an answer. Please try again later.');
        }
      }
    }
  };
  </script>
  
  <style>
  h1 {
    text-align: center;
    font-size: 24px;
    margin: 20px 0;
  }
  
  h2 {
    text-align: center;
    font-size: 22px;
  }
  
  input {
    display: block;
    margin: 20px auto;
    padding: 10px;
    font-size: 16px;
    width: 80%;
  }
  
  button {
    display: block;
    margin: 20px auto;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
  
  p {
    text-align: center;
    font-size: 18px;
    margin: 20px 0;
  }
  </style>