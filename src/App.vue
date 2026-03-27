<template>
  <div class="app-container">
    <Header @funcSearch="doSearch" />
    <Main
      :cats="cats"
      :list="list"
      :current-cat-id="currentCatId"
      :page-data="pageData"
      @category-change="changeCategory"
      @func_page-change="changePage"
      @install="installApp"
    />
  </div>
</template>
<script setup lang="ts">
import { onMounted } from "vue";
import Header from "./Header.vue";
import Main from "./Main.vue";
import {
  initApp,
  doSearch,
  changeCategory,
  changePage,
  installApp,
  cats,
  list,
  currentCatId,
  pageData,
} from "./data.ts";
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
