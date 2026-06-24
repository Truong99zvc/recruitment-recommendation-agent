import argparse
import asyncio
import sys

from loguru import logger

from jobber.core.system_orchestrator import SystemOrchestrator


def setup_logger(verbose: bool):
    logger.remove()
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add("logs/jobber_{time}.log", rotation="10 MB", level="DEBUG")


async def main():
    parser = argparse.ArgumentParser(description="Jobber AI Agent")
    parser.add_argument("--eval", action="store_true", help="Run in evaluation mode")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    setup_logger(args.verbose)
    logger.info("Starting Jobber...")

    orchestrator = SystemOrchestrator(eval_mode=args.eval)
    await orchestrator.start()


if __name__ == "__main__":
    asyncio.run(main())
