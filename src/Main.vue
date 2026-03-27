<!--
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-26 17:32:29
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-27 09:02:38
 * @FilePath: /store/src/Main.vue
 * @Description: 主页面组件
-->
<template>
  <div class="main-container">
    <!-- 分类 -->
    <div class="cat-box">
      <d-button
        :type="currentCatId === 0 ? 'primary' : 'default'"
        @click="emit('category-change', 0)"
      >
        全部
      </d-button>
      <d-button
        v-for="c in cats"
        :key="c.id"
        :type="currentCatId === c.id ? 'primary' : 'default'"
        @click="emit('category-change', c.id)"
      >
        {{ c.name }}
      </d-button>
    </div>

    <!-- 应用列表 -->
    <div class="software-grid">
      <d-panel v-for="item in list" :key="item.id" class="app-panel">
        <div class="app-inner">
          <img :src="item.icon_url || ''" class="app-img" alt="应用图标" />
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
    <!-- 分页 ✅ 绝对修复 -->
    <div class="page-box">
      <d-pagination
        size="sm"
        :total="pageData.total"
        v-model:pageSize="pageData.pageSize"
        v-model:pageIndex="pageData.pageIndex"
        :max-items="10"
        :can-view-total="true"
        :can-jump-page="true"
        :show-jump-button="true"
        @page-index-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Category } from "./types/category";
import { Pager } from "./types/pager";
import type { Software } from "./types/software";

const props = defineProps({
  cats: { type: Array as () => Category[], default: () => [] },
  list: { type: Array as () => Software[], default: () => [] },
  currentCatId: { type: Number, default: 0 },
  pageData: { type: Object as () => Pager, default: () => ({}) },
});

const emit = defineEmits<{
  "category-change": [id: number];
  "func_page-change": [page: number];
  install: [id: string, pkg: string];
}>();

// ✅ 分页点击（带日志打印，排查问题）
function handlePageChange(newPage: number) {
  console.log("=====================================");
  console.log("👉 分页点击了，新页码 =", newPage);
  console.log("👉 当前组件接收的页码 =", props.pageData.pageIndex);
  console.log("👉 总数 total =", props.pageData.total);
  console.log("👉 每页条数 pageSize =", props.pageData.pageSize);
  emit("func_page-change", newPage);
}
</script>

<style scoped>
.main-container {
  width: 100%;
}
.cat-box {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.software-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}
.app-panel {
  height: 100%;
}
.app-inner {
  display: flex;
  padding: 16px;
  gap: 16px;
  height: 100%;
  box-sizing: border-box;
}
.app-img {
  width: 64px;
  height: 64px;
  object-fit: contain;
  border-radius: 8px;
  flex-shrink: 0;
}
.app-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.app-info h3 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}
.app-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}
.dev {
  color: #999 !important;
  font-size: 12px !important;
}
.app-info .d-button {
  margin-top: 8px;
}
.page-box {
  display: flex;
  justify-content: center;
  padding: 10px 0;
}
</style>
