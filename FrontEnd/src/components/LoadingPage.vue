<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
      <p>Loading...</p>
      <!-- 채점하기 버튼 추가 -->
      <button @click="goToOutputPage">채점하기</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      async goToOutputPage() {
        try {
          const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: this.$route.query.link }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const result = await response.json();

          this.$router.push({
            name: 'OutputPage',
            query: {
              score: result.score,
              image: result.image_url,
              text: result.text
            }
          });
        } catch (error) {
          console.error('Error:', error);
          alert('Failed to analyze video. Please try again later.');
        }
      }
    }
  }
  </script>
  
  <style>
  header {
    background-color: #282c34;
    padding: 20px;
    color: white;
    text-align: center;
  }
  
  h1 {
    margin: 0;
    font-size: 24px;
  }
  
  p {
    text-align: center;
    font-size: 20px;
  }
  
  button {
    display: block;
    margin: 20px auto;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
  </style>
  