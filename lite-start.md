Open WebUI Lite – 本地启动流程（前后端分离）
================================================

前置要求
- Python 3.11+（已用 `.venv` 配好）
- Node.js 22.x
- 仓库路径：`D:\Documents\open-webui-lite\open-webui`

一次性准备（首次拉仓库或依赖更新后执行）
1) 进入项目根目录并激活虚拟环境  
   `.\.venv\Scripts\activate`
2) 确保后端依赖已装（已做过可跳过）  
   `pip install -e .`
3) 安装前端依赖（已做过可跳过）  
   `npm install`

启动后端（新终端或在激活后的同一终端）
1) 激活虚拟环境：`.\.venv\Scripts\activate`
2) 可选：禁用不需要的重量功能，减少噪音  
   ```
   set ENABLE_WEB_SEARCH=false
   set BYPASS_EMBEDDING_AND_RETRIEVAL=true
   set ENABLE_OLLAMA_API=false
   set CORS_ALLOW_ORIGIN=http://localhost:5173
   ```
3) 启动服务（推荐命令）：  
   `.\.venv\Scripts\open-webui serve --host 0.0.0.0 --port 8080`
   （若脚本名为 `open-webui.exe`，同理运行）
4) 健康检查：`http://localhost:8080/health` 应返回 `{"status": true}`；API 文档：`http://localhost:8080/docs`

启动前端（单独终端）
1) 进入项目根目录：`cd D:\Documents\open-webui-lite\open-webui`
2) 运行开发服务：`npm run dev -- --host --port 5173`
3) 浏览器访问：`http://localhost:5173`

常见排查
- 浏览器提示后端未启动：确保后端命令在运行，`/health` 正常；检查端口占用，必要时调整 `--port` 并同步前端指向的后端地址。
- CORS 问题：确认后端环境变量 `CORS_ALLOW_ORIGIN` 包含前端地址（如 `http://localhost:5173`）。
- 端口冲突：用 `netstat -ano | findstr :8080` / `:5173` 找占用进程，结束或改用其他端口并同步配置。

验证顺序
1) 后端先跑通 `/health`
2) 前端再打开 `http://localhost:5173`
3) 如仍有问题，记录终端报错和浏览器 Network 面板信息再排查。

Docker 启动（可选，前后端分离）
- 构建并启动：`docker-compose up --build`
- 访问：后端 `http://localhost:8080/health`，前端 `http://localhost:5173`
- 需要调整环境变量（如端口/CORS/功能开关）时，可在 `docker-compose.yml` 的 `environment` 中修改。
