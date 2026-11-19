# 清单制作工具桌面客户端（Rust + Tauri 2）

本客户端基于 **Rust + Tauri 2** 构建，界面与最新网页版完全一致，所有单据、独立存档与历史快照均由 Rust 后端直接以原子写入方式保存在系统本地磁盘（`procurement_data.json`），彻底避免浏览器清理缓存导致数据丢失。

## 目录结构

- `src-tauri/src/lib.rs`：Rust 本地持久化与原生文件导出命令（`load_app_data`、`save_app_data`、`get_data_file_path`、`export_file_native`）
- `src-tauri/src/main.rs`：桌面端入口
- `src-tauri/tauri.conf.json`：Tauri 2 窗口与打包配置
- `dist/index.html`：前端单据录入、分页、Excel/PDF 导出界面（已内置 Tauri 原生桥接）

## 本地编译与运行

1. 安装 [Rust 工具链](https://www.rust-lang.org/tools/install)（含 `cargo`）。
2. Windows 需确保已安装系统自带的 WebView2 Runtime（Win10/Win11 通常已预装）。
3. 安装 Tauri CLI：
   ```bash
   cargo install tauri-cli --version "^2"
   ```
4. 在项目根目录运行调试或打包：
   ```bash
   # 开发模式启动客户端
   cargo tauri dev

   # 打包生成独立安装包（Windows 下生成 .exe / .msi）
   cargo tauri build
   ```
