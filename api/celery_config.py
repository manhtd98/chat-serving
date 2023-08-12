from celery import Task
import celery

class ChatQueryTask(Task):
    name = "task_query_workflow"

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def run(self, payload):
        """
        place holder method
        """
        pass

def create_worker_from(WorkerClass):
    """
    Create worker instance given WorkerClass
    :param WorkerClass: WorkerClass to perform task
    :type WorkerClass: subclass of celery.Task
    :param celery_config: celery config module, default 'celery_tasks.celery_config'. This depends on
                            project path
    :type celery_config: str
    :return: celery app instance and worker task instance
    :rtype: tuple of (app, worker_task)
    """
    assert issubclass(WorkerClass, celery.Task)
    app = celery.Celery()
    # app.config_from_object(celery_config)
    app.conf.update(task_default_queue=WorkerClass.name)  # update worker queue
    worker_task = app.register_task(WorkerClass())
    return app, worker_task

