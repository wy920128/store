<!--
 * @Author: wangye 18545455617@163.com
 * @Date: 2026-04-20 14:45:03
 * @LastEditors: wangye 18545455617@163.com
 * @LastEditTime: 2026-04-21 15:42:46
 * @FilePath: /store/src/App.vue
 * @Description: 应用商店主界面
-->
<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-top">
        <div class="header-left">
          <span class="app-title">{{ systemData.name || "内网应用商店" }}</span>
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
        @tab-change="tabsData.funcTabChange"
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
            <div class="card-top">
              <div class="card-left">
                <el-image
                  class="card-icon"
                  :src="software.icon_url || ''"
                  alt="图标"
                  fit="contain"
                >
                  <template #error>
                    <div class="image-error-slot">
                      <i class="ri-image-line"></i>
                    </div>
                  </template>
                </el-image>
              </div>
              <div class="card-right">
                <span class="card-title">{{ software.name }}</span>
                <p class="card-version">
                  版本：{{ software.version || "未知" }}
                </p>
              </div>
            </div>
            <div class="card-bottom">
              <div class="card-row-1">
                <span>大小：{{ software.size || "-" }}</span>
                <span>下载：{{ software.download_count || 0 }}</span>
              </div>
              <div class="card-row-2">
                <el-tooltip
                  :content="software.description || '暂无描述'"
                  placement="top"
                >
                  <p class="card-desc">
                    {{ software.description || "暂无描述" }}
                  </p>
                </el-tooltip>
              </div>
              <div class="card-row-3">
                <el-button
                  type="success"
                  size="small"
                  @click="handleInstall(software.id, software.package)"
                >
                  一键安装
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
        <div v-if="tabsData.softwareList.length === 0" class="app-empty">
          <el-empty description="暂无应用" />
        </div>
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
      <div class="app-logger">
        <el-card class="logger-card" shadow="hover">
          <div class="log-header">
            <span class="log-title">日志</span>
            <el-button
              type="info"
              round
              plain
              size="small"
              @click="installLog = []"
              >清空</el-button
            >
          </div>
          <div class="log-body">
            <pre v-for="(log, idx) in installLog" :key="idx" :class="log.type">
            {{ log.message }}
          </pre
            >
            <div v-if="installLog.length === 0" class="log-empty">
              暂无运行日志
            </div>
          </div>
        </el-card>
      </div>
    </main>
    <footer class="app-footer">
      <span
        >{{ systemData.name || "UOS内网应用商店" }} - {{ systemData.author }} ©
        2026</span
      >
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
  handleInstall,
  debounceSearch,
  initApp,
} from "./data";
onMounted(() => {
  initApp();
});
console.log(`systemData`, systemData);
console.log(`searchData`, searchData);
console.log(`tabsData`, tabsData);
console.log(`pageData`, pageData);
</script>
<style src="./style.scss" lang="scss"></style>
