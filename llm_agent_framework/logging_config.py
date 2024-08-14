# llm_agent_framework/logging_config.py
import logging
import logging.config
import os

def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        import yaml
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# Example usage in a module
if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("This is an info message.")
