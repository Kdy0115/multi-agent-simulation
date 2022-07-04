import mesa
import random
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from .moving import MovingSpanModel

def compute_segrigate_rate(model):
    num = 0
    sum_segregation = 0
    for agent in model.schedule.agents:
        neighbors_residents = model.grid.get_neighbors(agent.pos, moore=True, include_center=False, radius=1)
        same_residents_num = agent._get_num_same_type_agents(neighbors_residents)
        try:
            sum_segregation += same_residents_num / len(neighbors_residents)
            num += 1
        except ZeroDivisionError:
            print("skip agent")
    if num == 0:
        return 100
    else:
        return (sum_segregation / num) * 100



class Resident(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, color, type, threshold, contract_span, moving_area=2):
        super().__init__(unique_id, model)
        self.moving_area         = moving_area
        self.color               = color
        self.type                = type
        self.threshold           = threshold
        self.contract_span       = contract_span
        self.moving_span_model   = MovingSpanModel()
        self.moving_rate         = self.moving_span_model.logistic(self.contract_span)
        
    def _get_num_same_type_agents(self, neighbor_residents_list):
        return len([agent for agent in neighbor_residents_list if self.type == agent.type])
        
    def _check_around_residents(self) -> bool:
        # 周囲の住人の人種をチェックして閾値以上（満足度が高い）なら真を返す
        neighbors_residents = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        same_residents_num = self._get_num_same_type_agents(neighbors_residents)
        try:
            satisfaction_level = same_residents_num / len(neighbors_residents)
        except ZeroDivisionError:
            satisfaction_level = 1.0
        if satisfaction_level > self.threshold:
            return True
        else:
            return False

    def move(self):
        # 周りの多くが同じ人種でなかった（満足度が低い）場合
        if self._check_around_residents() == False:
            # rand = random.random() * 100
            # 引っ越し割合に応じて引っ越す
            # if rand <= self.moving_rate:
                moving_candidate_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=self.moving_area)
                for cell in moving_candidate_list:
                    if self.model.grid.is_cell_empty(cell):
                        self.model.grid.move_agent(self, cell)
                        # self.contract_span = 0

    def step(self):
        self.move()
        # self.contract_span += 1
        # self.moving_rate = self.moving_span_model.logistic(self.contract_span)
        

class SegregationModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, rate, moving_range, satisfaction):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        # Create agents
        for i in range(self.num_agents):
            # contract = random.random() * 10
            contract = 0
            if i < N * rate:
                resident = Resident(i, self, "black", "A", satisfaction, contract, moving_range)
                self._definition_position(resident)
            else:
                resident = Resident(i, self, "blue", "B", satisfaction, contract, moving_range)
                self._definition_position(resident)
        self.datacollector = DataCollector(model_reporters={"SegregationRate": compute_segrigate_rate})                
    
    def _definition_position(self, agent):
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while self.grid.is_cell_empty((x, y)) == False:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)        
            
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()   