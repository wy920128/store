/**
 * 分类信息
 * 对应 Rust Category
 */
export interface Category {
  id: number
  name: string
  icon: string | null
  description: string | null
  sort: number | null
  created_time: string | null
  updated_time: string | null
  deleted_time: string | null
}

/**
 * 应用信息
 * 对应 Rust Software
 */
export interface Software {
  id: string
  name: string
  package: string | null
  version: string | null
  size: string | null
  icon_url: string | null
  download_count: number | null
  provider_department: string | null
  provider: string | null
  top: number | null
  status: number | null
  created_time: string | null
  updated_time: string | null
  deleted_time: string | null
}

/**
 * 系统信息
 * 对应 Rust SystemInfo
 */
export interface SystemInfo {
  name: string
  major: number
  minor: number
  patch: number
  author: string | null
  update_log: string | null
  created_time: string | null
  updated_time: string | null
  deleted_time: string | null
}

/**
 * 日志信息
 * 对应 Rust LogInfo
 */
export interface LogInfo {
  type: `info` | `error`;
  message: string;
}