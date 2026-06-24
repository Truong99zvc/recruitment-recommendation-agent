import argparse
import asyncio
import sys

from loguru import logger

from jobber_fsm.core.agent.browser_nav_agent import BrowserNavAgent
from jobber_fsm.core.agent.planner_agent import PlannerAgent
from jobber_fsm.core.models.models import State
from jobber_fsm.core.orchestrator.orchestrator import Orchestrator


def setup_logger(verbose: bool):
    logger.remove()
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add("logs/jobber_fsm_{time}.log", rotation="10 MB", level="DEBUG")


async def main():
    parser = argparse.ArgumentParser(description="Jobber FSM AI Agent")
    parser.add_argument("--eval", action="store_true", help="Run in evaluation mode")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    setup_logger(args.verbose)
    logger.info("Starting Jobber FSM...")

    # Define state machine
    state_to_agent_map = {
        State.PLAN: PlannerAgent(),
        State.BROWSE: BrowserNavAgent(),
    }

    orchestrator = Orchestrator(
        state_to_agent_map=state_to_agent_map, eval_mode=args.eval
    )
    await orchestrator.start()


if __name__ == "__main__":
    asyncio.run(main())
