<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
      <input v-model="youtubeLink" placeholder="Enter YouTube link" />
      <button @click="submitLink">Submit</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        youtubeLink: ''
      };
    },
    methods: {
      submitLink() {
        this.$router.push({ name: 'LoadingPage', query: { link: this.youtubeLink } });
      }
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
  
  input {
    display: block;
    margin: 20px auto;
    padding: 10px;
    font-size: 16px;
  }
  
  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
  </style>
  