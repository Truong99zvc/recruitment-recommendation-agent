from datetime import datetime
from string import Template
from typing import Any, Dict

from loguru import logger

from jobber.core.agents.base import BaseAgent
from jobber.core.agents.browser_nav_agent import BrowserNavAgent
from jobber.core.memory import ltm
from jobber.core.prompts import LLM_PROMPTS
from jobber.core.skills.get_screenshot import get_screenshot


class PlannerAgent(BaseAgent):
    def __init__(self) -> None:
        user_ltm: str = self.__get_ltm()
        system_prompt: str = LLM_PROMPTS["PLANNER_AGENT_PROMPT"]

        # Add user ltm to system prompt
        user_ltm_formatted = "\n" + user_ltm
        system_prompt = Template(system_prompt).substitute(
            basic_user_information=user_ltm_formatted
        )

        # Add today's day & date to the system prompt
        today = datetime.now()
        today_date = today.strftime("%d/%m/%Y")
        weekday = today.strftime("%A")
        system_prompt += f"\nToday's date is: {today_date}"
        system_prompt += f"\nCurrent weekday is: {weekday}"

        super().__init__(system_prompt=system_prompt)
        self.browser_agent = BrowserNavAgent(self)

    async def process_query(self, query: str) -> str:
        response: Dict[str, Any] = await super().process_query(query)

        while True:
            # If we get terminate right away from planner
            if response.get("terminate", False):
                return str(response["content"])

            # Process the browser response
            processed_browser_response = await self.browser_agent.process_query(
                response["content"]
            )

            if processed_browser_response.get("terminate", False):
                return str(processed_browser_response["content"])

            # Update the response for the next iteration
            response = processed_browser_response

        # This line should never be reached, but it's good practice to have it
        return "Error: Unexpected end of process_query"

    async def receive_browser_message(self, message: str) -> Dict[str, Any]:
        logger.debug("Received browser message")
        screenshot = await get_screenshot()
        processed_helper_response = await self.generate_reply(
            [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Helper response: {message} \nHere is a screenshot of the current browser page",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"{screenshot}"},
                        },
                    ],
                }
            ],
            self.browser_agent,
        )

        return processed_helper_response

    def __get_ltm(self) -> str:
        return ltm.get_user_ltm()
