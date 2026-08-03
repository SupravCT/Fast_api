from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import time
from fastapi.middleware.cors import CORSMiddleware
import logging

uvicorn_logger=logging.getLogger("uvicorn.access")
uvicorn_logger.disabled=True

logger = logging.getLogger("custom_middleware")
logging.basicConfig(level=logging.INFO)

def register_middleware(app:FastAPI):
    
    @app.middleware("http")
    async def custom_logging(request:Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Process Time: {process_time}")
        return response


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"])