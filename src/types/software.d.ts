/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-26 16:59:30
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-26 16:59:36
 * @FilePath: /store/src/types/software.d.ts
 * @Description: 软件接口
 */
export interface Software {
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
  created_time?: string;
  updated_time?: string;
  deleted_time?: string;
}
