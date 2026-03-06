/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-05 16:36:44
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-05 16:52:40
 * @FilePath: /store/app/types/software.ts
 * @Description: 软件类型定义
 */

import type { TimeStamp } from ".";

export interface Software {
  id: number; // 软件主键ID
  name: string; // 软件名称（唯一）
  version: string | null; // 软件版本
  size: string | null; // 软件大小
  download_url: string; // 软件下载地址
  provider_department: string | null; // 供应者部门
  provider: string | null; // 软件者应商
}

export interface SoftwareRes extends Software, TimeStamp {}
