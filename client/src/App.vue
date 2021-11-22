<template>
  <v-header />

  <main class="py-3">
    <router-view class="mb-5" />
  </main>

  <v-footer />
</template>

<script>
import Header from "./components/core/Header";
import Footer from "./components/core/Footer";

export default {
  components: {
    Header,
    Footer,
  },
};
</script>

<style lang="scss">
#app {
  // font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  // color: #2c3e50;

  main {
    min-height: calc(100vh - 7rem);
  }
}
</style>
