import os
from browser_use import Agent, Browser, ChatOpenAI

class BaseAgentWrapper:
    def __init__(self, task: str):
        # Browser configuration
        self.browser = Browser(
            headless=True,
            viewport={"width": 1920, "height": 1080}
        )
        # LLM configuration
        self.llm = ChatOpenAI(model="gpt-4.1")  # Reads OPENAI_API_KEY

        # Create Browser-Use Agent
        self.agent = Agent(browser=self.browser, task=task, llm=self.llm)

    async def run_structured(self, max_steps=20):
        """
        Run the agent and return a structured result:
        {"success": bool, "output": str}
        """
        try:
            history = await self.agent.run(max_steps=max_steps)
            last_step = getattr(history, "last_step", None)
            if not last_step:
                return {"success": False, "output": "No steps completed"}

            success = getattr(last_step, "success", True)
            output = getattr(last_step, "output", str(last_step))
            return {"success": success, "output": output}
        except Exception as e:
            return {"success": False, "output": f"Agent failed: {str(e)}"}

def make_base_agent(task: str):
    """
    Factory function for creating BaseAgentWrapper
    """
    return BaseAgentWrapper(task)