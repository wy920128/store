/*
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-05 14:38:42
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-05 17:10:35
 * @FilePath: /store/server/api/classify/get.ts
 * @Description: 获取分类列表
 */
import type { ClassifyRes, Res } from "~/types";
import { utilsQuery } from "~/server/utils/db";
export default defineEventHandler(
  async (event): Promise<Res<ClassifyRes[]>> => {
    try {
      // 基础 SQL - 修正分类条件位置
      let selectSql = `
      SELECT DISTINCT
        c.id,
        c.name,
        c.description,
        c.created_time,
        c.updated_time
      FROM classify c
      WHERE c.deleted_time IS NULL
    `;
      // 计数 SQL - 必须与查询SQL保持相同的过滤条件
      let countSql = `
      SELECT COUNT(DISTINCT c.id) as total 
      FROM classify c
      WHERE c.deleted_time IS NULL
    `;
      const classifyList: ClassifyRes[] = await utilsQuery(selectSql);
      const countResult = await utilsQuery(countSql);
      const total = Number((countResult as any[])[0]?.total) || 0;
      return {
        code: 200,
        data: {
          list: classifyList,
          pagination: {
            page: 1,
            pageSize: 10,
            total,
            totalPages: Math.ceil(total / 10),
          },
        },
        message: `查询成功，共 ${total} 条记录`,
        success: true,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      return {
        code: 500,
        data: {
          list: [],
          pagination: {
            page: 1,
            pageSize: 1,
            total: 1,
            totalPages: 1,
          },
        },
        message: error instanceof Error ? error.message : String(error),
        success: false,
        timestamp: new Date().toISOString(),
      };
    }
  },
);
