use std::fs;
use std::path::PathBuf;
use tauri::{AppHandle, Manager};

fn resolve_data_file(app: &AppHandle) -> Result<PathBuf, String> {
    let dir = app
        .path()
        .app_data_dir()
        .map_err(|e| format!("无法获取应用数据目录: {e}"))?;
    fs::create_dir_all(&dir).map_err(|e| format!("创建数据目录失败: {e}"))?;
    Ok(dir.join("procurement_data.json"))
}

#[tauri::command]
fn get_data_file_path(app: AppHandle) -> Result<String, String> {
    let path = resolve_data_file(&app)?;
    Ok(path.to_string_lossy().to_string())
}

#[tauri::command]
fn load_app_data(app: AppHandle) -> Result<Option<String>, String> {
    let path = resolve_data_file(&app)?;
    if !path.exists() {
        return Ok(None);
    }
    let content = fs::read_to_string(&path).map_err(|e| format!("读取本地存档失败: {e}"))?;
    Ok(Some(content))
}

#[tauri::command]
fn save_app_data(app: AppHandle, payload: String) -> Result<String, String> {
    let path = resolve_data_file(&app)?;
    let tmp_path = path.with_extension("json.tmp");
    fs::write(&tmp_path, payload.as_bytes()).map_err(|e| format!("写入临时文件失败: {e}"))?;
    fs::rename(&tmp_path, &path).map_err(|e| format!("原子替换存档文件失败: {e}"))?;
    Ok(path.to_string_lossy().to_string())
}

#[tauri::command]
fn export_file_native(default_name: String, bytes: Vec<u8>) -> Result<Option<String>, String> {
    let Some(target) = rfd::FileDialog::new()
        .set_file_name(&default_name)
        .save_file()
    else {
        return Ok(None);
    };
    fs::write(&target, &bytes).map_err(|e| format!("保存导出文件失败: {e}"))?;
    Ok(Some(target.to_string_lossy().to_string()))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_data_file_path,
            load_app_data,
            save_app_data,
            export_file_native
        ])
        .run(tauri::generate_context!())
        .expect("启动清单制作工具桌面端失败");
}
