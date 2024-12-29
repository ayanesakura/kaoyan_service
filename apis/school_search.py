from fastapi import FastAPI, HTTPException
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file_util import loads_json

app = FastAPI(title="学校搜索服务")

# 加载学校数据
SCHOOL_DATA_PATH = "/Users/ayane/WeChatProjects/kaoyan_service/resources/全部学校信息.json"

schools = loads_json(SCHOOL_DATA_PATH)
schools = [school['学校名称'] for school in schools]

@app.get("/search")
async def search_schools(query: str) -> List[dict]:
    """
    搜索学校接口
    :param query: 搜索关键词
    :return: 匹配的学校列表
    """
    if not query:
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
        
    # 简单的模糊匹配实现
    results = []
    for school in schools:
        if query.lower() in str(school).lower():
            results.append(school)
    results = [{'name': i} for i in results]
    return results

@app.get("/")
async def root():
    return {"message": "学校搜索服务"} 