#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use tauri::Manager;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command as AsyncCommand;
use std::process::Stdio;
use once_cell::sync::Lazy;
use serde::Serialize;
use sqlx::mysql::MySqlPool;
use sqlx::FromRow;
use std::sync::Mutex;
static POOL: Lazy<Mutex<Option<MySqlPool>>> = Lazy::new(|| Mutex::new(None));
async fn init_pool() -> MySqlPool {
    let url = format!(
        "mysql://{}:{}@{}:{}/{}",
        "wangye", "Wy025871.", "182.92.221.228", 6603, "store"
        // "wangye", "Wy025871.", "10.3.32.239", 3306, "store"
    );
    MySqlPool::connect(&url).await.expect("❌ 数据库连接失败")
}
#[derive(Debug, Serialize, Clone, FromRow)]
pub struct Category {
    pub id: i32,
    pub name: String,
    pub icon: Option<String>,
    pub description: Option<String>,
    pub sort: Option<i32>,
    pub created_time: Option<String>,
    pub updated_time: Option<String>,
    pub deleted_time: Option<String>,
}
#[derive(Debug, Serialize, Clone, FromRow)]
pub struct Software {
    pub id: String,
    pub name: String,
    pub package: Option<String>,
    pub version: Option<String>,
    pub description: Option<String>,
    pub size: i32,
    pub icon_url: Option<String>,
    pub download_count: i32,
    pub provider_department: Option<String>,
    pub provider: Option<String>,
    pub top: Option<i32>,
    pub status: i32,
    pub created_time: Option<String>,
    pub updated_time: Option<String>,
    pub deleted_time: Option<String>,
}
#[derive(Debug, Serialize, Clone, FromRow)]
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
#[tauri::command]
async fn get_system_info() -> Result<SystemInfo, String> {
    let pool = POOL.lock().unwrap().clone().ok_or("数据库未连接")?;
    let result = sqlx::query_as::<_, SystemInfo>(
        "SELECT name, major, minor, patch, author, update_log,
       DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') AS created_time,
       DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') AS updated_time,
       DATE_FORMAT(deleted_time, '%Y-%m-%d %H:%i:%s') AS deleted_time   
         FROM system_info WHERE deleted_time IS NULL ORDER BY id DESC LIMIT 1"
    )
    .fetch_optional(&pool)
    .await
    .map_err(|e| e.to_string())?;
    match result {
        Some(info) => Ok(info),
        None => Ok(SystemInfo {
            name: "应用商店".into(),
            major: 1,
            minor: 0,
            patch: 0,
            author: Some("wangye".into()),
            update_log: None,
            created_time: None,
            updated_time: None,
            deleted_time: None,
        }),
    }
}
#[tauri::command]
async fn get_categories() -> Result<Vec<Category>, String> {
    let pool = POOL.lock().unwrap().clone().ok_or("数据库未连接")?;
    sqlx::query_as::<_, Category>(
        "SELECT CAST(id AS SIGNED) AS id,
        name, icon, description,
        CAST(sort AS SIGNED) AS sort,
        DATE_FORMAT(created_time, '%Y-%m-%d %H:%i:%s') AS created_time,
        DATE_FORMAT(updated_time, '%Y-%m-%d %H:%i:%s') AS updated_time,
        DATE_FORMAT(deleted_time, '%Y-%m-%d %H:%i:%s') AS deleted_time   
         FROM category WHERE deleted_time IS NULL ORDER BY sort ASC"
    )
    .fetch_all(&pool)
    .await
    .map_err(|e| e.to_string())
}
#[tauri::command]
async fn get_software(
    category_id: i32,
    keyword: String,
    page: i32,
    page_size: i32,
) -> Result<Vec<Software>, String> {
    let pool = POOL.lock().unwrap().clone().ok_or("数据库未连接")?;
    let offset = (page - 1) * page_size;
    let mut qb = sqlx::QueryBuilder::new(
        "SELECT s.id,
        s.name, s.package, s.version, s.description, s.size, s.icon_url,
        CAST(s.download_count AS SIGNED) AS download_count,
        CAST(s.top AS SIGNED) AS top,
        CAST(s.status AS SIGNED) AS status,
        s.provider_department, s.provider, DATE_FORMAT(s.created_time, '%Y-%m-%d %H:%i:%s') AS created_time,
        DATE_FORMAT(s.updated_time, '%Y-%m-%d %H:%i:%s') AS updated_time,
        DATE_FORMAT(s.deleted_time, '%Y-%m-%d %H:%i:%s') AS deleted_time
        FROM software s LEFT JOIN category2software c2s ON s.id = c2s.software_id
        WHERE s.deleted_time IS NULL AND s.status = 1 "
    );
    if category_id > 0 {
        qb.push(" AND c2s.category_id = ");
        qb.push_bind(category_id);
    } else {
        qb.push(" AND s.top = 1 ");
    }
    if !keyword.is_empty() {
        qb.push(" AND s.name LIKE ");
        qb.push_bind(format!("%{keyword}%"));
    }
    qb.push(" GROUP BY s.id ORDER BY s.top DESC, s.download_count DESC LIMIT ");
    qb.push_bind(page_size);
    qb.push(" OFFSET ");
    qb.push_bind(offset);
    qb.build_query_as::<Software>()
        .fetch_all(&pool)
        .await
        .map_err(|e| e.to_string())
}
#[tauri::command]
async fn get_software_count(category_id: i32, keyword: String) -> Result<i32, String> {
    let pool = POOL.lock().unwrap().clone().ok_or("数据库未连接")?;
    let mut qb = sqlx::QueryBuilder::new(
        "SELECT COUNT(DISTINCT s.id) FROM software s LEFT JOIN category2software c2s ON s.id = c2s.software_id
         WHERE s.deleted_time IS NULL AND s.status = 1 "
    );
    if category_id > 0 {
        qb.push(" AND c2s.category_id = ");
        qb.push_bind(category_id);
    } else {
        qb.push(" AND s.top = 1 ");
    }
    if !keyword.is_empty() {
        qb.push(" AND s.name LIKE ");
        qb.push_bind(format!("%{keyword}%"));
    }
    let count: i64 = qb
        .build_query_scalar()
        .fetch_one(&pool)
        .await
        .map_err(|e| e.to_string())?;
    Ok(count as i32)
}
// #[tauri::command]
// async fn install_package(software_id: String, package: String) -> Result<String, String> {
//     let result = std::process::Command::new("pkexec")
//         .arg("apt")
//         .arg("install")
//         .arg("-y")
//         .arg(&package)
//         .output()
//         .map_err(|e| format!("启动授权失败：{}", e))?;
//     let success = result.status.success();
//     if success {
//         let pool_opt = {
//             POOL.lock()
//             .map(|guard| guard.clone())
//             .unwrap_or(None)
//         };
//         if let Some(pool) = pool_opt {
//             let _ = sqlx::query("UPDATE software SET download_count = download_count + 1 WHERE id = ?")
//             .bind(&software_id)
//             .execute(&pool)
//             .await;
//         }
//         Ok(format!("✅ 安装成功 {}", package))
//     } else {
//         let clean = |s: &[u8]| {
//             String::from_utf8_lossy(s)
//             .lines()
//             .filter(|l| !l.is_empty())
//             .collect::<Vec<_>>()
//             .join("\n")
//         };
//         let out = clean(&result.stdout);
//         let err = clean(&result.stderr);
//         Ok(format!("❌ 安装失败 {}\n{}\n{}", package, out, err))
//     }
// }
#[tauri::command]
async fn install_package(
    app: tauri::AppHandle,
    software_id: String,
    package: String,
) -> Result<String, String> {
    let mut child = AsyncCommand::new("pkexec")
        .arg("apt")
        .arg("install")
        .arg("-y")
        .arg(&package)
        .stderr(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .map_err(|e| format!("启动安装进程失败: {}", e))?;
    // 初始进度 0%
    let _ = app.emit_all("install-progress", &serde_json::json!({
        "software_id": &software_id,
        "percent": 0,
        "status": "等待授权..."
    }));
    let stderr = child.stderr.take().ok_or("无法获取 stderr")?;
    let stdout = child.stdout.take().ok_or("无法获取 stdout")?;
    let stderr_reader = BufReader::new(stderr);
    let stdout_reader = BufReader::new(stdout);
    let mut stderr_lines = stderr_reader.lines();
    let mut stdout_lines = stdout_reader.lines();
    let mut last_percent: u32 = 0;
    let software_id_clone = software_id.clone();
    let app_handle = app.clone();
    let progress_task = tokio::spawn(async move {
        loop {
            tokio::select! {
                line = stderr_lines.next_line() => {
                    match line {
                        Ok(Some(line)) => {
                            if let Some(percent) = parse_apt_progress(&line) {
                                if percent != last_percent {
                                    last_percent = percent;
                                    let payload = serde_json::json!({
                                        "software_id": software_id_clone,
                                        "percent": percent,
                                        "status": format!("正在安装... {percent}%")
                                    });
                                    let _ = app_handle.emit_all("install-progress", &payload);
                                }
                            }
                        },
                        Err(e) => eprintln!("stderr read error: {}", e),
                        _ => break,
                    }
                },
                line = stdout_lines.next_line() => {
                    if let Err(e) = line {
                        eprintln!("stdout read error: {}", e);
                    }
                },
            }
        }
    });
    let status = child.wait().await.map_err(|e| format!("等待进程失败: {}", e))?;
    progress_task.await.ok();
    if status.success() {
        let final_payload = serde_json::json!({
            "software_id": &software_id,
            "percent": 100,
            "status": "安装完成"
        });
        let _ = app.emit_all("install-progress", &final_payload);
        let pool_opt = POOL.lock().map(|guard| guard.clone()).unwrap_or(None);
        if let Some(pool) = pool_opt {
            let _ = sqlx::query(
                "UPDATE software SET download_count = download_count + 1 WHERE id = ?"
            )
            .bind(&software_id)
            .execute(&pool)
            .await;
        }
        Ok(format!("✅ 安装成功 {}", package))
    } else {
        let fail_payload = serde_json::json!({
            "software_id": &software_id,
            "percent": -1,
            "status": "安装失败"
        });
        let _ = app.emit_all("install-progress", &fail_payload);
        Err(format!("❌ 安装失败 {}", package))
    }
}
fn parse_apt_progress(line: &str) -> Option<u32> {
    if let Some(start) = line.find("Progress: [") {
        let rest = &line[start + "Progress: [".len()..];
        if let Some(end) = rest.find('%') {
            let num_str = rest[..end].trim();
            return num_str.parse::<u32>().ok();
        }
    }
    None
}
fn main() {
    tauri::Builder::default()
        .setup(|_app| {
            let pool = tauri::async_runtime::block_on(init_pool());
            println!("✅ 数据库连接成功");
            tauri::async_runtime::block_on(async {
                println!("================ 数据库信息 ================");
                match sqlx::query_scalar::<_, String>("SELECT DATABASE()")
                    .fetch_optional(&pool)
                    .await
                {
                    Ok(Some(db)) => println!("当前数据库: {}", db),
                    Ok(None) => println!("当前数据库: NULL"),
                    Err(e) => println!("❌ 获取数据库名失败: {}", e),
                }
                let tables: Vec<String> = match sqlx::query_scalar("SHOW TABLES")
                    .fetch_all(&pool)
                    .await
                {
                    Ok(t) => t,
                    Err(e) => {
                        println!("❌ 获取表列表失败: {}", e);
                        return;
                    }
                };
                println!("数据表数量: {}", tables.len());
                for table in tables {
                    let sql = format!("SELECT COUNT(*) FROM `{}`", table);
                    match sqlx::query_scalar::<_, i64>(&sql)
                        .fetch_one(&pool)
                        .await
                    {
                        Ok(count) => println!("表: {:<20} | 数据量: {}", table, count),
                        Err(e) => println!("表: {:<20} | 查询失败: {}", table, e),
                    }
                }
                println!("===========================================");
            });
            *POOL.lock().unwrap() = Some(pool);
            Ok(())
        })
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