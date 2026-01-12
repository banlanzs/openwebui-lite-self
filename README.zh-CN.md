# Open WebUI Lite 👋

> **[!NOTE]**
> **这是 Open WebUI 的 Lite 精简版本** - 专为本地开发优化的前后端分离版本。如需完整的生产版本，请访问 [open-webui/open-webui](https://github.com/open-webui/open-webui)。

**Open WebUI 是一个[可扩展](https://docs.openwebui.com/features/plugin/)、功能丰富、用户友好的自托管 AI 平台，专为完全离线运行而设计。** 它支持各种 LLM 运行器，如 **Ollama** 和 **OpenAI 兼容的 API**，并具有**用于 RAG 的内置推理引擎**，使其成为一个**强大的 AI 部署解决方案**。


## 本地开发（Lite 版本）💻

这是 Lite 版本，采用前后端分离架构，专为本地开发而设计。

### 前置要求

- **Python 3.11+**（用于后端）
- **Node.js 22.x**（用于前端）
- **Git**

### 初始设置

1. **克隆仓库**：
   ```bash
   git clone https://github.com/banlanzs/openwebui-lite.git
   cd openwebui-lite
   ```

2. **安装后端依赖**：
   ```bash
   # 创建虚拟环境（推荐）
   python -m venv .venv

   # 激活虚拟环境
   # Windows:
   .\.venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate

   # 以开发模式安装 Open WebUI
   pip install -e .
   ```

3. **安装前端依赖**：
   ```bash
   npm install
   # 如果遇到兼容性问题，尝试：
   npm install --force
   ```

### 启动开发服务器

**后端（终端 1）**：
```bash
# 激活虚拟环境（如果尚未激活）
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# 设置可选的环境变量以禁用重型功能
set ENABLE_WEB_SEARCH=false
set BYPASS_EMBEDDING_AND_RETRIEVAL=true
set ENABLE_OLLAMA_API=false
set CORS_ALLOW_ORIGIN=http://localhost:5173

# 启动后端服务器
.\.venv\Scripts\open-webui serve --host 0.0.0.0 --port 8080
```

后端将在 [http://localhost:8080](http://localhost:8080) 访问
- 健康检查：[http://localhost:8080/health](http://localhost:8080/health)
- API 文档：[http://localhost:8080/docs](http://localhost:8080/docs)

**前端（终端 2）**：
```bash
npm run dev -- --host --port 5173
```

前端将在 [http://localhost:5173](http://localhost:5173) 访问

### Docker 开发（可选）

用于容器化开发的前后端分离：

```bash
# 构建并启动前端和后端
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 故障排查

- **CORS 错误**：确保 `CORS_ALLOW_ORIGIN` 包含 `http://localhost:5173`
- **端口冲突**：使用 `netstat -ano | findstr :8080`（Windows）或 `lsof -i :8080`（Linux/macOS）查找冲突的进程
- **前端无法连接**：验证后端正在运行并且可以在 `/health` 端点访问

详细的设置说明，请参阅 [lite-start.md](./lite-start.md) 或 [start.md](./start.md)。

---
