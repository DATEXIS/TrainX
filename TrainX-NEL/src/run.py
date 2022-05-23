import logging
import os
from typing import Dict, Union

import ray
from flask import Flask, request, json, Response
from ray.exceptions import RayActorError
from waitress import serve
from werkzeug.exceptions import BadRequest

from biencodernel.datasets import KBDataset
from biencodernel.utils import get_config_from_env, get_gpu_ids
from jobs import TrainJob, PredictJob
from model import JobContainer, JobType, Job, JobStatus

app = Flask(__name__)

logger = logging.getLogger(__name__)

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())

config = get_config_from_env()

logger.info("Parsing knowledge base dataset {}".format(config['paths']['kb']))
kb_dataset = KBDataset(path_to_json=config['paths']['kb'], max_length=config['input_length'], bert_model=config['bert_model'])

gpu_ids = get_gpu_ids()

jobs: Dict[str, Union[TrainJob, PredictJob]] = dict()

@app.errorhandler(BadRequest)
def handle_invalid_usage(error):
    return error.description, error.code


@app.route('/jobstatus/<job_id>', methods=['GET'])
def get_job_status(job_id: str):
    try:
        state: JobStatus = ray.get(jobs[job_id].get_status.remote())
        return Response(json.dumps(state.to_texoo_dict()), status=200, mimetype='application/json')
    except KeyError:
        return Response('no job with id {}'.format(job_id), status=404, mimetype='application/json')
    except RayActorError:
        # since there was an actor and we do not have a FAILED state yet, assume that the job was finished
        state: JobStatus = JobStatus.FINISHED
        return Response(json.dumps(state.to_texoo_dict()), status=200, mimetype='application/json')


@app.route("/startjob", methods=['POST'])
def submit_job():
    json_content = request.get_json(force=True)
    job_container = JobContainer.from_json(json_content)
    job: Job = job_container.mljob
    if job.type == JobType.TRAIN:
        logger.info("Starting train job with id {}".format(job.uid))
        train_job = TrainJob.options(max_concurrency=2).remote(job_container)
        jobs[str(job.uid)] = train_job
        train_job.train.remote(config, kb_dataset, gpu_ids)
        return Response(None, status=200)
    elif job.type == JobType.PREDICT:
        logger.info("Starting predict job with id {}".format(job.uid))
        predict_job = PredictJob.options(max_concurrency=2).remote(job_container)
        jobs[str(job.uid)] = predict_job
        predict_job.predict.remote(config, kb_dataset, gpu_ids)
        return Response(None, status=200)
    return Response('Unsupported job type', status=400)


if __name__ == '__main__':
    ray.init(num_gpus=len(gpu_ids))
    serve(app, host="0.0.0.0", port=4567, threads=4, max_request_body_size=16 * 1024 * 1024 * 1024)
