<template>
  <div id="app">
      <DesignPicture></DesignPicture>
  </div>
</template>

<script>
import DesignPicture from './components/DesignPicture'

export default {
  name: 'App',
  components: {
    DesignPicture
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
