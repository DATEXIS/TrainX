# TrainX-NEL

This repository provides the NEL component for the TrainX system.

`--shm-size 32G` should be set.

## Config

TODO write me

```python
def get_config_from_env() -> Dict[str, Any]:
    config = {
        'batch_size': int(os.getenv('BATCH_SIZE', '128')),
        'epochs': int(os.getenv('EPOCHS', '50')),
        'learning_rate': float(os.getenv('LEARNING_RATE', '5e-5')),
        'warmup_steps': int(os.getenv('WARMUP_STEPS', '100')),
        'input_length': int(os.getenv('INPUT_LENGTH', '50')),
        'force_cpu': os.getenv('FORCE_CPU') in ['True', 'true', '1'],
        'omp_num_threads': int(os.getenv('OMP_NUM_THREADS', 1)),
        'fix_random_seed': os.getenv('FIX_RANDOM_SEED', True),
        'paths': {
            'kb': os.getenv('PATH_KB', '/data/kb_texoo.json'),
        },
        'retrain_ner': os.getenv('RETRAIN_NER') in ['True', 'true', '1'],
        'retrain_nel': os.getenv('RETRAIN_NEL') in ['True', 'true', '1'],
    }

    if config['force_cpu']:
        config['device'] = 'cpu'
        logger.warning('Forcing CPU usage, did not try to acquire GPU!')
    else:
        config['device'], config['num_gpu'] = get_device()
    logger.info('Using {}'.format(config['device']))

    return config
```