# 清单制作工具桌面客户端（Rust + Tauri 2）

本客户端基于 **Rust + Tauri 2** 构建，界面与最新网页版完全一致，所有单据、独立存档与历史快照均由 Rust 后端直接以原子写入方式保存在系统本地磁盘（`procurement_data.json`），彻底避免浏览器清理缓存导致数据丢失。

## 目录结构

- `src-tauri/src/lib.rs`：Rust 本地持久化与原生文件导出命令（`load_app_data`、`save_app_data`、`get_data_file_path`、`export_file_native`）
- `src-tauri/src/main.rs`：桌面端入口
- `src-tauri/tauri.conf.json`：Tauri 2 窗口与打包配置（`decorations: false`，无边框窗口）
- `src-tauri/icons/`：应用图标（由 `scripts/make_icons.py` 生成）
- `dist/index.html`：前端单据录入、分页、Excel/PDF 导出界面（已内置 Tauri 原生桥接与右上角窗口按钮）
- `.github/workflows/build-windows.yml`：GitHub Actions 自动编译 Windows exe

## 无边框窗口与右上角按钮

系统标题栏已关闭（`decorations: false`），窗口为普通直角无边框窗口：

- 窗口按钮：最小化 / 最大化（还原）/ 关闭，浮动在窗口右上角、覆盖在深色工具栏之上（`#win-controls`）
- 拖拽移动：深色工具栏整条为拖拽区（`data-tauri-drag-region`），双击空白处由 Tauri 原生切换最大化
- 滚动条：桌面端隐藏（`html.is-tauri` 下 `::-webkit-scrollbar` 置零），滚轮与触控板滚动不受影响
- 仅在桌面端启用（检测到 `window.__TAURI__` 时给 `<html>` 与 `<body>` 加 `is-tauri`），浏览器打开时按钮自动隐藏、滚动条正常显示

## 在 GitHub 上编译 exe

推送代码到 `main` 分支（或在 Actions 页面手动 `Run workflow`）后，工作流 `Build Windows EXE` 会在 `windows-latest` 上自动编译，产物位于该次运行的 **Artifacts → ProcurementListTool-windows-x64**：

| 文件 | 说明 |
| --- | --- |
| `ProcurementListTool.exe` | 免安装单文件，双击即用（依赖系统 WebView2，Win10/11 一般已预装） |
| `ProcurementListTool_1.0.0_x64-setup.exe` | NSIS 安装包，会创建开始菜单快捷方式 |

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
