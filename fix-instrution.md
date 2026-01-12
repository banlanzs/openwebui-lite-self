## 轻量化改造方案

要对Open WebUI进行轻量化改造，只保留核心API调用服务，可以按照以下步骤进行：

### 1. 保留的核心模块

**必需保留的文件和功能：**
- `backend/open_webui/main.py` - 主应用入口（需精简导入） [1](#1-0) 
- `backend/open_webui/routers/openai.py` - OpenAI API兼容接口
- `backend/open_webui/routers/chats.py` - 聊天功能
- `backend/open_webui/routers/models.py` - 模型管理
- `backend/open_webui/utils/models.py` - 模型工具函数 [2](#1-1) 
- `backend/open_webui/utils/chat.py` - 聊天处理逻辑
- `backend/open_webui/utils/middleware.py` - 中间件（保留工具调用部分） [3](#1-2) 

### 2. 可以删除的功能模块

**删除以下router和功能：**
- `routers/retrieval.py` - RAG检索功能
- `routers/pipelines.py` - 管道功能
- `routers/knowledge.py` - 知识库
- ~~`routers/files.py` - 文件管理~~
- `routers/functions.py` - 自定义函数
- ~~`routers/prompts.py` - 提示词管理~~
- `routers/evaluations.py` - 评估功能
- `routers/notes.py` - 笔记功能
- `routers/folders.py` - 文件夹功能
- `routers/groups.py` - 用户组
- ~~`routers/memories.py` - 记忆功能~~
- `routers/scim.py` - SCIM协议
- `routers/tasks.py` - 任务管理
- `routers/audio.py` - 音频功能（如果不需要语音）

### 3. 精简依赖项

**修改 `pyproject.toml`，删除不必要的依赖：** [4](#1-3) 

保留核心依赖：
```toml
dependencies = [
    "fastapi==0.123.0",
    "uvicorn[standard]==0.37.0", 
    "pydantic==2.12.5",
    "python-multipart==0.0.20",
    "requests==2.32.5",
    "aiohttp==3.12.15",
    "httpx[socks,http2,zstd,cli,brotli]==0.28.1",
    "sqlalchemy==2.0.38",
    "alembic==1.17.2",
    "python-jose==3.5.0",
    "cryptography",
    "bcrypt==5.0.0",
    "PyJWT[crypto]==2.10.1",
]
```

删除以下依赖：
- `chromadb` - 向量数据库
- `langchain` - LangChain框架
- ~~`opensearch-py` - 搜索引擎~~
- `pycrdt` - 协作编辑
- ~~`redis` - 缓存（如果不需要分布式）~~
- `APScheduler` - 任务调度
- ~~`RestrictedPython` - 代码执行~~
- 所有AI模型特定依赖（anthropic, google-genai等）

### 4. 简化main.py

**精简主应用文件，只保留必要路由：**

```python
from open_webui.routers import (
    openai,  # 核心API
    chats,   # 聊天功能
    models,  # 模型管理
    auths,   # 认证
    users,   # 用户管理
    configs, # 配置
    tools,   # 工具调用
    images,  # 画图功能
)

# 删除其他不需要的router导入
```

### 5. 环境变量配置

**设置环境变量禁用不需要的功能：**
```bash
# 禁用Ollama
ENABLE_OLLAMA_API=false

# 禁用RAG功能
ENABLE_RAG=false

# 禁用Web搜索
ENABLE_WEB_SEARCH=false

# 禁用文件上传
ENABLE_FILE_UPLOAD=false

# 禁用音频功能
ENABLE_AUDIO=false

# 禁用代码执行
ENABLE_CODE_EXECUTION=false
```

### 6. 前端精简

**删除或注释前端不需要的页面和组件：**
- 删除知识库相关页面
- 删除文档管理界面
- 删除管道配置界面
- 删除评估和统计页面
- 简化侧边栏，只保留模型、聊天、设置等核心功能

### 7. 数据库精简

**只保留必要的表结构：**
- `users` - 用户表
- `chats` - 聊天记录表
- `models` - 模型配置表
- `configs` - 配置表

删除以下表：
- `files` - 文件表
- `knowledge` - 知识库表
- `functions` - 函数表
- `prompts` - 提示词表
- `memories` - 记忆表

## 实施步骤
2. **逐步删除不需要的router文件**
3. **精简main.py导入**
4. **修改pyproject.toml依赖**
5. **删除数据库模型文件**
6. **运行数据库迁移**
7. **测试核心功能**

这样改造后，项目将只保留核心的API调用、模型管理和聊天功能，大幅减少资源占用和复杂度。

## Notes

- 轻量化后的项目将失去RAG、知识库、文档处理等高级功能
- 建议在分支中进行改造，保留原始代码以便需要时恢复
- 删除功能时要确保没有循环依赖
- 工具调用功能保留，因为这是日常对话的重要功能

Wiki pages you might want to explore:
- [Data and Storage Layer (open-webui/open-webui)](/wiki/open-webui/open-webui#2.3)

### Citations

**File:** backend/open_webui/main.py (L70-96)
```python
from open_webui.routers import (
    audio,
    images,
    ollama,
    openai,
    retrieval,
    pipelines,
    tasks,
    auths,
    channels,
    chats,
    notes,
    folders,
    configs,
    groups,
    files,
    functions,
    memories,
    models,
    knowledge,
    prompts,
    evaluations,
    tools,
    users,
    utils,
    scim,
)
```

**File:** backend/open_webui/utils/models.py (L1-33)
```python
import time
import logging
import asyncio
import sys

from aiocache import cached
from fastapi import Request

from open_webui.socket.utils import RedisDict
from open_webui.routers import openai, ollama
from open_webui.functions import get_function_models


from open_webui.models.functions import Functions
from open_webui.models.models import Models
from open_webui.models.groups import Groups


from open_webui.utils.plugin import (
    load_function_module_by_id,
    get_function_module_from_cache,
)
from open_webui.utils.access_control import has_access


from open_webui.config import (
    BYPASS_ADMIN_ACCESS_CONTROL,
    DEFAULT_ARENA_MODEL,
)

from open_webui.env import BYPASS_MODEL_ACCESS_CONTROL, SRC_LOG_LEVELS, GLOBAL_LOG_LEVEL
from open_webui.models.users import UserModel

```

**File:** backend/open_webui/utils/middleware.py (L31-90)
```python
from open_webui.models.users import Users
from open_webui.socket.main import (
    get_event_call,
    get_event_emitter,
)
from open_webui.routers.tasks import (
    generate_queries,
    generate_title,
    generate_follow_ups,
    generate_image_prompt,
    generate_chat_tags,
)
from open_webui.routers.retrieval import (
    process_web_search,
    SearchForm,
)
from open_webui.routers.images import (
    image_generations,
    CreateImageForm,
    image_edits,
    EditImageForm,
)
from open_webui.routers.pipelines import (
    process_pipeline_inlet_filter,
    process_pipeline_outlet_filter,
)
from open_webui.routers.memories import query_memory, QueryMemoryForm

from open_webui.utils.webhook import post_webhook
from open_webui.utils.files import (
    convert_markdown_base64_images,
    get_file_url_from_base64,
    get_image_url_from_base64,
)


from open_webui.models.users import UserModel
from open_webui.models.functions import Functions
from open_webui.models.models import Models

from open_webui.retrieval.utils import get_sources_from_items


from open_webui.utils.chat import generate_chat_completion
from open_webui.utils.task import (
    get_task_model_id,
    rag_template,
    tools_function_calling_generation_template,
)
from open_webui.utils.misc import (
    deep_update,
    extract_urls,
    get_message_list,
    add_or_update_system_message,
    add_or_update_user_message,
    get_last_user_message,
    get_last_user_message_item,
    get_last_assistant_message,
    get_system_message,
    prepend_to_first_user_message_content,
```

**File:** pyproject.toml (L1-60)
```text
[project]
name = "open-webui"
description = "Open WebUI"
authors = [
    { name = "Timothy Jaeryang Baek", email = "tim@openwebui.com" }
]
license = { file = "LICENSE" }
dependencies = [
    "fastapi==0.123.0",
    "uvicorn[standard]==0.37.0",
    "pydantic==2.12.5",
    "python-multipart==0.0.20",
    "itsdangerous==2.2.0",

    "python-socketio==5.15.0",
    "python-jose==3.5.0",
    "cryptography",
    "bcrypt==5.0.0",
    "argon2-cffi==25.1.0",
    "PyJWT[crypto]==2.10.1",
    "authlib==1.6.5",

    "requests==2.32.5",
    "aiohttp==3.12.15",
    "async-timeout",
    "aiocache",
    "aiofiles",
    "starlette-compress==1.6.1",
    "httpx[socks,http2,zstd,cli,brotli]==0.28.1",
    "starsessions[redis]==2.2.1",

    "sqlalchemy==2.0.38",
    "alembic==1.17.2",
    "peewee==3.18.3",
    "peewee-migrate==1.14.3",

    "pycrdt==0.12.25",
    "redis",

    "APScheduler==3.10.4",
    "RestrictedPython==8.0",

    "loguru==0.7.3",
    "asgiref==3.11.0",

    "tiktoken",
    "mcp==1.22.0",

    "openai",
    "anthropic",
    "google-genai==1.52.0",
    "google-generativeai==0.8.5",

    "langchain==0.3.27",
    "langchain-community==0.3.29",

    "fake-useragent==2.2.0",
    "chromadb==1.0.20",
    "opensearch-py==2.8.0",
    "PyMySQL==1.1.1",
```
