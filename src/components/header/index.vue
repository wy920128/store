<!--
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-26 16:14:27
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-26 16:43:43
 * @FilePath: /store/src/components/header/index.vue
 * @Description: 头部组件
-->
<template>
  <div class="header">
    <div class="header-left">
      <h1>{{ sysInfo.name || `UOS 内网应用商店` }}</h1>
      <span class="version-tag" v-if="sysInfo.name">
        v{{ sysInfo.major }}.{{ sysInfo.minor }}.{{ sysInfo.patch }}
      </span>
    </div>
    <d-input
      v-model="keyword"
      placeholder="搜索应用"
      style="width: 320px"
      @keyup.enter="funcSearch"
    />
  </div>
</template>
<script setup lang="ts">
import { useHeader } from "./index.ts";
const { sysInfo, keyword } = useHeader();
const emit = defineEmits([`search`]);
function funcSearch() {
  emit(`search`, keyword.value);
}
</script>
<style scoped src="./index.css"></style>
