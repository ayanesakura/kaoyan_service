from fastapi import FastAPI
import uvicorn
from school_search import app as school_app
from utils.file_util import get_host_ip

# 创建主应用
app = FastAPI(title="考研服务API")

# 挂载子应用
app.mount("/school", school_app)

@app.get("/")
async def root():
    return {"message": "考研服务API已启动"}

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    ip = get_host_ip()
    
    print(f"服务已启动,可通过以下地址访问:")
    print(f"本地访问: http://localhost:{port}")
    print(f"局域网访问: http://{ip}:{port}")
    print(f"API文档: http://{ip}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
