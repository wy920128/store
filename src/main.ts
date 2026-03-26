/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-24 16:53:16
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-25 08:17:41
 * @FilePath: /store/src/main.ts
 * @Description: 主入口文件
 */
import { createApp } from "vue";
import App from "./App.vue";

// DevUI
import "vue-devui/style.css";
import "@devui-design/icons/icomoon/devui-icon.css";
import DevUI from "vue-devui";

createApp(App).use(DevUI).mount(`#app`);
