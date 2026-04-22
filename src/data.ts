/*
 * @Author: wangye 18545455617@163.com
 * @Date: 2026-04-20 16:27:48
 * @LastEditors: wangye 18545455617@163.com
 * @LastEditTime: 2026-04-21 15:10:14
 * @FilePath: /store/src/data.ts
 * @Description: 数据管理
 */
import { ref, reactive, type Ref } from 'vue';
import { invoke } from '@tauri-apps/api/tauri';
import type { Category, LogInfo, Software, SystemInfo } from './type'
export const systemData: Ref<SystemInfo> = ref<SystemInfo>({
    name: `应用商店`,
    major: 0,
    minor: 0,
    patch: 1,
    author: `王野`,
    update_log: null,
    created_time: null,
    updated_time: null,
    deleted_time: null,
});
export const searchData: {
    keyword: string;
    funcSearch: () => Promise<void>;
} = reactive({
    keyword: ``,
    funcSearch: async () => {
        tabsData.funcTabChange(tabsData.activeId);
    },
});
export const tabsData: {
    activeId: string;
    categoryList: Category[];
    softwareList: Software[];
    funcTabChange: (tab: string | number) => Promise<void>;
} = reactive({
    activeId: `0`,
    categoryList: [
        {
            id: 0,
            name: `首页`,
            icon: `ri-apps-2-line`,
            description: null,
            sort: null,
            created_time: null,
            updated_time: null,
            deleted_time: null,
        }
    ],
    softwareList: [],
    async funcTabChange(tab: string | number) {
        const cid: number = Number(tab);
        console.log(tab, cid);
        tabsData.activeId = cid.toString();
        pageData.pageIndex = 1;
        await loadList(cid);
    },
});
export const pageData: {
    pageIndex: number;
    pageSize: number;
    total: number;
    funcPageChange: () => Promise<void>;
} = reactive({
    pageIndex: 1,
    pageSize: 6,
    total: 0,
    async funcPageChange() {
        await loadList(Number(tabsData.activeId));
    },
});
export const installLog: Ref<LogInfo[]> = ref<LogInfo[]>([]);
async function loadList(categoryId: number) {
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
export async function handleInstall(id: string, pkg: string) {
    if (!pkg) {
        installLog.value.push({ type: "error", message: `❌ 无包名` });
        return;
    }
    installLog.value.push({ type: "info", message: `正在安装：${pkg}\n请在弹出密码框输入密码...\n\n` });
    try {
        const log: string = await invoke(`install_package`, {
            softwareId: id,
            package: pkg,
        });
        installLog.value.push({ type: "info", message: log });
    } catch (e) {
        installLog.value.push({ type: "error", message: `❌ 错误：${e}` });
    }
}
let timer: any;
export function debounceSearch() {
    clearTimeout(timer);
    timer = setTimeout(() => searchData.funcSearch(), 500);
}
export async function initApp() {
    systemData.value = await invoke(`get_system_info`);
    const apiCategories: Category[] = await invoke(`get_categories`);
    tabsData.categoryList = [...tabsData.categoryList, ...apiCategories];
    tabsData.funcTabChange(`0`);
}