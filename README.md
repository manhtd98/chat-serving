# CHAT SERVING ENGINE FOR TRITON LLMA
## Start the system
Start triton serving
```
sudo docker run -it --rm --gpus all -d --shm-size=4g --ulimit memlock=-1 --network="host" --ulimit stack=67108864 -p8000:8000 -p8001:8001 -p8002:8002 -v $(pwd)/serving:/opt/ml/model segmentation:latest tritonserver --model-store=/opt/ml/model --strict-model-config=false --allow-grpc=true --allow-http=true --allow-metrics=true --grpc-infer-allocation-pool-size=16
```
Start backend api
```
docker-compose up -d
```


```
CELERY_BROKER_URL=redis://localhost:6379/0 CELERY_RESULT_BACKEND=db+postgresql://user:password@localhost:5432/alpha celery -A main worker --concurrency 1 -P solo -Q task_query_workflow -E --loglevel=info --logfile=logs/celery.log
```


```
sudo COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up -d --build
```