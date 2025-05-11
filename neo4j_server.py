import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase
from typing import Any
from request import GraphQueryRequest
from dotenv import load_dotenv

# 创建FastAPI应用实例
app = FastAPI(title="Neo4j HTTP Server", 
              description="Neo4j HTTP 查询服务")

# 配置CORS中间件，允许跨域资源共享
# 这对于前端应用从不同域访问API非常重要
app.add_middleware(
    CORSMiddleware,           # 使用CORS中间件
    allow_origins=["*"],      # 允许所有来源的请求，生产环境中应该限制为特定域名
    allow_credentials=True,   # 允许发送凭证（如cookies）
    allow_methods=["POST"],   # 允许POST请求，其他请求方法需要单独配置
    allow_headers=["*"],      # 允许所有HTTP头部
)

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取Neo4j数据库连接信息
uri = os.getenv("NEO4J_URI")                    # Neo4j数据库URI
username = os.getenv("NEO4J_USER")              # 用户名
password = os.getenv("NEO4J_PASSWORD")          # 密码
database = os.getenv("NEO4J_DATABASE", "neo4j") # 数据库名称，默认为neo4j

def get_db():
    """
    获取Neo4j数据库连接
    Returns:
        GraphDatabase.driver: Neo4j驱动实例
    """
    return GraphDatabase.driver(uri, auth=(username, password), database=database)

@app.post("/query")
async def query_graph(query: GraphQueryRequest, db: Any = Depends(get_db)):
    """
    处理图数据库查询请求
    Args:
        query (GraphQueryRequest): 查询请求参数
        db: Neo4j数据库连接
    Returns:
        dict: 查询结果
    """
    try:
        with db.session(database=database) as session:
            # 打印查询参数，用于调试
            # print(query.entity_name)
            # print(query.entity_type)
            # print(query.relation_type)
            
            # 执行Cypher查询
            # 查询说明：
            # 1. 首先匹配指定类型和名称的节点n
            # 2. 然后查找与n有指定关系类型连接的术语节点m
            # 3. 收集关系路径信息
            # 4. 过滤掉空节点
            # 5. 返回唯一的术语名称和是否为标准术语的标志
            result = session.run(
                """
                MATCH (n:$($entity_type) {name: $entity_name})
                OPTIONAL MATCH path=(n)-[r:$($relation_type)]-(m:`术语`)
                WITH m, relationships(path) AS rels
                WHERE m IS NOT NULL
                RETURN DISTINCT m.name AS name, m.标准术语 AS is_standard
                LIMIT $limit
                """,
                entity_name=query.entity_name,
                entity_type=query.entity_type,
                relation_type=query.relation_type,
                limit=query.limit
            )
            # 处理查询结果，将Neo4j记录转换为JSON格式
            # 提取每条记录中的name和is_standard字段，并重命名is_standard为standard_term
            return [{"name": record["name"], "standard_term": record["is_standard"]} for record in result]
    except Exception as e:
        # 导入日志模块并配置
        import logging
        # 设置日志记录到文件，级别为ERROR
        logging.basicConfig(filename='neo4j_server.log', level=logging.ERROR)
        # 记录查询失败的详细错误信息
        logging.error(f"Query failed: {str(e)}")
        # 返回用户友好的错误信息，同时包含详细错误信息供调试
        return {"error": "查询失败", "details": str(e)}


