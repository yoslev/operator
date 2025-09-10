import signal
from globals import *
from lib.azLogger import create_logger
from lib.communicators.libRest.route import create_app
from flask import Flask

logger = create_logger(__name__)

def graceful_shutdown(signum, frame):
    logger.info(f"graceful_shutdown() - Received shutdown signal:[{signum}]. Stopping Operator...")

def main():
  global jobsDict

  APP = create_app()
  return APP

APP: Flask = None
if __name__ == '__main__':
   load_dotenv()
   collectorHost: str = os.getenv("COLLECTOR_HOST", '0.0.0.0')
   collectorPort: int = int(os.getenv("COLLECTOR_PORT", '8000'))
   logger.info("starting COLLECTOR service...v1.0.1")
   logger.info(f"collector http host:[{collectorHost}]")
   logger.info(f"collector http port:[{collectorPort}]")
   APP = main()
   APP.logger.setLevel('INFO')
   APP.run(host=collectorHost, port=collectorPort, debug=False, threaded=True)

signal.signal(signal.SIGINT, graceful_shutdown)   # Ctrl+C
signal.signal(signal.SIGTERM, graceful_shutdown)  # Docker/K8s kill