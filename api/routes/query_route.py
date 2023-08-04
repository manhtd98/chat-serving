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
from schemas import QueryRequest, TaskResult
from crud import get_user_chat_history
from tasks import task_query_workflow

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# create a ZipkinExporter
zipkin_exporter = ZipkinExporter(
    endpoint=os.getenv("ZIPKIN_ENDPOINT", "http://172.17.0.1:9411/api/v2/spans"),
)
span_processor = BatchSpanProcessor(zipkin_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)
prop = TraceContextTextMapPropagator()

router = APIRouter(prefix="/chat", tags=["chat api"])


@router.post(
    "/query",
    response_model=TaskResult,
    status_code=202,
    responses={202: {"model": TaskResult, "description": "Accepted: Not Ready"}},
)
async def process(
    query: QueryRequest
):
    chat_session = get_user_chat_history(query.token, query.bucket)
    result = {}
    start_time = time.perf_counter()
    with tracer.start_as_current_span("RESTFUL API SEGMENTATION"):
        try:
            logging.info("START REQUEST SEGMENTATION")
            task_id = task_query_workflow.delay(query.query, chat_session)
            result["task_id"] = str(task_id)
            result["status"] = "PROCESSING"
            task = AsyncResult(str(task_id))
            # Task Not Ready
            while not task.ready():
                await asyncio.sleep(0.05)
            # Task done: return the value
            task_result = task.get()
            result = task_result.get("result")
            logging.info(f"END REQUEST SEGMENTATION: {time.perf_counter()- start_time}")
            return JSONResponse(
                status_code=200,
                content={
                    "task_id": str(task_id),
                    "status": "SUCCESS",
                    "result": result,
                },
            )
        except Exception as ex:
            logging.error(str(ex))
            result["task_id"] = "-"
            result["status"] = "ERROR"
        return JSONResponse(status_code=202, content=result)
