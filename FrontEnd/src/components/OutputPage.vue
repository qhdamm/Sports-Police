<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>

      <!-- GT score -->
      <div v-if="gtScore !== null">
        <h2>Ground Truth Score: {{ gtScore }}</h2>
      </div>

      <div v-html="report"></div>
      <!-- 추가 질문을 위한 섹션 -->
      <div v-if="qaEnabled">
        <h2>Ask a Question:</h2>
        <input v-model="question" placeholder="Enter your question here" />
        <button @click="submitQuestion">Submit</button>

        <p v-if="answer">Answer: {{ answer }}</p>
      </div>

      <button @click="goHome">Home</button>

    </div>
  </template>
  



  <script>
  import axios from "axios";

  export default {
    data() { // Initialize data
      return {
        gtScore: null,  // Ground Truth Score
        report: null, // 모델의 HTML report
        question: '',
        answer: '',
        documentId: null,  // document_id
        video_name: null,
        qaEnabled: true // 기본적으로 QA 기능 활성화
      };
    },
    created() { // Get the query parameters to initialize the data
      this.gtScore = this.$route.query.gt_score !== undefined ? parseFloat(this.$route.query.gt_score) : null;
      this.report = this.$route.query.report;
      this.documentId = this.$route.query.document_id;
      this.video_name = this.$route.query.video_name;
    },
    methods: { // Define methods to handle user interactions
      async submitQuestion() {
        try {
          const response = await axios.post('http://localhost:8000/qa', {
            user_input: this.question,
            document_id: this.documentId, // str, gpt_html id
            video_name: this.video_name // str
          });

          this.answer = response.data.answer;
        } catch (error) {
          console.error('Error: ', error);
          alert('Failed to get an answer. Please try again later.');
        }
      },
      async goHome() {
        try {
          // reset system by calling the backend to delete the document and clear the report
          const response = await axios.post('http://localhost:8000/home', {
            document_id: this.documentId
          });
          alert(response.data.message);
          // Redirect to the home page (input page)
          this.$router.push({ name: 'InputPage' });
        } catch (error) {
          console.error('Error: ', error);
          alert('Failed to reset the system. Please try again later.');
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
