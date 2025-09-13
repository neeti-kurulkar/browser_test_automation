import os
import asyncio
from browser_use import Agent, Browser, ChatOpenAI

class BaseAgentWrapper:
    def __init__(self, task: str):
        # Browser configuration
        self.browser = Browser(
            headless=True,
            viewport={"width": 1920, "height": 1080}
        )

        # LLM configuration (force JSON mode)
        self.llm = ChatOpenAI(
            model="gpt-4.1"
        )

        # Create Browser-Use Agent
        self.agent = Agent(browser=self.browser, task=task, llm=self.llm)

    async def run_structured(self, max_steps=20, retries=2):
        """
        Run the agent and return a structured result:
        {"success": bool, "output": str}
        Includes retries if DOM fails to load.
        """
        for attempt in range(1, retries + 1):
            try:
                history = await self.agent.run(max_steps=max_steps)
                last_step = getattr(history, "last_step", None)

                if not last_step:
                    if attempt < retries:
                        await asyncio.sleep(5)
                        continue
                    return {"success": False, "output": "No steps completed"}

                success = getattr(last_step, "success", True)
                output = getattr(last_step, "output", str(last_step))

                # Retry if the output looks like "empty DOM" error
                if "empty DOM" in output.lower() and attempt < retries:
                    await asyncio.sleep(5)
                    continue

                return {"success": success, "output": output}

            except Exception as e:
                if attempt < retries:
                    await asyncio.sleep(5)
                    continue
                return {"success": False, "output": f"Agent failed: {str(e)}"}

        return {"success": False, "output": "Retries exhausted"}

def make_base_agent(task: str):
    """
    Factory function for creating BaseAgentWrapper
    """
    return BaseAgentWrapper(task)
