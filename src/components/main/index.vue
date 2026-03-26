<template>
  <div class="main-container">
    <!-- 分类 -->
    <div class="cat-box">
      <d-button
        :type="currentCatId === 0 ? 'primary' : 'default'"
        @click="emit('categoryChange', 0)"
      >
        全部
      </d-button>
      <d-button
        v-for="c in cats"
        :key="c.id"
        :type="currentCatId === c.id ? 'primary' : 'default'"
        @click="emit('categoryChange', c.id)"
      >
        {{ c.name }}
      </d-button>
    </div>

    <!-- 应用列表 -->
    <div class="software-grid">
      <d-panel v-for="item in list" :key="item.id" class="app-panel">
        <div class="app-inner">
          <img :src="item.icon_url || ''" class="app-img" />
          <div class="app-info">
            <h3>{{ item.name }}</h3>
            <p>版本：{{ item.version || "未知" }}</p>
            <p>大小：{{ item.size || "-" }}</p>
            <p>下载量：{{ item.download_count || 0 }}</p>
            <p class="dev">{{ item.provider || "UOS 官方" }}</p>
            <d-button
              type="success"
              size="sm"
              @click="emit('install', item.id, item.package || '')"
            >
              安装
            </d-button>
          </div>
        </div>
      </d-panel>
    </div>

    <!-- 分页 -->
    <div class="page-box">
      <d-pagination
        v-model:page="currentPage"
        :total="total"
        :page-size="pageSize"
        @change="emit('pageChange', currentPage)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMain } from "./index.ts";
const { cats, list, currentCatId, currentPage, pageSize, total } = useMain();

const emit = defineEmits(["categoryChange", "install", "pageChange"]);
</script>

<style scoped src="./index.css"></style>
