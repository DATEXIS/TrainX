import logging
import os
from typing import Dict, Any, Tuple, List, Union

import torch

logger = logging.getLogger(__name__)


def get_device() -> Tuple[str, int]:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    n_gpu = None
    if str(device) == 'cuda':
        torch.cuda.empty_cache()
        n_gpu = torch.cuda.device_count()
        logger.info("Number of GPUs: {}".format(n_gpu))
    return str(device), n_gpu


def get_config_from_env() -> Dict[str, Any]:
    config = {
        'batch_size': int(os.getenv('BATCH_SIZE', '128')),
        'epochs': int(os.getenv('EPOCHS', '50')),
        'ner_max_epochs': int(os.getenv('NER_MAX_EPOCHS', '150')),
        'learning_rate': float(os.getenv('LEARNING_RATE', '5e-5')),
        'warmup_steps': int(os.getenv('WARMUP_STEPS', '100')),
        'input_length': int(os.getenv('INPUT_LENGTH', '50')),
        'force_cpu': os.getenv('FORCE_CPU', '').lower() in ['true', '1'],
        'omp_num_threads': int(os.getenv('OMP_NUM_THREADS', 1)),
        'fix_random_seed': not os.getenv('FIX_RANDOM_SEED', '').lower() in ['false', '0'],
        'clip_grad_norm': os.getenv('CLIP_GRAD_NORM', '').lower() in ['true', '1'],
        'paths': {
            'kb': os.getenv('PATH_KB', '/data/kb_texoo.json'),
        },
        'retrain_ner': os.getenv('RETRAIN_NER') in ['True', 'true', '1'],
        'retrain_nel': os.getenv('RETRAIN_NEL') in ['True', 'true', '1'],
        'bert_model': os.getenv('BERT_MODEL', 'bert-base-uncased'),
    }

    if config['force_cpu']:
        config['device'] = 'cpu'
        logger.warning('Forcing CPU usage, did not try to acquire GPU!')
    else:
        config['device'], config['num_gpu'] = get_device()
    logger.info('Using {}'.format(config['device']))

    return config


def get_gpu_ids() -> List[Union[str, None]]:
    if torch.cuda.is_available():
        return ['cuda:{}'.format(n) for n in range(torch.cuda.device_count())]
    else:
        return []
