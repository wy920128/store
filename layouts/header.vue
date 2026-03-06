<template>
  <el-header class="app-header" height="auto">
    <div class="header-top">
      <h1 class="header-title">警务UOS内网软件商店</h1>
      <el-button
        type="primary"
        size="default"
        @click="handleLogin"
        class="login-btn"
      >
        登录
      </el-button>
    </div>
    <el-menu
      class="header-nav"
      mode="horizontal"
      background-color="#0000ff"
      text-color="#ffffff"
      active-text-color="#ffffff"
      router
    >
      <el-menu-item index="/" key="home" class="nav-item">首页</el-menu-item>
      <el-menu-item
        v-for="item in categories"
        :index="`software\/${item.id}`"
        :key="item.id"
        class="nav-item"
      >
        {{ item.name }}
      </el-menu-item>
    </el-menu>
  </el-header>
</template>

<script setup lang="ts">
import type { Classify } from '~/types';
const props = defineProps<{
  categories: Classify[];
}>();
const emit = defineEmits<{
  login: [];
}>();
const handleLogin = () => {
  emit("login");
};
</script>

<style scoped>
.app-header {
  width: 100%;
  padding: 0;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18%;
  width: 100%;
  box-sizing: border-box;
}
.header-title {
  font-size: 28px;
  font-weight: 700;
  color: #000000;
  margin: 0;
  line-height: 1.2;
}
.login-btn {
  background-color: #add8e6;
  border-color: #add8e6;
  --el-button-text-color: #ffffff;
  --el-button-hover-text-color: #ffffff;
  --el-button-hover-bg-color: #99cbe6;
  --el-button-hover-border-color: #99cbe6;
}
.header-nav {
  --el-menu-item-font-size: 16px;
  --el-menu-item-height: 48px;
  --el-menu-horizontal-item-padding: 0 24px;
  padding: 0 15%;
}
.nav-item {
  cursor: pointer;
}
</style>
