/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-04 16:35:26
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-05 14:53:46
 * @FilePath: /store/nuxt.config.ts
 * @Description: 前端nuxt配置文件
 */
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: `2025-07-15`,
  css: [`element-plus/dist/index.css`],
  devServer: {
    port: 3000 // 前端运行端口
  },
  devtools: { enabled: true },
  modules: [`@element-plus/nuxt`],
  runtimeConfig: {
    db: {
      host: process.env.DB_HOST,
      port: process.env.DB_PORT,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_DATABASE,
    }
  }
});
