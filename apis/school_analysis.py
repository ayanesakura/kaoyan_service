from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
import sys
import os
import logging
import json
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file_util import loads_json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="志愿分析服务")

class AnalysisRequest(BaseModel):
    """分析请求的数据模型"""
    current_school: str
    current_major: str
    grade: str  # 年级
    rank: str  # 成绩排名
    good_major: str = '英语' # 擅长专业
    if_first: bool = True # 是否一战
    target_school: str
    target_major: str 
    target_city: str
    target_level: str # 期望学校层次

class AnalysisResponse(BaseModel):
    """分析响应的数据模型"""
    success: bool
    message: str
    analysis: Optional[str] = None
    recommendations: Optional[List[Dict]] = None

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_application(request: AnalysisRequest) -> Dict:
    """
    分析考研申请的可能性
    
    Args:
        request: 包含申请信息的请求对象
        
    Returns:
        包含分析结果的响应对象
    """
    # 记录请求信息
    logger.info(f"收到分析请求: {json.dumps(request.dict(), ensure_ascii=False, indent=2)}")
    
    try:
        # 验证输入参数
        # if request.rank <= 0:
        #     error_msg = "排名必须为正数"
        #     logger.error(f"参数验证失败: {error_msg}")
        #     raise HTTPException(status_code=400, detail=error_msg)
            
        # TODO: 这里将来添加实际的分析逻辑
        # 目前返回空分析结果
        response = {
            "success": True,
            "message": "分析完成",
            "analysis": None,  # 暂时返回null
            "recommendations": [
                {
                    "aspect": "申请可能性",
                    "content": "暂无分析"
                },
                {
                    "aspect": "建议",
                    "content": "暂无建议"
                }
            ]
        }
        
        # 记录响应信息
        logger.info(f"返回分析结果: {json.dumps(response, ensure_ascii=False, indent=2)}")
        time.sleep(1)
        return response
        
    except Exception as e:
        error_response = {
            "success": False,
            "message": f"分析过程出现错误: {str(e)}",
            "analysis": None,
            "recommendations": None
        }
        # 记录错误信息
        logger.error(f"处理请求时发生错误: {str(e)}")
        logger.error(f"错误响应: {json.dumps(error_response, ensure_ascii=False, indent=2)}")
        return error_response

@app.get("/")
async def root():
    return {"message": "志愿分析服务"}

