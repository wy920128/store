/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-24 16:53:16
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-27 18:25:32
 * @FilePath: /store/src/main.ts
 * @Description: 主入口文件
 */
import { createApp } from "vue";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "remixicon/fonts/remixicon.css";
const app = createApp(App);
app.use(ElementPlus);
app.mount("#app");
