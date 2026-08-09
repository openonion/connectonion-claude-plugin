from connectonion import Agent, host


def create_agent():
    return Agent("isolated")


host(create_agent)
