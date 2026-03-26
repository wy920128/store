/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-26 17:00:30
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-26 17:00:39
 * @FilePath: /store/src/types/system.d.ts
 * @Description: 系统信息接口
 */
export interface SystemInfo {
  name: string;
  major: number;
  minor: number;
  patch: number;
  author: string;
  update_log?: string;
  created_time?: string;
  updated_time?: string;
  deleted_time?: string;
}
