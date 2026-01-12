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

## 如何安装 🚀

### 通过 Python pip 安装 🐍

Open WebUI 可以使用 pip（Python 包安装程序）安装。在继续之前，请确保您使用的是 **Python 3.11** 以避免兼容性问题。

1. **安装 Open WebUI**：
   打开终端并运行以下命令来安装 Open WebUI：

   ```bash
   pip install open-webui
   ```

2. **运行 Open WebUI**：
   安装完成后，您可以通过执行以下命令启动 Open WebUI：

   ```bash
   open-webui serve
   ```

这将启动 Open WebUI 服务器，您可以在 [http://localhost:8080](http://localhost:8080) 访问

### 使用 Docker 快速开始 🐳

> [!NOTE]
> 请注意，对于某些 Docker 环境，可能需要额外的配置。如果您遇到任何连接问题，我们的[Open WebUI 文档](https://docs.openwebui.com/)上的详细指南随时为您提供帮助。

> [!WARNING]
> 使用 Docker 安装 Open WebUI 时，请确保在 Docker 命令中包含 `-v open-webui:/app/backend/data`。这一步骤至关重要，因为它确保您的数据库已正确挂载并防止任何数据丢失。

> [!TIP]
> 如果您希望将 Open WebUI 与包含的 Ollama 或 CUDA 加速一起使用，我们建议使用标记为 `:cuda` 或 `:ollama` 的官方镜像。要启用 CUDA，您必须在 Linux/WSL 系统上安装 [Nvidia CUDA 容器工具包](https://docs.nvidia.com/dgx/nvidia-container-runtime-upgrade/)。

### 默认配置安装

- **如果 Ollama 在您的计算机上**，使用此命令：

  ```bash
  docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
  ```

- **如果 Ollama 在不同的服务器上**，使用此命令：


- **要使用 Nvidia GPU 支持运行 Open WebUI**，使用此命令：

  ```bash
  docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda
  ```

### 仅使用 OpenAI API 的安装

- **如果您只使用 OpenAI API**，使用此命令：

  ```bash
  docker run -d -p 3000:8080 -e OPENAI_API_KEY=your_secret_key -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
  ```


安装完成后，您可以在 [http://localhost:3000](http://localhost:3000) 访问 Open WebUI。享受吧！😄

### 其他安装方法

我们提供各种替代安装方法，包括非 Docker 本地安装方法、Docker Compose、Kustomize 和 Helm。访问我们的 [Open WebUI 文档](https://docs.openwebui.com/getting-started/)或加入我们的 [Discord 社区](https://discord.gg/5rJgQTnV4s)以获取全面指导。

查看[本地开发指南](https://docs.openwebui.com/getting-started/advanced-topics/development)以获取有关设置本地开发环境的说明。

### 故障排查

遇到连接问题？我们的 [Open WebUI 文档](https://docs.openwebui.com/troubleshooting/)随时为您提供帮助。如需进一步帮助并加入我们的充满活力的社区，请访问 [Open WebUI Discord](https://discord.gg/5rJgQTnV4s)。

#### Open WebUI：服务器连接错误

遇到连接问题？请访问文档进行故障排查。

### 保持 Docker 安装最新

如果您想将本地 Docker 安装更新到最新版本，您可以使用 [Watchtower](https://containrrr.dev/watchtower/)：

```bash
docker run --rm --volume /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --run-once open-webui
```

在命令的最后部分，如果容器名称不同，请将 `open-webui` 替换为您的容器名称。

查看我们的 [Open WebUI 文档](https://docs.openwebui.com/getting-started/updating)中提供的更新指南。

### 使用开发分支 🌙

> [!WARNING]
> `:dev` 分支包含最新的不稳定功能和更改。使用它需要您自担风险，因为它可能有错误或不完整的功能。

如果您想尝试最新的前沿功能并且可以接受偶尔的不稳定性，您可以像这样使用 `:dev` 标签：

```bash
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui --add-host=host.docker.internal:host-gateway --restart always ghcr.io/open-webui/open-webui:dev
```

### 离线模式

如果您在离线环境中运行 Open WebUI，您可以将 `HF_HUB_OFFLINE` 环境变量设置为 `1` 以防止尝试从互联网下载模型。

```bash
export HF_HUB_OFFLINE=1
```