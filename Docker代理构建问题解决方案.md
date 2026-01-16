# Docker 代理构建问题解决方案

## 概述

本文档记录了在 Windows 环境下使用 Proxifier + Clash 代理构建 Docker 镜像时遇到的问题及完整解决方案。

**环境信息：**
- 操作系统：Windows
- 代理工具：Proxifier + Clash（系统代理模式）
- Docker：Docker Desktop
- 项目：open-webui-lite
- Clash HTTP 代理端口：7890（默认）

**构建目标：**
- Backend：Python 3.12 + FastAPI 0.123.0
- Frontend：Node.js 22 + npm

**核心问题：**
Docker 容器网络与宿主机隔离，无法自动使用 Proxifier + Clash 的系统代理，需要显式配置。

---

## 遇到的问题

### 1. FastAPI 版本找不到（阿里云镜像源未同步）

**错误信息：**
```
ERROR: Could not find a version that satisfies the requirement fastapi==0.123.0
ERROR: No matching distribution found for fastapi==0.123.0
```

**原因：**
- 使用了阿里云镜像源（mirrors.aliyun.com）
- fastapi 0.123.0 是最新版本（2025-11-30 发布），镜像源未同步

**解决方案：**
改用官方 PyPI 源（pypi.org）+ Clash 代理访问

---

### 2. Docker 容器无法使用宿主机代理

**错误信息：**
```
npm error network request failed
pip error connection timeout
```

**原因：**
- Proxifier + Clash 的系统代理只对宿主机进程生效
- Docker 容器有独立的网络栈，无法自动继承系统代理
- 需要通过 `host.docker.internal` 访问宿主机代理

**解决方案：**
1. 确保 Clash 开启 "Allow LAN" 选项
2. 在 docker-compose.yml 中配置 build.args 传递代理参数
3. 使用 `host.docker.internal:7890` 访问宿主机代理

---

### 3. Docker ARG 作用域问题

**错误信息：**
```bash
RUN if [ -n "" ]; then  # HTTP_PROXY 为空
```

**原因：**
- ARG 在 FROM 之前声明，但在 FROM 之后就失效了
- ENV 中使用 `${HTTP_PROXY}` 时，ARG 已超出作用域

**解决方案：**
在 FROM 之后重新声明 ARG：
```dockerfile
ARG HTTP_PROXY
ARG HTTPS_PROXY

FROM node:22-slim AS frontend

# 重新声明 ARG（FROM 之后需要重新声明）
ARG HTTP_PROXY
ARG HTTPS_PROXY

ENV HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY}
```

---

### 4. apt-get 通过代理出现 502 错误

**错误信息：**
```
E: Failed to fetch http://deb.debian.org/debian/pool/...  502  Bad Gateway [IP: 192.168.65.254 7890]
```

**原因：**
- Clash 代理对 apt-get 的某些请求返回 502 错误
- apt-get 不需要代理（Debian 仓库可以直接访问）

**解决方案：**
移除代理测试步骤，避免 apt-get 使用代理

---

### 5. npm 依赖冲突

**错误信息：**
```
npm error ERESOLVE could not resolve
npm error While resolving: @tiptap/extension-bubble-menu@2.26.1
npm error Found: @tiptap/core@3.0.7
```

**原因：**
@tiptap/core 版本冲突（v3.0.7 vs v2.7.0）

**解决方案：**
使用 `--legacy-peer-deps` 参数忽略依赖冲突

---

### 6. onnxruntime-node 下载失败

**错误信息：**
```
npm error Downloading "https://github.com/microsoft/onnxruntime/releases/download/..."
npm error TypeError: fetch failed
npm error connect ECONNREFUSED 127.215.0.83:443
```

**原因：**
- onnxruntime-node 的 postinstall 脚本需要从 GitHub 下载二进制文件
- 该脚本使用 Node.js fetch API，不使用 npm 代理配置
- 即使设置了环境变量，连接仍然失败

**解决方案：**
使用 `--ignore-scripts` 参数跳过所有 postinstall 脚本

---

## 完整解决方案

### 1. 配置 Clash 代理

**步骤 1：确认 Clash HTTP 代理端口**
- 打开 Clash，查看 HTTP 代理端口（通常是 7890）
- 记录端口号，后续配置需要使用

**步骤 2：开启 Allow LAN**
- 在 Clash 设置中，开启 **"Allow LAN"** 或 **"允许局域网连接"**
- 这是关键步骤，否则 Docker 容器无法访问代理

---

### 2. 修改 Dockerfile.backend.lite

```dockerfile
# syntax=docker/dockerfile:1
ARG HTTP_PROXY
ARG HTTPS_PROXY

FROM python:3.12-slim AS backend

# 重新声明 ARG（FROM 之后需要重新声明）
ARG HTTP_PROXY
ARG HTTPS_PROXY

# 环境变量设置（代理优先）
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/backend \
    HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY} \
    NO_PROXY="localhost,127.0.0.1,.docker.internal"

WORKDIR /app

# 使用官方 PyPI 源（通过代理访问）
RUN if [ -n "${HTTP_PROXY}" ]; then \
        printf "[global]\nproxy = ${HTTP_PROXY}\n" > /etc/pip.conf; \
    fi

COPY backend/requirements.lite.txt ./backend/requirements.lite.txt

# 安装依赖（通过代理使用官方 PyPI 源）
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r backend/requirements.lite.txt

COPY backend ./backend

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "open_webui.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**关键点：**
1. 在 FROM 之后重新声明 ARG
2. 使用官方 PyPI 源（不使用国内镜像）
3. 通过代理访问官方源

---

### 3. 修改 Dockerfile.frontend.lite

```dockerfile
# syntax=docker/dockerfile:1
ARG HTTP_PROXY
ARG HTTPS_PROXY

FROM node:22-slim AS frontend

# 重新声明 ARG（FROM 之后需要重新声明）
ARG HTTP_PROXY
ARG HTTPS_PROXY

WORKDIR /app

# 转为环境变量（构建和运行时均生效）
ENV HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY} \
    NO_PROXY="localhost,127.0.0.1,.docker.internal"

COPY package*.json ./

# 配置 npm 使用代理并安装依赖
RUN if [ -n "${HTTP_PROXY}" ]; then \
        npm config set proxy ${HTTP_PROXY} && \
        npm config set https-proxy ${HTTPS_PROXY}; \
    fi \
 && npm install --legacy-peer-deps --ignore-scripts

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "--port", "5173"]
```

**关键点：**
1. 在 FROM 之后重新声明 ARG
2. 配置 npm 使用代理
3. 使用 `--legacy-peer-deps` 解决依赖冲突
4. 使用 `--ignore-scripts` 跳过 onnxruntime-node 下载

---

### 4. 修改 docker-compose.lite.yml

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend.lite
      args:
        HTTP_PROXY: "http://host.docker.internal:7890"
        HTTPS_PROXY: "http://host.docker.internal:7890"
    environment:
      CORS_ALLOW_ORIGIN: "http://localhost:5173"
      ENABLE_WEB_SEARCH: "false"
      BYPASS_EMBEDDING_AND_RETRIEVAL: "true"
      ENABLE_OLLAMA_API: "false"
      HTTP_PROXY: "http://host.docker.internal:7890"
      HTTPS_PROXY: "http://host.docker.internal:7890"
      NO_PROXY: "localhost,127.0.0.1,172.0.0.0/8,.docker.internal"
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/backend/data

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend.lite
      args:
        HTTP_PROXY: "http://host.docker.internal:7890"
        HTTPS_PROXY: "http://host.docker.internal:7890"
    depends_on:
      - backend
    environment:
      APP_BUILD_HASH: "docker-lite"
      HTTP_PROXY: "http://host.docker.internal:7890"
      HTTPS_PROXY: "http://host.docker.internal:7890"
      NO_PROXY: "localhost,127.0.0.1,172.0.0.0/8,.docker.internal"
    ports:
      - "5173:5173"
```

**关键点：**
1. 在 `build.args` 中传递代理参数
2. 使用 `host.docker.internal:7890` 访问宿主机代理
3. 如果端口不是 7890，需要修改为实际端口

---

## 构建和运行

### 构建镜像

```bash
# 构建所有服务
docker-compose -f docker-compose.lite.yml build --no-cache

# 只构建前端
docker-compose -f docker-compose.lite.yml build --no-cache frontend

# 只构建后端
docker-compose -f docker-compose.lite.yml build --no-cache backend
```

### 启动服务

```bash
docker-compose -f docker-compose.lite.yml up -d
```

### 查看日志

```bash
# 查看所有日志
docker-compose -f docker-compose.lite.yml logs -f

# 查看前端日志
docker-compose -f docker-compose.lite.yml logs -f frontend

# 查看后端日志
docker-compose -f docker-compose.lite.yml logs -f backend
```

---

## 常见问题

### Q1: 如何确认 Clash 代理端口？

A: 打开 Clash，在主界面或设置中查看 HTTP 代理端口。常见端口：
- 7890（默认）
- 7891
- 其他自定义端口

### Q2: 如何确认 Allow LAN 已开启？

A: 在 Clash 设置中查找 "Allow LAN" 或 "允许局域网连接" 选项，确保已勾选。

### Q3: 如果代理端口不是 7890 怎么办？

A: 修改 docker-compose.lite.yml 中所有的 `7890` 为你的实际端口号。

### Q4: 为什么使用 --ignore-scripts？

A: onnxruntime-node 的 postinstall 脚本需要从 GitHub 下载二进制文件，即使配置了代理也可能失败。使用 `--ignore-scripts` 可以跳过这个步骤，避免构建失败。如果应用不需要 onnxruntime 功能，不会有影响。

### Q5: 为什么不使用国内镜像源？

A: 国内镜像源（如阿里云）可能没有同步最新版本的包（如 fastapi 0.123.0）。使用官方源 + 代理可以确保获取最新版本。

---

## 总结

通过以下步骤成功解决了使用 Proxifier + Clash 代理构建 Docker 镜像的问题：

1. **配置 Clash**：开启 Allow LAN，确认代理端口
2. **修复 ARG 作用域**：在 FROM 之后重新声明 ARG
3. **配置代理传递**：通过 docker-compose.yml 的 build.args 传递代理参数
4. **使用官方源**：pip 和 npm 都使用官方源 + 代理
5. **解决依赖冲突**：npm 使用 --legacy-peer-deps
6. **跳过安装脚本**：npm 使用 --ignore-scripts 避免 onnxruntime-node 下载失败

**关键要点：**
- Docker 容器网络隔离，必须显式配置代理
- 使用 `host.docker.internal` 访问宿主机代理
- ARG 在 FROM 之后需要重新声明
- Clash 必须开启 Allow LAN 选项

**适用场景：**
- Windows + Docker Desktop + Proxifier + Clash
- 需要通过代理访问国外资源（PyPI、npm、GitHub）
- 国内镜像源未同步最新版本的包
