<template>
  <div class="app-container">
    <Header @search="funcSearch" />
    <Main
      @categoryChange="selectCat"
      @install="install"
      @pageChange="loadData"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import Header from "./components/header/index.vue";
import Main from "./components/main/index.vue";
import { initApp, loadData, selectCat, install, funcSearch } from "./data.ts";

onMounted(() => {
  initApp();
});
</script>

<style scoped>
.app-container {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}
</style>
