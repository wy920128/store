import { reactive, ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { CategoryT, SoftwareT, SystemT } from "./types";

export const systemInfo: {
  name: string;
  major: number;
  minor: number;
  patch: number;
  author: string;
} = reactive({
  name: ``,
  major: 1,
  minor: 0,
  patch: 0,
  author: `王野`,
});

// 搜索条件
export const searchData: {
  keyword: string;
  funcSearch: (keyword: string) => void;
} = reactive({
  keyword: ``,
  funcSearch(keyword: string) {
    searchData.keyword = keyword;
    pageData.pageIndex = 1;
    loadData();
  },
});

export const tabsData: {
  activeId: string;
  categoryList: CategoryT[];
  softwareList: SoftwareT[];
  funcTabChange: (id: string) => void;
  funcInstall: (id: string, pkg: string) => void;
} = reactive({
  activeId: `0`,
  categoryList: [],
  softwareList: [],
  funcTabChange(id: string) {
    tabsData.activeId = String(id);
    pageData.pageIndex = 1;
    loadData();
  },
  async funcInstall(id: string, pkg: string) {
    if (!pkg) return;
    try {
      await invoke("install_package", { softwareId: id, package: pkg });
      loadData();
    } catch {}
  },
});

// 应用列表
export const list = ref<SoftwareT[]>([]);

// 分页
export const pageData = reactive({
  total: 0,
  pageIndex: 1,
  pageSize: 9,
  funcPageChange(page: number) {
    pageData.pageIndex = page;
    loadData();
  },
});

// 初始化应用
export async function initApp() {
  Object.assign(systemInfo, await invoke<SystemT>("get_system_info"));
  tabsData.categoryList = await invoke<CategoryT[]>("get_categories");
  await loadData();
}

// 加载数据
export async function loadData() {
  try {
    const [items, count] = await Promise.all([
      invoke<SoftwareT[]>("get_software_by_category", {
        categoryId: Number(tabsData.activeId),
        keyword: searchData.keyword,
        page: pageData.pageIndex,
        pageSize: pageData.pageSize,
      }),
      invoke<number>("get_software_count", {
        categoryId: Number(tabsData.activeId),
        keyword: searchData.keyword,
      }),
    ]);
    list.value = items;
    pageData.total = count;
  } catch (err) {
    console.error(err);
  }
}

// 切换分页
export function changePage(p: number) {
  pageData.pageIndex = p;
  loadData();
}

// 安装应用
export async function installApp(id: string, pkg: string) {
  if (!pkg) return;
  try {
    await invoke("install_package", { softwareId: id, package: pkg });
    loadData();
  } catch {}
}
