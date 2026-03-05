/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-05 15:39:19
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-05 17:09:58
 * @FilePath: /store/app/types/index.ts
 * @Description: 全局类型定义
 */

export * from "./classify";
export * from "./software";
export * from "./classify2software";

export interface TimeStamp {
  created_time: string; // 创建时间（格式：YYYY-MM-DD HH:mm:ss）
  updated_time: string; // 更新时间（格式：YYYY-MM-DD HH:mm:ss）
  deleted_time: string | null; // 软删除标记（null=未删除，非null=删除时间）
}

export interface Res<T = any> {
  // 状态码 (通常200或0表示成功)
  code: number;
  // 响应消息 (成功或错误信息)
  message: string;
  // 核心响应数据 (使用泛型)
  data: {
    list: T;
    pagination: {
      page: number; // 当前页码
      pageSize: number; // 每页大小
      total: number; // 总数
      totalPages: number; // 总页数
    };
  };
  success: boolean;
  // 可选字段：分页信息 (对于列表数据)
  pagination?: {
    current: number; // 当前页码
    pageSize: number; // 每页大小
    total: number; // 总数
    totalPages: number; // 总页数
  };
  // 可选字段：时间戳
  timestamp: string;
}
