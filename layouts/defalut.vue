<!--
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-04 16:35:26
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-06 14:05:02
 * @FilePath: /store/pages/index.vue
 * @Description: 首页
-->
<template>
  <div class="app-container">
    <Header :categories="categoryList" @login="onLogin" />
    <main class="main-content">
      <!-- 应用列表区域，可后续扩展 -->
      <div class="app-list">
        <client-only>
          <Transition name="page-fade" mode="out-in">
            <div :key="route.fullPath" class="page-router-view">
              <NuxtPage />
            </div> </Transition
        ></client-only>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from "~/layouts/header.vue";
import type { Classify, ClassifyRes, Res } from "~/types";
const route = useRoute();
const categoryList = ref<Classify[]>([]);
const fetchClassify = async () => {
  try {
    const res = await $fetch<Res<ClassifyRes[]>>(`/api/classify/get`, {
      method: `GET`,
    });
    if (res.success) {
      categoryList.value = res.data.list;
    }
  } catch (error) {
    console.error(`获取分类失败:`, error);
  }
};
const onLogin = () => {
  // 登录逻辑，目前为空
  console.log(`登录按钮被点击`);
};
onMounted(() => {
  fetchClassify();
});
</script>

<style scoped>
.app-container {
  width: 100%;
  min-height: 100vh;
  background-color: #ffffff;
}

.main-content {
  padding: 20px;
}

.app-list {
  margin-top: 20px;
}
</style>
