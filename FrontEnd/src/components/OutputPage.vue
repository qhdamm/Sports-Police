<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
      <h2>Score: {{ score }}</h2>
      <img :src="image" alt="Result Image" />
      <p>{{ text }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        score: null,
        image: null,
        text: null
      };
    },
    created() {
      this.score = this.$route.query.score;
      this.image = this.$route.query.image;
      this.text = this.$route.query.text;
    }
  };
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
  
  h2 {
    text-align: center;
  }
  
  img {
    display: block;
    margin: 20px auto;
  }
  
  p {
    text-align: center;
    font-size: 18px;
  }
  </style>
  