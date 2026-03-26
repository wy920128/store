/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-24 16:53:16
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-25 08:18:26
 * @FilePath: /store/src/vite-env.d.ts
 * @Description: vite 环境变量类型声明文件
 */
/// <reference types="vite/client" />
declare module "vue-devui";
declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
