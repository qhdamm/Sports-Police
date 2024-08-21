<template>
    <div>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
      <p>Loading...</p>
      <!-- 채점하기 버튼 추가 -->
      <!-- <button @click="goToOutputPage">채점하기</button> -->
    </div>
  </template>
  
  <script>
  export default {
    mounted() {
      this.goToOutputPage();
    },

    methods: {
      async goToOutputPage() { // Analyze the video and push to OutputPage
        try {

          const youtubeLink = this.$route.query.link;
          const groundTruthScore = this.$route.query.gt_score;
          const startTime = this.$route.query.start_time;
          const endTime = this.$route.query.end_time;

          if (!youtubeLink) {
            throw new Error('YouTube link is missing.');
          }

          // send a POST request to the backend
          const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              url: youtubeLink,
              gt_score: groundTruthScore ? parseFloat(groundTruthScore) : null,
              start_time: startTime || "FULL_VIDEO",
              end_time: endTime || "FULL_VIDEO"
            }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const result = await response.json();
          console.log('Analysis result received:', result);

          // Push to OutputPage with the result
          this.$router.push({ // Push to OutputPage with the result
            name: 'OutputPage',
            query: {
              gt_score: result.gt_score,
              report: result.report,
              document_id: result.document_id,
              video_name: result.video_name
            }
          });
        } catch (error) {
          console.error('Error:', error);
          alert('Failed to analyze video. Please try again later.');

          // Redirect to InputPage
          this.$router.push({ name: 'InputPage' });
        }
      }
    }
  }
  </script>
  
  <style>
  h1 {
    text-align: center;
    font-size: 24px;
    margin: 20px 0;
  }
  
  p {
    text-align: center;
    font-size: 20px;
  }
  </style>
  
