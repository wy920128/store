import { ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { setSysInfo } from "./components/header/index.ts";
import {
  setCategories,
  setCurrentCatId,
  setList,
  setPage,
  setTotal,
} from "./components/main/index.ts";
import type { Category } from "./types/category";
import type { Software } from "./types/software";
import type { SystemInfo } from "./types/system";

// 系统信息
export const sysInfo = ref<SystemInfo>({
  name: "",
  major: 1,
  minor: 0,
  patch: 0,
  author: "",
});

// 列表数据
export const cats = ref<Category[]>([]);
export const list = ref<Software[]>([]);
export const currentCatId = ref<number>(0);
export const keyword = ref<string>("");
export const page = ref<number>(1);
export const pageSize = ref<number>(9);
export const total = ref<number>(0);

// 初始化
export async function initApp() {
  try {
    await loadSystemInfo();
    setSysInfo(sysInfo.value);
    await loadCats();
    await loadData(1);
  } catch (error) {
    console.error("初始化失败", error);
  }
}

// 加载系统信息
async function loadSystemInfo() {
  try {
    const res = await invoke<SystemInfo>("get_system_info");
    Object.assign(sysInfo.value, res);
  } catch (e) {
    console.error("加载系统信息失败", e);
  }
}

// 搜索
export function funcSearch(val: string) {
  keyword.value = val;
  loadData(1);
}

// 加载分类
async function loadCats() {
  try {
    const data = await invoke<Category[]>("get_categories");
    cats.value = data;
    setCategories(data);
  } catch (error) {
    console.error("加载分类失败", error);
  }
}

// 加载应用列表
export async function loadData(p: number) {
  try {
    page.value = p;

    const listData = await invoke<Software[]>("get_software_by_category", {
      categoryId: currentCatId.value,
      page: p,
      pageSize: pageSize.value,
      keyword: keyword.value,
    });

    const count = await invoke<number>("get_software_count", {
      categoryId: currentCatId.value,
      keyword: keyword.value,
    });

    list.value = listData;
    total.value = count;

    setList(listData);
    setPage(p);
    setTotal(count);
  } catch (error) {
    console.error("加载应用失败", error);
  }
}

// 选择分类
export function selectCat(id: number) {
  currentCatId.value = id;
  setCurrentCatId(id);
  loadData(1);
}

// 安装
export async function install(id: string, pkg: string) {
  if (!pkg) {
    alert("无安装包名");
    return;
  }
  try {
    await invoke("install_package", { softwareId: id, package: pkg });
    loadData(page.value);
  } catch (error) {
    console.error("安装失败", error);
  }
}
