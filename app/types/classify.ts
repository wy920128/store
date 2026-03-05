/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-05 16:36:44
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-05 16:44:58
 * @FilePath: /store/app/types/classify.ts
 * @Description: 分类类型定义
 */

import type { TimeStamp } from ".";

export interface Classify {
  id: number; // 分类主键ID
  name: string; // 分类名称（唯一）
  description: string | null; // 分类描述
}

export interface ClassifyRes extends Classify, TimeStamp {}
