<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-top">
        <div class="header-left">
          <h1 class="app-title">{{ systemData.name || "UOS 内网应用商店" }}</h1>
          <span class="version-tag" v-if="systemData.name">
            v{{ systemData.major }}.{{ systemData.minor }}.{{
              systemData.patch
            }}
          </span>
        </div>

        <!-- 修复后的搜索框：回车 + 防抖自动搜索 -->
        <el-input
          v-model="searchData.keyword"
          placeholder="搜索应用"
          class="header-search"
          @keyup.enter="searchData.funcSearch"
          @input="debounceSearch"
          clearable
        >
          <template #prefix>
            <i class="ri-search-line tab-icon"></i>
          </template>
        </el-input>

      </div>
      <el-tabs
        v-model="tabsData.activeId"
        class="app-tabs"
        @tab-click="tabsData.funcTabChange"
      >
        <el-tab-pane
          v-for="category in tabsData.categoryList"
          :key="category.id"
          :name="String(category.id)"
        >
          <template #label>
            <i
              :class="[category.icon, 'tab-icon', 'text-lg']"
              :style="{
                color:
                  Number(tabsData.activeId) === category.id
                    ? '#526ECC'
                    : '#1d1d21',
              }"
            ></i>
            <span class="tab-name">{{ category.name }}</span>
          </template>
        </el-tab-pane>
      </el-tabs>
    </header>
    <main class="app-content">
      <div class="app-grid">
        <el-card
          class="app-card"
          v-for="software in tabsData.softwareList"
          :key="software.id"
          shadow="hover"
        >
          <div class="card-body">
            <img :src="software.icon_url" class="card-icon" alt="应用图标" />
            <div class="card-info">
              <h3 class="card-title">{{ software.name }}</h3>
              <p class="card-text">版本：{{ software.version || "未知" }}</p>
              <p class="card-text">大小：{{ software.size || "-" }}</p>
              <p class="card-text">下载：{{ software.download_count || 0 }}</p>
              <p class="card-provider">{{ software.provider || "官方" }}</p>
              <el-button
                type="success"
                size="small"
                class="card-btn"
                @click="tabsData.funcInstall(software.id, software.package)"
              >
                一键安装
              </el-button>
            </div>
          </div>
        </el-card>
        <div v-if="tabsData.softwareList.length === 0" class="app-empty">
          <el-empty description="暂无应用数据" />
        </div>
      </div>
      <div class="app-pagination">
        <el-pagination
          v-model:current-page="pageData.pageIndex"
          v-model:page-size="pageData.pageSize"
          :total="pageData.total"
          background
          layout="total, prev, pager, next, jumper"
          @size-change="pageData.funcPageChange"
          @current-change="pageData.funcPageChange"
        />
      </div>
    </main>
    <footer class="app-footer">
      <span>{{ systemData.name || "UOS 内网应用商店" }} © 2025</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { initApp, systemData, searchData, tabsData, pageData } from "./data";

// 防抖函数（500ms 延迟搜索）
const debounceSearch = useDebounce(() => {
  console.log(`--->`, searchData.keyword);
  searchData.funcSearch(searchData.keyword);
}, 500);

onMounted(() => {
  initApp();
});

// 防抖工具函数
function useDebounce(fn: (...args: any[]) => void, delay: number) {
  let timeoutId: any;
  return (...args: any[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
</script>

<style scoped>
.app-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f7f8fa;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
.app-header {
  flex-shrink: 0;
  background: #ffffff;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 999;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.header-top {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.app-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
}
.version-tag {
  padding: 2px 8px;
  background: #e8f3ff;
  color: #1677ff;
  border-radius: 4px;
  font-size: 12px;
}
.header-search {
  width: 360px;
  --el-input-bg-color: #f1f3f5;
  --el-input-border-color: transparent;
  --el-input-text-color: #333;
}
.app-tabs {
  height: 48px;
  display: flex;
  align-items: center;
  background: #ffffff;
  padding: 0 12px;
}
.tab-icon {
  margin-right: 6px;
  font-size: 20px;
}
.tab-name {
  font-size: 18px;
}
.app-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px 32px;
}
.app-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}
.app-card {
  border-radius: 12px;
  border: none;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.25s ease;
  overflow: hidden;
}
.app-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}
.card-body {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
}
.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  object-fit: cover;
  flex-shrink: 0;
}
.card-info {
  flex: 1;
  min-width: 0;
}
.card-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-text {
  margin: 0 0 4px 0;
  font-size: 12px;
  color: #666;
}
.card-provider {
  margin: 0 0 10px 0;
  font-size: 12px;
  color: #1677ff;
}
.card-btn {
  border-radius: 6px;
  font-size: 12px;
  padding: 4px 12px;
}
.app-empty {
  grid-column: 1 / -1;
  padding: 60px 0;
  text-align: center;
}
.app-pagination {
  text-align: center;
  margin-top: 12px;
}
.app-footer {
  flex-shrink: 0;
  height: 48px;
  line-height: 48px;
  text-align: center;
  font-size: 12px;
  color: #999;
  background: #ffffff;
  border-top: 1px solid #eee;
}
</style>