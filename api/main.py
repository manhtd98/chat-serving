

import os
import sys

sys.path.insert(0, os.path.realpath(os.path.pardir))
import logging
import logstash

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # noqa: E402
from routes import query_route,user_route
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/tasks/openapi.json", docs_url="/api/docs")
FastAPIInstrumentor.instrument_app(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

logging.basicConfig(
    format=f"\n\x00%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logstash.TCPLogstashHandler(
            os.getenv("FLUENT_HOST", "logstash.aicycle.ai"), 50000, version=1
        ),
        logging.StreamHandler(),
    ],
)

@app.on_event("startup")
async def startup_event():
    logging.info("SUCCESS INIT RESTFUL API")


@app.get("/heatbeat")
async def heatbeat():
    logging.info("GET HEATBEAT")
    return {"status": True}


app.include_router(user_route.router, prefix="/api/v1")
app.include_router(query_route.router, prefix="/api/v1")