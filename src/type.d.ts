/*
 * @Author: wangye 18545455617@163.com
 * @Date: 2026-04-20 16:30:23
 * @LastEditors: wangye 18545455617@163.com
 * @LastEditTime: 2026-04-21 15:09:45
 * @FilePath: /store/src/type.d.ts
 * @Description: 数据类型定义
 */
// 分类信息
export interface Category {
  id: number
  name: string
  icon: string | null
  description: string | null
  sort: number | null
  created_time: string | null
  updated_time: string | null
  deleted_time: string | null
}

// 应用信息
export interface Software {
  id: string
  name: string
  description: string | null
  package: string
  version: string | null
  size: string | null
  icon_url: string | null
  download_count: number | null
  provider_department: string | null
  provider: string | null
  top: number | null
  status: number | null
  created_time: string | null
  updated_time: string | null
  deleted_time: string | null
}

// 系统信息
export interface SystemInfo {
  name: string
  major: number
  minor: number
  patch: number
  author: string | null
  update_log: string | null
  created_time: string | null
  updated_time: string | null
  deleted_time: string | null
}

// 日志信息
export interface LogInfo {
  type: `info` | `error`;
  message: string;
}