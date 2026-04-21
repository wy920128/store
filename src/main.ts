/*
 * @Author: wangye 18545455617@163.com
 * @Date: 2026-04-20 14:45:03
 * @LastEditors: wangye 18545455617@163.com
 * @LastEditTime: 2026-04-21 09:21:46
 * @FilePath: /store/src/main.ts
 * @Description: 应用商店主程序
 */
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import "remixicon/fonts/remixicon.css";

createApp(App).use(ElementPlus).mount('#app')
