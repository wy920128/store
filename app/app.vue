<template>
  <div class="app-store">
    <!-- 页首：名称 + 搜索框 -->
    <header class="header">
      <h1 class="app-title">Nuxt 应用商店</h1>
      <el-input
        v-model="searchText"
        placeholder="搜索应用..."
        class="search-input"
        prefix-icon="el-icon-search"
        @keyup.enter="handleSearch"
      />
    </header>

    <!-- 分类栏 -->
    <div class="category-bar">
      <el-button
        v-for="category in categoryList"
        :key="category.id"
        :type="activeCategoryId === category.id ? 'primary' : 'default'"
        @click="switchCategory(category.id)"
        class="category-btn"
      >
        {{ category.name }}
      </el-button>
    </div>

    <!-- 软件列表 -->
    <main class="app-list">
      <el-card
        v-for="app in appList"
        :key="app.id"
        class="app-card"
      >
        <div class="app-info">
          <img :src="app.icon" alt="app icon" class="app-icon" />
          <div class="app-detail">
            <h3 class="app-name">{{ app.name }}</h3>
            <p class="app-desc">{{ app.desc }}</p>
          </div>
        </div>
      </el-card>
      <!-- 空数据提示 -->
      <div v-if="appList.length === 0" class="empty-tip">
        暂无该分类的应用
      </div>
    </main>
  </div>
</template>

<script setup>
// Nuxt 4 自动导入 ref、onMounted 等 Vue API，无需手动引入
// 自动导入 useFetch/useAsyncData（Nuxt 内置请求方法）
const runtimeConfig = useRuntimeConfig()
const apiBase = runtimeConfig.public.apiBase

// 响应式数据
const searchText = ref('')
const categoryList = ref([])
const activeCategoryId = ref('')
const appList = ref([])

// 初始化：加载分类 + 默认加载所有软件
onMounted(async () => {
  await loadCategories()
  await loadApps()
})

// 加载分类列表
const loadCategories = async () => {
  try {
    // Nuxt 4 内置 useFetch，自动处理异步和状态
    const { data, error } = await useFetch(`${apiBase}/categories`)
    if (error.value) throw new Error('分类加载失败')
    categoryList.value = data.value.data
  } catch (err) {
    console.error('加载分类失败：', err)
    ElMessage.error('分类加载失败') // Element Plus 消息提示
  }
}

// 加载软件列表（支持分类筛选）
const loadApps = async (categoryId = '') => {
  try {
    const { data, error } = await useFetch(`${apiBase}/apps`, {
      params: { categoryId } // 传分类ID参数
    })
    if (error.value) throw new Error('应用加载失败')
    appList.value = data.value.data
  } catch (err) {
    console.error('加载应用失败：', err)
    ElMessage.error('应用加载失败')
  }
}

// 切换分类
const switchCategory = (categoryId) => {
  activeCategoryId.value = categoryId
  loadApps(categoryId)
  // 清空搜索框
  searchText.value = ''
}

// 搜索功能（前端筛选）
const handleSearch = () => {
  if (!searchText.value) {
    // 搜索框为空，恢复当前分类的应用
    loadApps(activeCategoryId.value)
    return
  }
  // 筛选包含关键词的应用（不区分大小写）
  appList.value = appList.value.filter(app => 
    app.name.toLowerCase().includes(searchText.value.toLowerCase())
  )
}
</script>

<style scoped>
/* 全局样式 */
.app-store {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 页首样式 */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}
.app-title {
  font-size: 28px;
  color: #333;
  margin: 0;
}
.search-input {
  width: 300px;
}

/* 分类栏样式 */
.category-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.category-btn {
  padding: 8px 20px;
}

/* 软件列表样式 */
.app-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.app-card {
  height: 120px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 0.3s;
}
.app-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.app-info {
  display: flex;
  align-items: center;
  width: 100%;
}
.app-icon {
  width: 60px;
  height: 60px;
  margin-right: 15px;
}
.app-detail {
  flex: 1;
}
.app-name {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #333;
}
.app-desc {
  margin: 0;
  color: #666;
  font-size: 14px;
}
.empty-tip {
  grid-column: 1 / -1;
  text-align: center;
  padding: 50px;
  color: #999;
  font-size: 16px;
}
</style>