#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use mysql::prelude::*;
use mysql::*;
use once_cell::sync::Lazy;
use serde::Serialize;
use std::sync::Mutex;
static POOL: Lazy<Mutex<Option<Pool>>> = Lazy::new(|| Mutex::new(None));
fn init_db() {
    let mut lock = POOL.lock().unwrap();
    if lock.is_some() {
        return;
    }
    let opts = Opts::from_url(&format!(
        "mysql://{}:{}@{}:{}/{}",
        "wangye", "Wy025871.", "182.92.221.228", 6603, "store"
    ))
    .unwrap();
    match Pool::new(opts) {
        Ok(p) => {
            println!("✅ 数据库连接成功");
            *lock = Some(p);
        }
        Err(e) => {
            eprintln!("❌ 数据库连接失败: {}", e);
        }
    }
}
fn get_conn() -> Result<PooledConn, String> {
    let lock = POOL.lock().unwrap();
    let pool = lock.as_ref().ok_or("数据库未连接")?;
    pool.get_conn().map_err(|e| e.to_string())
}
#[derive(Debug, Serialize, Clone)]
pub struct Category {
    pub id: u32,
    pub name: String,
    pub icon: Option<String>,
    pub description: Option<String>,
    pub sort: Option<u32>,
    pub created_time: Option<String>,
    pub updated_time: Option<String>,
    pub deleted_time: Option<String>,
}
#[derive(Debug, Serialize, Clone)]
pub struct Software {
    pub id: String,
    pub name: String,
    pub package: Option<String>,
    pub version: Option<String>,
    pub size: Option<String>,
    pub icon_url: Option<String>,
    pub download_count: Option<u32>,
    pub provider_department: Option<String>,
    pub provider: Option<String>,
    pub top: Option<u32>,
    pub status: Option<u32>,
    pub created_time: Option<String>,
    pub updated_time: Option<String>,
    pub deleted_time: Option<String>,
}
#[derive(Debug, Serialize, Clone)]
pub struct SystemInfo {
    pub name: String,
    pub major: i32,
    pub minor: i32,
    pub patch: i32,
    pub author: Option<String>,
    pub update_log: Option<String>,
    pub created_time: Option<String>,
    pub updated_time: Option<String>,
    pub deleted_time: Option<String>,
}
fn get_value<T>(row: &Row, i: usize) -> Option<T>
where
    T: FromValue,
{
    row.get_opt(i).transpose().ok().flatten()
}
#[tauri::command]
fn get_system_info() -> Result<SystemInfo, String> {
    let mut conn = get_conn()?;
    let info = conn
        .query_map(
            "SELECT name,major,minor,patch,author,update_log,created_time,updated_time,deleted_time
             FROM system_info WHERE deleted_time IS NULL ORDER BY id DESC LIMIT 1",
            |row: Row| SystemInfo {
                name: get_value(&row, 0).unwrap(),
                major: get_value(&row, 1).unwrap(),
                minor: get_value(&row, 2).unwrap(),
                patch: get_value(&row, 3).unwrap(),
                author: get_value(&row, 4),
                update_log: get_value(&row, 5),
                created_time: get_value(&row, 6),
                updated_time: get_value(&row, 7),
                deleted_time: get_value(&row, 8),
            },
        )
        .map_err(|e| e.to_string())?
        .into_iter()
        .next();
    Ok(info.unwrap_or(SystemInfo {
        name: "UOS内网应用商店".into(),
        major: 1,
        minor: 0,
        patch: 0,
        author: Some("wangye".into()),
        update_log: None,
        created_time: None,
        updated_time: None,
        deleted_time: None,
    }))
}
#[tauri::command]
fn get_categories() -> Result<Vec<Category>, String> {
    let mut conn = get_conn()?;
    let list: Vec<Category> = conn
        .query_map(
            "SELECT id,name,icon,description,sort,created_time,updated_time,deleted_time
             FROM category WHERE deleted_time IS NULL ORDER BY sort ASC",
            |row: Row| Category {
                id: get_value(&row, 0).unwrap(),
                name: get_value(&row, 1).unwrap(),
                icon: get_value(&row, 2),
                description: get_value(&row, 3),
                sort: get_value(&row, 4),
                created_time: get_value(&row, 5),
                updated_time: get_value(&row, 6),
                deleted_time: get_value(&row, 7),
            },
        )
        .map_err(|e| e.to_string())?;
    Ok(list)
}
#[tauri::command]
fn get_software(
    category_id: u32,
    keyword: String,
    page: u32,
    page_size: u32,
) -> Result<Vec<Software>, String> {
    let mut conn = get_conn()?;
    let offset = (page - 1) * page_size;
    let mut sql = "
        SELECT s.id,s.name,s.package,s.version,s.size,s.icon_url,s.download_count,
               s.provider_department,s.provider,s.top,s.status,
               s.created_time,s.updated_time,s.deleted_time
        FROM software s
        LEFT JOIN category2software c2s ON s.id = c2s.software_id
        WHERE s.deleted_time IS NULL AND s.status = 1 "
    .to_string();
    let mut params: Vec<Value> = Vec::new();
    if category_id > 0 {
        sql += " AND c2s.category_id = ? ";
        params.push(category_id.into());
    } else {
        sql += " AND s.top = 1 ";
    }
    if !keyword.is_empty() {
        sql += " AND s.name LIKE ? ";
        params.push(format!("%{keyword}%").into());
    }
    sql += " GROUP BY s.id ORDER BY s.top DESC, s.download_count DESC LIMIT ?, ?";
    params.push(offset.into());
    params.push(page_size.into());
    let list: Vec<Software> = conn
        .exec_map(&sql, params, |row: Row| Software {
            id: get_value(&row, 0).unwrap(),
            name: get_value(&row, 1).unwrap(),
            package: get_value(&row, 2),
            version: get_value(&row, 3),
            size: get_value(&row, 4),
            icon_url: get_value(&row, 5),
            download_count: get_value(&row, 6),
            provider_department: get_value(&row, 7),
            provider: get_value(&row, 8),
            top: get_value(&row, 9),
            status: get_value(&row, 10),
            created_time: get_value(&row, 11),
            updated_time: get_value(&row, 12),
            deleted_time: get_value(&row, 13),
        })
        .map_err(|e| e.to_string())?;
    Ok(list)
}
#[tauri::command]
fn get_software_count(category_id: u32, keyword: String) -> Result<u32, String> {
    let mut conn = get_conn()?;
    let mut sql = "
        SELECT COUNT(DISTINCT s.id)
        FROM software s
        LEFT JOIN category2software c2s ON s.id = c2s.software_id
        WHERE s.deleted_time IS NULL AND s.status = 1 "
    .to_string();
    let mut params: Vec<Value> = Vec::new();
    if category_id > 0 {
        sql += " AND c2s.category_id = ? ";
        params.push(category_id.into());
    } else {
        sql += " AND s.top = 1 ";
    }
    if !keyword.is_empty() {
        sql += " AND s.name LIKE ? ";
        params.push(format!("%{keyword}%").into());
    }
    let count: u32 = conn
        .exec_first(&sql, params)
        .map_err(|e| e.to_string())?
        .unwrap_or(0);
    Ok(count)
}
// ===================== 安装（图形密码弹窗）=====================
#[tauri::command]
async fn install_package(software_id: String, package: String) -> Result<String, String> {
    // 1. 执行安装（图形密码弹窗）
    let result = std::process::Command::new("pkexec")
        .arg("apt")
        .arg("install")
        .arg("-y")
        .arg(&package)
        .output()
        .map_err(|e| format!("启动授权失败：{e}"))?;
    // 2. 统计下载量 +1
    let mut conn = get_conn()?;
    let _ = conn.exec_drop(
        "UPDATE software SET download_count = download_count +1 WHERE id=?",
        params![software_id],
    );
    // 3. 返回日志
    let out = String::from_utf8_lossy(&result.stdout);
    let err = String::from_utf8_lossy(&result.stderr);
    Ok(format!("=== 输出 ===\n{out}\n=== 错误 ===\n{err}"))
}
// ======================================================
fn main() {
    init_db();
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_system_info,
            get_categories,
            get_software,
            get_software_count,
            install_package
        ])
        .run(tauri::generate_context!())
        .expect("启动失败");
}