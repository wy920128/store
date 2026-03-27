import { reactive } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { CategoryT, SoftwareT, SystemT } from "./types";
import { TabsPaneContext } from "element-plus";
// 系统数据
export const systemData: {
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
// 搜索数据
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
// 标签页数据
export const tabsData: {
  activeId: string;
  category0: CategoryT;
  categoryList: CategoryT[];
  softwareList: SoftwareT[];
  funcTabChange: (tab: TabsPaneContext) => void;
  funcInstall: (id: string, pkg: string) => void;
} = reactive({
  activeId: `0`,
  category0: {
    id: 0,
    name: `首页`,
    sort: 0,
    icon: `ri-home-9-line`,
    description: `首页推荐应用`,
    created_time: `2026-03-27 14:20:46`,
    updated_time: `2026-03-27 14:20:46`,
    deleted_time: null,
  },
  categoryList: [],
  softwareList: [],
  funcTabChange(tab: TabsPaneContext) {
    tabsData.activeId = String(tab.props.name);
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
// 分页
export const pageData = reactive({
  total: 0,
  pageIndex: 1,
  pageSize: 6,
  funcPageChange(page: number) {
    pageData.pageIndex = page;
    loadData();
  },
});
// 加载数据
export async function loadData() {
  try {
    console.log(searchData.keyword)
    const [items, count] = await Promise.all([
      invoke<SoftwareT[]>("get_software", {
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
    tabsData.softwareList = items;
    pageData.total = count;
  } catch (err) {
    console.error(err);
  }
}
// 初始化应用
export async function initApp() {
  Object.assign(systemData, await invoke<SystemT>("get_system_info"));
  tabsData.categoryList = [
    tabsData.category0,
    ...(await invoke<CategoryT[]>("get_categories")),
  ];
  await loadData();
}
