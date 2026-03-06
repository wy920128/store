// server/utils/db.ts
import * as mariadb from "mariadb";
import { Pool, PoolConnection } from "mariadb";
import type { PoolConfig } from "mariadb";

const runtimeConfig = useRuntimeConfig();
const poolConfig: PoolConfig = {
  host: runtimeConfig.db.host,
  user: runtimeConfig.db.user,
  password: runtimeConfig.db.password,
  database: runtimeConfig.db.database,
  port: parseInt(runtimeConfig.db.port!),
  connectionLimit: 10,
  connectTimeout: 5000,
  multipleStatements: false,
  rowsAsArray: false,
};
const pool: Pool = mariadb.createPool(poolConfig);

export const getConnection = async (): Promise<PoolConnection> => {
  try {
    return await pool.getConnection();
  } catch (error) {
    throw new Error(
      `数据库连接失败 [${runtimeConfig.db_aliyun.dbHost}]: ${error}`,
    );
  }
};

const safeNormalizeResult = (result: any) => {
  // 如果结果是数组，直接返回
  if (Array.isArray(result)) {
    return result;
  }
  // 如果结果是对象且有 insertId/lastInsertId，说明是插入操作
  if (result && typeof result === "object") {
    // 检查是否是MariaDB的ResultSet对象
    if (result.insertId !== undefined || result.affectedRows !== undefined) {
      return result;
    }
    // 如果是普通对象，包装成数组（单行查询结果）
    return [result];
  }
  // 其他情况返回空数组
  console.warn("无法识别的查询结果格式:", typeof result, result);
  return [];
};

const execute = async (
  sql: string,
  params: any[] = [],
  conn?: PoolConnection,
) => {
  let connection: PoolConnection | null = conn || null;
  const isExternalConn = !!conn;
  try {
    if (!connection) connection = await getConnection();
    // 使用更安全的查询方式
    const result = await connection.query(sql, params);
    // 修复：确保返回格式统一，避免迭代器错误
    return safeNormalizeResult(result);
  } catch (error) {
    console.error("SQL执行错误:", {
      sql: sql.substring(0, 200),
      params,
      error: error instanceof Error ? error.message : String(error),
    });
    throw new Error(`SQL执行失败: ${(error as Error).message}`);
  } finally {
    if (connection && !isExternalConn) connection.release();
  }
};

export async function utilsQuery<T = any>(
  sql: string,
  params: any[] = [],
  conn?: PoolConnection,
): Promise<T[]> {
  const result = await execute(sql, params, conn);
  // 确保返回的是数组
  if (Array.isArray(result)) {
    return result as T[];
  }
  // 如果是单个对象，包装成数组
  if (result && typeof result === "object") {
    return [result] as T[];
  }
  return [] as T[];
}
