def agent_portrayal(agent) -> dict:
    """ Returns agent drawing information

    Args:
        agent (Resident): agent

    Returns:
        dict: Agent drawing information
    """
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": agent.color,
                 "r": 0.5}
    return portrayal


def compute_segrigate_rate(model) -> float:
    """ Calculate the rate of same agents throughout the space

    Args:
        model (SegregationModel): SegregationModel

    Returns:
        float: Rate of same agents
    """
    num = 0
    sum_segregation = 0
    for agent in model.schedule.agents:
        neighbors_residents = model.grid.get_neighbors(agent.pos, moore=True, include_center=False, radius=1)
        same_residents_num = agent._get_num_same_type_agents(neighbors_residents)
        try:
            sum_segregation += same_residents_num / len(neighbors_residents)
            num += 1
        except ZeroDivisionError:
            print("Skip agent")
    if num == 0:
        return 100
    else:
        return (sum_segregation / num) * 100