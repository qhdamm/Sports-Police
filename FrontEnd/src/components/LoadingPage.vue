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
      // 채점하기 버튼 클릭 시 OutputPage로 이동
      goToOutputPage() {
        // 쿼리 파라미터 예시로 임의의 값 설정
        const exampleScore = 85;
        const exampleImage = 'http://example.com/example-image.jpg';
        const exampleText = 'Example result text';
  
        // OutputPage로 네비게이션
        this.$router.push({
          name: 'OutputPage',
          query: {
            score: exampleScore,
            image: exampleImage,
            text: exampleText
          }
        });
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
  