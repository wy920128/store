// src/data.ts
import { reactive, ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import type { Category } from "./types/category";
import type { Software } from "./types/software";
import type { SystemInfo } from "./types/system";
export const sysInfo = ref<SystemInfo>({
  name: "",
  major: 1,
  minor: 0,
  patch: 0,
  author: "",
});
export const cats = ref<Category[]>([]);
export const list = ref<Software[]>([]);
export const currentCatId = ref(0);
export const keyword = ref("");
export const pageData = reactive({
  total: 0,
  pageIndex: 1,
  pageSize: 9,
  maxItems: 5,
});
// 初始化
export async function initApp() {
  await loadSystemInfo();
  await loadCategories();
  await loadData();
}
// 系统信息
async function loadSystemInfo() {
  try {
    const res = await invoke<SystemInfo>("get_system_info");
    Object.assign(sysInfo.value, res);
  } catch (e) {}
}
// 加载分类
async function loadCategories() {
  try {
    const data = await invoke<Category[]>("get_categories");
    cats.value = data;
  } catch (e) {}
}
// 搜索
export function doSearch(val: string) {
  keyword.value = val;
  pageData.pageIndex = 1;
  loadData();
}
// 切换分类
export function changeCategory(id: number) {
  currentCatId.value = id;
  pageData.pageIndex = 1;
  loadData();
}
// 切换页码
export function changePage(p: number) {
  console.log("✅ data.ts 接收新页码 =", p);
  pageData.pageIndex = p;
  loadData();
}
// 加载数据
export async function loadData() {
  try {
    console.log("📦 开始请求数据，页码 =", pageData.pageIndex);
    const [listData, count] = await Promise.all([
      invoke<Software[]>("get_software_by_category", {
        categoryId: currentCatId.value,
        page: pageData.pageIndex,
        pageSize: pageData.pageSize,
        keyword: keyword.value,
      }),
      invoke<number>("get_software_count", {
        categoryId: currentCatId.value,
        keyword: keyword.value,
      }),
    ]);
    list.value = listData;
    pageData.total = count;
    console.log("✅ 数据加载完成，列表长度 =", listData.length);
    console.log("✅ 总数 total =", count);
  } catch (err) {
    console.error("加载失败", err);
  }
}
// 安装
export async function installApp(id: string, pkg: string) {
  if (!pkg) return alert("无安装包名");
  try {
    await invoke("install_package", { softwareId: id, package: pkg });
    loadData();
  } catch (err) {}
}
