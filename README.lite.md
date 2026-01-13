# Open WebUI Lite - Docker 精简版部署 🚀

## 镜像大小对比

| 版本 | Backend | Frontend | 总计 | 减少 |
|------|---------|----------|------|------|
| **完整版** | 14.51 GB | 6.69 GB | **21.20 GB** | - |
| **精简版** | ~1-2 GB | ~500 MB | **~2 GB** | **90%** |

## 精简说明

### 移除的重量级功能
- ❌ 本地向量数据库（ChromaDB、Weaviate、Milvus、Qdrant）
- ❌ 本地嵌入模型（transformers、sentence-transformers）
- ❌ 文档 OCR 识别（opencv、rapidocr）
- ❌ 语音转文字（faster-whisper、onnxruntime）
- ❌ 网页爬虫（playwright、firecrawl）
- ❌ 复杂文档解析（unstructured、pandoc）
- ❌ 数据分析库（pandas、openpyxl）
- ❌ LangChain 社区扩展

### 保留的核心功能
- ✅ FastAPI Web 框架
- ✅ 用户认证和授权
- ✅ 数据库支持（SQLite/PostgreSQL/MySQL）
- ✅ OpenAI/Anthropic/Google AI API 调用
- ✅ WebSocket 实时通信
- ✅ Redis 缓存
- ✅ 基础文件上传

## 快速开始

### 1. 构建并启动服务

```bash
# 使用精简版配置启动
docker-compose -f docker-compose.lite.yml up --build -d
```

### 2. 查看日志

```bash
docker-compose -f docker-compose.lite.yml logs -f
```

### 3. 访问服务

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **API 文档**: http://localhost:8080/docs

### 4. 停止服务

```bash
docker-compose -f docker-compose.lite.yml down
```

## 验证镜像大小

```bash
# 查看镜像大小
docker images | grep open-webui

# 预期输出类似：
# open-webui-backend    latest    1.5GB
# open-webui-frontend   latest    600MB
```

## 环境变量配置

精简版默认配置（在 `docker-compose.lite.yml` 中）：

```yaml
CORS_ALLOW_ORIGIN: "http://localhost:5173"
ENABLE_WEB_SEARCH: "false"              # 关闭网页搜索
BYPASS_EMBEDDING_AND_RETRIEVAL: "true"  # 跳过向量检索
ENABLE_OLLAMA_API: "false"              # 关闭 Ollama 本地模型
```

## 自定义依赖

如果需要某些被移除的功能，可以编辑 `backend/requirements.lite.txt` 添加依赖：

```bash
# 例如：添加文档解析支持
echo "pypdf==6.4.0" >> backend/requirements.lite.txt
echo "docx2txt==0.8" >> backend/requirements.lite.txt

# 重新构建
docker-compose -f docker-compose.lite.yml up --build -d
```

## 常见问题

### Q: 精简版缺少哪些功能？
A: 主要是本地 AI 模型、向量搜索、OCR、语音识别等重量级功能。如果只使用云端 API（OpenAI/Claude/Gemini），精简版完全够用。

### Q: 如何切换回完整版？
A: 使用原始配置文件启动：
```bash
docker-compose down
docker-compose up --build -d
```

### Q: 精简版性能如何？
A: 启动更快，内存占用更少，适合个人使用或小团队部署。

## 技术细节

### Backend 优化
- 使用 `requirements.lite.txt` 替代完整依赖
- 移除深度学习框架和大型库
- 清理 pip 缓存

### Frontend 优化
- 多阶段构建，分离构建和运行环境
- 生产构建替代开发模式
- 仅安装生产依赖
- 清理 npm 缓存

## 相关文件

- `Dockerfile.backend.lite` - 精简版后端 Dockerfile
- `Dockerfile.frontend.lite` - 精简版前端 Dockerfile
- `docker-compose.lite.yml` - 精简版编排配置
- `backend/requirements.lite.txt` - 精简版 Python 依赖

## 完整版部署

如需完整功能，请参考 [README.md](./README.md) 使用标准部署方式。
