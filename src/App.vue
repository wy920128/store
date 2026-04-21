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
        <el-input
          v-model="searchData.keyword"
          placeholder="搜索应用"
          class="header-search"
          @keyup.enter="searchData.funcSearch"
          @input="debounceSearch"
          clearable
        >
          <template #prefix>
            <i class="ri-search-line"></i>
          </template>
        </el-input>
      </div>
      <el-tabs
        v-model="tabsData.activeId"
        class="app-tabs"
        @tab-click="(e) => tabsData.funcTabChange(e.name)"
      >
        <el-tab-pane
          v-for="category in tabsData.categoryList"
          :key="category.id"
          :name="String(category.id)"
        >
          <template #label>
            <i :class="[category.icon, 'tab-icon']"></i>
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
            <img :src="software.icon_url" class="card-icon" alt="图标" />
            <div class="card-info">
              <h3 class="card-title">{{ software.name }}</h3>
              <div class="card-metas">
                <p class="card-text">版本：{{ software.version || "未知" }}</p>
                <p class="card-text">大小：{{ software.size || "-" }}</p>
                <p class="card-text">
                  下载：{{ software.download_count || 0 }}
                </p>
              </div>
              <p class="card-provider">{{ software.provider || "官方" }}</p>
              <el-button
                type="success"
                size="small"
                @click="handleInstall(software.id, software.package)"
              >
                一键安装
              </el-button>
            </div>
          </div>
        </el-card>
        <div v-if="tabsData.softwareList.length === 0" class="app-empty">
          <el-empty description="暂无应用" />
        </div>
      </div>
      <div v-if="installLog.length" class="log-box">
        <div class="log-header">
          <span>安装输出</span>
          <el-button type="text" @click="installLog = []">清空</el-button>
        </div>
        <pre class="log-content">
          <template v-for="(log, index) in installLog" :key="index">
            <span :class="log.type === 'error' ? 'log-error' : 'log-info'">
              {{ log.message }}
            </span>
          </template>
        </pre>
      </div>
      <div class="app-pagination">
        <el-pagination
          v-model:current-page="pageData.pageIndex"
          v-model:page-size="pageData.pageSize"
          :total="pageData.total"
          background
          layout="total, prev, pager, next, jumper"
          @current-change="pageData.funcPageChange"
        />
      </div>
    </main>
    <footer class="app-footer">
      <span>{{ systemData.name || "UOS内网应用商店" }} © 2025</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import {
  systemData,
  searchData,
  tabsData,
  pageData,
  installLog,
  loadList,
  handleInstall,
  debounceSearch,
  initApp,
} from "./data";

onMounted(() => {
  initApp();
});
</script>

<style src="./style.css"></style>
