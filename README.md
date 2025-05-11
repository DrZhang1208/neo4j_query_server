# Neo4j HTTP Server

## 项目概述

Neo4j HTTP Server 是一个基于 FastAPI 开发的 HTTP 服务，用于查询 Neo4j 图数据库。该服务提供了一个简单的 API 接口，允许客户端通过 HTTP 请求查询图数据库中的实体关系数据，特别是术语及其同义词关系。

## 功能特点

- 基于 FastAPI 框架，提供高性能的 HTTP API
- 支持 Neo4j 图数据库查询
- 支持跨域资源共享 (CORS)
- 提供术语同义词查询功能
- 支持自定义查询深度和结果限制
- 错误日志记录

## 安装说明

### 前置条件

- Python 3.10 或更高版本
- Neo4j 数据库服务

### 安装步骤

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量

创建 `.env` 文件，并设置以下环境变量：

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
```

## 使用方法

### 启动服务

```bash
uvicorn neo4j_server:app --port 7575
```

或者使用提供的启动脚本：

```bash
./start.sh
```

服务默认在 `http://localhost:7575` 启动。

### API 文档

启动服务后，可以通过访问 `http://localhost:7575/docs` 查看自动生成的 API 文档。

## API 接口

### 查询图数据库

**端点**: `/query`

**方法**: POST

**请求体**:

```json
{
  "entity_name": "实体名称",
  "entity_type": "术语",
  "relation_type": "同义词",
  "limit": 10
}
```

**参数说明**:

- `entity_name`: 要查询的实体名称（必填）
- `entity_type`: 实体类型，默认为 "术语"
- `relation_type`: 关系类型，默认为 "同义词"
- `limit`: 返回结果数量限制，默认为 25

**响应示例**:

```json
[
  {
    "name": "相关术语1",
    "is_standard": true
  },
  {
    "name": "相关术语2",
    "is_standard": false
  }
]
```

## 错误处理

服务会将错误信息记录到 `neo4j_server.log` 文件中，并返回包含错误详情的 JSON 响应：

```json
{
  "error": "查询失败",
  "details": "错误详情"
}
```

## 开发说明

### 项目结构

- `neo4j_server.py`: 主服务文件，包含 FastAPI 应用和 Neo4j 查询逻辑
- `request.py`: 请求模型定义
- `main.py`: 入口文件
- `.env`: 环境变量配置文件
- `requirements.txt`: 项目依赖

### 扩展开发

如需添加新的查询功能，可以在 `neo4j_server.py` 中添加新的路由和查询逻辑。
