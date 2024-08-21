<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
      <input v-model="youtubeLink" placeholder="Enter YouTube link" />
      <input v-model.number="groundTruthScore" type="number" step="0.1" placeholder="Enter Ground Truth Score (Optional, float)" />
      
      <div class="time-buttons">
        <input v-model="startTime" type="text" placeholder="Enter Start Time (Optional, e.g. 01:30)" />
        <input v-model="endTime" type="text" placeholder="Enter End Time (Optional, e.g. 03:00)" />
      </div>
      
      <button @click="submitLink">Submit</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        youtubeLink: '',
        groundTruthScore: null, // Optional Ground Truth score
        startTime: '', // (Optional)
        endTime: '' // (Optional)
      };
    },
    methods: {
      submitLink() { // Push to LoadingPage with the YouTube link
        if (this.youtubeLink.trim()) {

          const startTime = this.startTime.trim() || "FULL_VIDEO";
          const endTime = this.endTime.trim() || "FULL_VIDEO";

          this.$router.push({ 
            name: 'LoadingPage', 
            query: { 
              link: this.youtubeLink,
              gt_score: this.groundTruthScore, // GT 점수
              start_time: startTime, // 시작 시간
              end_time: endTime // 끝 시간
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
  
  .time-buttons {
  display: flex;
  justify-content: space-around;
  margin: 20px auto;
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
  
