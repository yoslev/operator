from dotenv import load_dotenv
import os
from lib.azLogger import create_logger, set_logging_level

logger = create_logger(__name__)

load_dotenv()

sched_redis_poll_interval_sec: int = os.getenv("SCHED_REDIS_POLL_INTERVAL_SEC", 10)
monitor_sched_interval_sec: int = os.getenv("MONITOR_SCHED_INTERVAL_SEC", 10)

log_level_name = os.getenv("LOG_LEVEL_NAME", 'INFO')
set_logging_level(logger=logger, log_level_name=log_level_name)

redisHost: str = os.getenv("REDIS_HOST", 'localhost')
redisPort: int = int(os.getenv("REDIS_PORT", '6379'))
logger.info(f"GLOBALS redisHost:[{redisHost}] redisPort: {redisPort}")

SLACK_SERVICE_URL: str = os.getenv("SLACK_SERVICE_URL")

