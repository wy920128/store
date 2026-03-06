/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-05 16:55:29
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-05 16:55:52
 * @FilePath: /store/app/types/classify2software.ts
 * @Description: 分类关联软件类型定义
 */
import type { TimeStamp } from ".";

export interface Classify2Software {
  classify_id: number; // 分类ID
  software_id: number; // 软件ID
}

export interface Classify2SoftwareRes extends Classify2Software, TimeStamp {}
