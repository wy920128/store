/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-26 16:58:48
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-26 16:58:57
 * @FilePath: /store/src/types/category.d.ts
 * @Description: 分类接口
 */
export interface Category {
  id: number;
  name: string;
  icon?: string;
  description?: string;
  sort?: number;
  created_time?: string;
  updated_time?: string;
  deleted_time?: string;
}
