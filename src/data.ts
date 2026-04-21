import { ref, reactive } from 'vue';
import { invoke } from '@tauri-apps/api/tauri';
import type { Category, LogInfo, Software, SystemInfo } from './type'
export const systemData = ref<SystemInfo>({
    name: `应用商店`,
    major: 1,
    minor: 0,
    patch: 0,
    author: `王野`,
    update_log: null,
    created_time: null,
    updated_time: null,
    deleted_time: null,
});
// 搜索
export const searchData = reactive({
    keyword: ``,
    funcSearch: async () => {
        tabsData.funcTabChange(tabsData.activeId);
    },
});
// 分类 & 应用列表
export const tabsData = reactive({
    activeId: `0`,
    categoryList: [] as Category[],
    softwareList: [] as Software[],
    async funcTabChange(tab: string | number) {
        const cid: number = Number(tab);
        console.log(tab, cid);
        tabsData.activeId = cid.toString();
        pageData.pageIndex = 1;
        await loadList(cid);
    },
});
// 分页
export const pageData = reactive({
    pageIndex: 1,
    pageSize: 12,
    total: 0,
    async funcPageChange() {
        await loadList(Number(tabsData.activeId));
    },
});
// 安装日志
export const installLog = ref<LogInfo[]>([]);
// 加载应用列表
export async function loadList(categoryId: number) {
    const list: Software[] = await invoke(`get_software`, {
        categoryId: categoryId,
        keyword: searchData.keyword,
        page: pageData.pageIndex,
        pageSize: pageData.pageSize,
    });
    const total: number = await invoke(`get_software_count`, {
        categoryId: categoryId,
        keyword: searchData.keyword,
    });
    tabsData.softwareList = list;
    pageData.total = total;
}
// 安装应用
export async function handleInstall(id: string, pkg: string | undefined) {
    if (!pkg) {
        installLog.value.push({ type: "error", message: `❌ 无包名` });
        return;
    }
    installLog.value.push({ type: "info", message: `正在安装：${pkg}\n请在弹出密码框输入密码...\n\n` });
    try {
        const log: string = await invoke(`install_package`, {
            software_id: id,
            package: pkg,
        });
        installLog.value.push({ type: "info", message: log });
    } catch (e) {
        installLog.value.push({ type: "error", message: `❌ 错误：${e}` });
    }
}
// 防抖搜索
let timer: any;
export function debounceSearch() {
    clearTimeout(timer);
    timer = setTimeout(() => searchData.funcSearch(), 500);
}
// 初始化
export async function initApp() {
    systemData.value = await invoke(`get_system_info`);
    tabsData.categoryList = await invoke(`get_categories`);
    tabsData.funcTabChange(`0`);
}