from pydantic import BaseModel
from typing import Optional


class GraphQueryRequest(BaseModel):
    """
    图数据库查询请求模型
    
    用于定义Neo4j图数据库查询的参数结构，包括实体名称、类型、关系类型等
    所有可选参数都提供了默认值
    """
    entity_name: str         # 实体名，例如疾病名称
    entity_type: Optional[str] = '术语'        # 实体类型，如 Disease、Symptom、Drug 等
    relation_type: Optional[str] = '同义词'  # 关系类型，默认为"同义词"
    limit: Optional[int] = 10            # 返回结果数量限制，默认为10条