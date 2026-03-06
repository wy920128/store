<!--
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-06 12:02:02
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-06 14:03:16
 * @FilePath: /store/pages/software/[id].vue
 * @Description: 软件分类页
-->
<template>
  <div class="app-container">
    <main class="main-content">
      <h1>软件详情页</h1>
    </main>
  </div>
</template>
<script setup lang="ts">
// 打印出来路由的参数
const route = useRoute();
console.log(route.params);
</script>
