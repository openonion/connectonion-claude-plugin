from connectonion import host
from connectonion.cli.co_ai.agent import create_agent

agent = create_agent(role="coding")
host(agent)
