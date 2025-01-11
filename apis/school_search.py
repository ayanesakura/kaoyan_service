from fastapi import FastAPI, HTTPException
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file_util import loads_json

app = FastAPI(title="学校搜索服务")

# 加载学校基础数据
SCHOOL_DATA_PATH = "/Users/ayane/WeChatProjects/kaoyan_service/resources/全部学校信息.json"
# 加载专业详细数据
MAJOR_DATA_PATH = "/Users/ayane/WeChatProjects/kaoyan_service/resources/all_major_detail.json"

schools = loads_json(SCHOOL_DATA_PATH)
schools = [school['学校名称'] for school in schools]

# 加载并预处理专业数据
major_data = loads_json(MAJOR_DATA_PATH)
school_structure = {}

# 构建学校-学院-专业的层级结构
for item in major_data:
    school = item['dwmc']
    college = item['yxsmc']
    major = item['zymc']
    
    if school not in school_structure:
        school_structure[school] = {}
    
    if college not in school_structure[school]:
        school_structure[school][college] = []
        
    if major not in school_structure[school][college]:
        school_structure[school][college].append(major)

@app.post("/search")
async def search_schools(request: dict) -> List[dict]:
    """
    搜索学校接口
    :param request: 请求体,包含query字段作为搜索关键词
    :return: 匹配的学校列表
    """
    query = request.get('query', '')
    if not query:
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
        
    # 简单的模糊匹配实现
    results = []
    for school in schools:
        if query.lower() in str(school).lower():
            results.append(school)
    results = [{'name': i} for i in results]
    return results

@app.get("/school_structure/{school_name}")
async def get_school_structure(school_name: str) -> Dict:
    """
    获取学校的学院和专业结构
    :param school_name: 学校名称
    :return: 包含学院和专业信息的字典
    """
    if not school_name:
        raise HTTPException(status_code=400, detail="学校名称不能为空")
        
    if school_name not in school_structure:
        raise HTTPException(status_code=404, detail="未找到该学校信息")
    
    return {
        "school": school_name,
        "colleges": [
            {
                "name": college,
                "majors": majors
            }
            for college, majors in school_structure[school_name].items()
        ]
    }

@app.get("/")
async def root():
    return {"message": "学校搜索服务"} 