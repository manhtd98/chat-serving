import os
import sys

sys.path.insert(0, os.path.realpath(os.path.pardir))
import logging
import logstash
from importlib import metadata
from fastapi.responses import UJSONResponse
from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # noqa: E402
from routes import query_route, user_route
from database import engine
from models import Base
from logging_helper import configure_logging

# Base.metadata.create_all(bind=engine)
configure_logging()
app = FastAPI(
    openapi_url="/api/v1/tasks/openapi.json",
    title="fastlogging",
    redoc_url="/api/redoc",
    default_response_class=UJSONResponse,
    docs_url="/api/doc",
)
FastAPIInstrumentor.instrument_app(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
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
