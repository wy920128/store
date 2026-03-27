/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-27 14:20:46
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-27 16:33:07
 * @FilePath: /store/src/types/index.d.ts
 * @Description: 接口定义
 */
export interface CategoryT {
  id: number;
  name: string;
  icon: string;
  description: string;
  sort: number;
  created_time: string;
  updated_time: string;
  deleted_time: string | null;
}
export interface SoftwareT {
  id: string;
  name: string;
  package: string;
  version: string;
  size: string;
  icon_url: string;
  download_count: number;
  provider_department: string;
  provider: string;
  top: number;
  created_time: string;
  updated_time: string;
  deleted_time: string | null;
}
export interface SystemT {
  name: string;
  major: number;
  minor: number;
  patch: number;
  author: string;
  update_log: string;
  created_time: string;
  updated_time: string;
  deleted_time: string | null;
}