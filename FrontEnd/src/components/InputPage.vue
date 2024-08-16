<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
      <input v-model="youtubeLink" placeholder="Enter YouTube link" />
      <input v-model.number="groundTruthScore" type="number" placeholder="Enter Ground Truth Score (Optional)" />
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
      submitLink() { // Push to LoadingPage with the YouTube link
        if (this.youtubeLink.trim()) {
          // 유효한 YouTube 링크인지 확인
          this.$router.push({ 
            name: 'LoadingPage', 
            query: { 
              link: this.youtubeLink,
              gt_score: this.groundTruthScore // GT score가 없으면 null이 input
            } 
          });
        } else {
          alert('Please enter a valid YouTube link.');
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
  </style>
  