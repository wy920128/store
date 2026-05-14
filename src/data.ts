/*
 * @Author: wangye 18545455617@163.com
 * @Date: 2026-04-21 11:01:53
 * @LastEditors: wangye 18545455617@163.com
 * @LastEditTime: 2026-05-13 17:59:51
 * @FilePath: /store/src/data.ts
 * @Description: 数据管理
 */
import { ref, reactive, type Ref } from "vue";
import { invoke } from "@tauri-apps/api/tauri";
import type { Category, LogInfo, Software, SystemInfo } from "./type";
import { ElMessage } from "element-plus";
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
    timer: ReturnType<typeof setTimeout>;
    funcSearch: () => Promise<void>;
} = reactive({
    keyword: ``,
    timer: 0,
    funcSearch: async () => {
        clearTimeout(searchData.timer);
        searchData.timer = setTimeout(() => {
            logData.addLog(`info`, `搜索：「${searchData.keyword || `无`}」`);
            tabsData.funcTabChange(tabsData.activeId);
        }, 500);
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
        },
    ],
    softwareList: [],
    async funcTabChange(tab: string | number) {
        const cid: number = Number(tab);
        tabsData.activeId = cid.toString();
        pageData.pageIndex = 1;
        // logData.addLog(`info`, `切换到分类：${cid}`);
        await globalData.loadList(cid);
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
        // logData.addLog(`info`, `翻到第 ${this.pageIndex} 页`);
        await globalData.loadList(Number(tabsData.activeId));
    },
});
export const logData = reactive<{
    logs: LogInfo[];
    addLog: (type: `info` | `error`, msg: string) => void;
}>({
    logs: [],
    addLog(type, msg) {
        const prefix = type === `info` ? `✅` : `❌`;
        this.logs.push({ type, message: `${prefix} ${msg}` });
    },
});
export const globalData: {
    installingId: string | null;
    installProgress: Record<string, {
        percent: number;
        status: string;
    }>;
    formatSize(size: string | null | undefined): string;
    loadList: (categoryId: number) => Promise<void>;
    handleInstall: (id: string, pkg: string, name: string) => Promise<void>;
} = reactive({
    installingId: null,
    installProgress: {},
    formatSize(size: string | null | undefined): string {
        if (!size) return '-';
        const bytes = parseInt(size, 10);
        if (isNaN(bytes)) return '-';
        const KB = 1024;
        const MB = KB * 1024;
        const GB = MB * 1024;
        if (bytes >= GB) return `${(bytes / GB).toFixed(2)} GB`;
        if (bytes >= MB) return `${(bytes / MB).toFixed(2)} MB`;
        if (bytes >= KB) return `${(bytes / KB).toFixed(2)} KB`;
        return `${bytes} B`;
    },
    async loadList(categoryId: number) {
        try {
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
            tabsData.softwareList = list.map(software => ({
                ...software,
                size: globalData.formatSize(software.size)
            }));;
            pageData.total = total;
            // logData.addLog(`info`, `加载应用列表：${total} 条`);
        } catch (err) {
            logData.addLog(`error`, `加载失败：${err}`);
            tabsData.softwareList = [];
            pageData.total = 0;
        }
    },
    async handleInstall(id: string, pkg: string, name: string) {
        if (!pkg) {
            logData.addLog(`error`, `安装失败：软件包名为空`);
            return;
        }
        if (globalData.installingId) {
            ElMessage.warning(`已有安装任务在进行中，请稍后`);
            return;
        }
        globalData.installingId = id;
        logData.addLog(`info`, `开始安装 ${name}，等待授权...`);
        invoke(`install_package`, {
            softwareId: id,
            package: pkg,
        }).catch(e => {
            logData.addLog(`error`, `安装异常：${e}`);
            ElMessage.error(`${name} 安装出错：${e}`);
            globalData.installingId = null;   // 出错时恢复按钮
        });
    },
});
export async function initApp() {
    logData.addLog(`info`, `========== 应用初始化开始 ==========`);
    try {
        const info = await invoke<SystemInfo>(`get_system_info`);
        systemData.value = info;
        // logData.addLog(
        //     `info`,
        //     `系统：${info.name} v${info.major}.${info.minor}.${info.patch}`,
        // );
        const apiCategories: Category[] =
            await invoke<Category[]>(`get_categories`);
        tabsData.categoryList = [{
            id: 0,
            name: `首页`,
            icon: `ri-apps-2-line`,
            description: null,
            sort: null,
            created_time: null,
            updated_time: null,
            deleted_time: null,
        }, ...apiCategories];
        // logData.addLog(
        //     `info`,
        //     `分类加载完成：${tabsData.categoryList.map((c) => c.name).join(`、`)}`,
        // );
        await tabsData.funcTabChange(`0`);
        logData.addLog(`info`, `初始化完成 ✅`);
    } catch (e) {
        logData.addLog(`error`, `初始化失败：${e}`);
    }
    logData.addLog(`info`, `========== 应用初始化结束 ==========`);
}
