import os
import time
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import logging
import asyncio
from schemas import UserIn, UserOut
from crud import crud_add_user, crud_get_user_info

# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)

# # create a ZipkinExporter
# zipkin_exporter = ZipkinExporter(
#     endpoint=os.getenv("ZIPKIN_ENDPOINT", "http://172.17.0.1:9411/api/v2/spans"),
# )
# span_processor = BatchSpanProcessor(zipkin_exporter)

# # add to the tracer
# trace.get_tracer_provider().add_span_processor(span_processor)
# prop = TraceContextTextMapPropagator()

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", status_code=201)
async def process(user: UserIn):
    user = crud_add_user(user)
    return {"user_id": user.id}


@router.get("/user/{user_id}", status_code=201)
def get_user_info(user_id: int):
    return crud_get_user_info(user_id)
