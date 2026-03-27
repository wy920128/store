<template>
  <d-layout>
    <!-- 头部 -->
    <d-header class="header">
      <div class="header-left">
        <h1>{{ systemInfo.name || "UOS 内网应用商店" }}</h1>
        <span class="version-tag" v-if="systemInfo.name">
          v{{ systemInfo.major }}.{{ systemInfo.minor }}.{{ systemInfo.patch }}
        </span>
      </div>
      <d-search
        class="search"
        v-model="searchData.keyword"
        v-if="systemInfo.name"
        icon-position="left"
        placeholder="搜索应用"
        is-keyup-search
        :delay="300"
        no-border
        @search="searchData.funcSearch"
      />
    </d-header>
    <!-- 内容区域 -->
    <d-content class="dcontent">
      <d-tabs
        type="pills"
        v-model="tabsData.activeId"
        class="full-tabs"
        @active-tab-change="tabsData.funcTabChange"
      >
        <d-tab id="0" title="全部" />
        <d-tab
          v-for="category in tabsData.categoryList"
          :key="category.id"
          :id="String(category.id)"
          :title="category.name"
        >
          <d-panel
            class="app-card"
            v-for="software in tabsData.softwareList"
            :key="software.id"
          >
            <div class="card-inner">
              <img :src="software.icon_url" class="app-icon" alt="icon" />
              <div class="app-info">
                <h3>{{ software.name }}</h3>
                <p>版本：{{ software.version || "未知" }}</p>
                <p>大小：{{ software.size || "-" }}</p>
                <p>下载：{{ software.download_count || 0 }}</p>
                <p class="provider">{{ software.provider || "官方" }}</p>
                <d-button
                  type="success"
                  size="sm"
                  @click="tabsData.funcInstall(software.id, software.package)"
                >
                  安装
                </d-button>
              </div>
            </div>
          </d-panel>
        </d-tab>
      </d-tabs>
      <div class="pagination" style="margin-top: 20px; text-align: center">
        <d-pagination
          :total="pageData.total"
          v-model:page-index="pageData.pageIndex"
          v-model:page-size="pageData.pageSize"
          can-view-total
          can-jump-page
          @page-index-change="pageData.funcPageChange"
        />
      </div>
    </d-content>
    <!-- 页脚 -->
    <d-footer class="dfooter">Footer</d-footer>
  </d-layout>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { initApp, systemInfo, searchData, tabsData, pageData } from "./data";

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
