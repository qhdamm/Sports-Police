<template>
  <div id="app">
    <header>
      <h1>SGYUNG 당신의 AI 스포츠 심판</h1>
    </header>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
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
</style>
