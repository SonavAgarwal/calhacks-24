import time
from typing import Any, Dict
 
from uagents import Agent, Context, Model

 
class Response(Model):
    timestamp: int
    text: str
    agent_address: str
 
 
# You can also use empty models to represent empty request/response bodies
class EmptyMessage(Model):
    pass
 
 
agent = Agent(name="Rest API")
 
 
@agent.on_rest_get("/rest/get", Response)
async def handle_get(ctx: Context) -> Dict[str, Any]:
    ctx.logger.info("Received GET request")
    return {
        "timestamp": int(time.time()),
        "text": "Hello from the GET handler!",
        "agent_address": ctx.agent.address,
    }
 
 
if __name__ == "__main__":
    agent.run()