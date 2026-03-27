<!--
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-26 16:14:27
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-27 09:10:04
 * @FilePath: /store/src/Header.vue
 * @Description: 头部组件
-->
<template>
  <div class="header">
    <div class="header-left">
      <h1>{{ sysInfo.name || "UOS 内网应用商店" }}</h1>
      <span class="version-tag" v-if="sysInfo.name">
        v{{ sysInfo.major }}.{{ sysInfo.minor }}.{{ sysInfo.patch }}
      </span>
    </div>

    <!-- <d-input
      v-model="searchText"
      placeholder="搜索"
      style="width: 320px"
      @keyup.enter="handleSearch"
    /> -->
    <d-search
      class="search"
      v-model="searchText"
      v-if="sysInfo.name"
      icon-position="left"
      placeholder="搜索应用"
      is-keyup-search
      delay="300"
      no-border
      @search="funcSearch"
    ></d-search>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { sysInfo } from "./data.ts";

// 本地搜索框状态
const searchText = ref("");
const emit = defineEmits(["funcSearch"]);

// 搜索提交
function funcSearch() {
  emit("funcSearch", searchText.value);
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.version-tag {
  padding: 2px 8px;
  background: #e8f3ff;
  color: #1677ff;
  border-radius: 4px;
  font-size: 12px;
}
.search {
  width: 320px;
}
</style>
