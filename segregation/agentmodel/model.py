import mesa
import random
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import agentmodel.tools.func as func
import agentmodel.tools.moving as moving


# Definition type name
Resident = mesa.Agent
SegregationModel = mesa.Model


class Resident(mesa.Agent):
    """ Resident agent class
        This class is overridden from the mesa agent class.
    """

    def __init__(self, unique_id:int, model:SegregationModel, color:str, type:str, satisfaction:float, contract_span:int, moving_range=2) -> None:
        """ Constructor

        Args:
            unique_id (int)              : Agent's unique ID
            model (SegregationModel)     : Space to which the agent belongs
            color (str)                  : Color
            type (str)                   : Type
            satisfaction (float)         : Satisfaction
            contract_span (int)          : Contract span
            moving_range (int, optional) : Range of move
        """        
        super().__init__(unique_id, model)
        self.moving_range        = moving_range
        self.color               = color
        self.type                = type
        self.satisfaction        = satisfaction
        self.contract_span       = contract_span
        
        self.moving_span_model   = moving.MovingSpanModel()
        self.moving_rate         = self.moving_span_model.logistic(self.contract_span)
        
    def _get_num_same_type_agents(self, neighbor_residents_list:list) -> int:
        """ Returns the number of agents of the same type.

        Args:
            neighbor_residents_list (list): List containing surrounding agents

        Returns:
            int: The number of agents of the same type
        """
        return len([agent for agent in neighbor_residents_list if self.type == agent.type])
    
    def _get_current_satisfaction(self) -> float:
        """ Get satisfaction with the current condition of the residence.

        Returns:
            float: Current satisfaction
        """
        # Get all neighbor agents within one cell
        neighbors_residents = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        # Get the number of same agent type
        same_residents_num = self._get_num_same_type_agents(neighbors_residents)
        
        return same_residents_num / len(neighbors_residents) if same_residents_num > 0 else 0
    
    def _check_contract(self) -> bool:
        rand = random.random() * 100
        return True if rand <= self.moving_rate else False
         
    def _check_moving(self) -> bool:
        """ Check if agent is moving out.

        Returns:
            bool: Moving flag
        """
        if self._check_contract():
            current_satisfaction = self._get_current_satisfaction()
            if current_satisfaction < self.satisfaction:
                return True
            else:
                return False
            
        return False

    def _move(self) -> bool:
        """ The agent's moving behavior

        Returns:
            bool: Move success flag
        """
        # Move to an available cell within the moving range.
        moving_candidate_list = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=self.moving_range)
        for cell in moving_candidate_list:
            if self.model.grid.is_cell_empty(cell):
                self.model.grid.move_agent(self, cell)
                return True
        return False
        
    def _reset_contract(self) -> None:
        """ Reset contract span
        """
        self.contract_span = 0
        
    def _update_contract(self) -> None:
        """ Update contract span
        """
        self.contract_span += 1
        self.moving_rate = self.moving_span_model.logistic(self.contract_span)

    def step(self) -> None:
        """ Step-by-step actions of an agent
        """
        if self._check_moving():
            move = self._move()
            if move:
                self._update_contract()
            else:
                self._reset_contract()
        
class SegregationModel(mesa.Model):
    """ Segregation model class
        Simulation space including all agents class.
        This class is overridden from the mesa model class.
    """

    def __init__(self, num:int, width:int, height:int, rate:float, moving_range:int, satisfaction:float, condition_contract:bool) -> None:
        """ Constructor

        Args:
            num (int)                : The number of agents
            width (int)              : Width of space
            height (int)             : Height of space
            rate (float)             : Percentage of the number of agents of the two types.
            moving_range (int)       : Range of move
            satisfaction (float)     : Satisfaction
            condition_contract (bool): Contract
        """
        self.num_agents         = num
        self.grid               = MultiGrid(width, height, True)
        self.schedule           = RandomActivation(self)
        self.running            = True
        self.condition_contract = condition_contract
        # Create agents
        for i in range(self.num_agents):
            if i < self.num_agents * rate:
                self._create_agent(i, "black", "A", satisfaction, moving_range)
            else:
                self._create_agent(i, "blue", "B", satisfaction, moving_range)
        self.datacollector = DataCollector(model_reporters={"SegregationRate": func.compute_segrigate_rate})                
    
    def _create_agent(self, i:int, color:str, type:str, satisfaction:float, moving_range:int) -> None:
        """ Creating agent

        Args:
            i (int)             : Agent ID
            color (str)         : Agent color 
            type (str)          : Resident type
            satisfaction (float): Satisfaction
            moving_range (int)  : Range of move
        """
        if self.condition_contract:
            contract = int(random.random() * 10)
        else:
            contract = 0
        resident = Resident(i, self, color, type, satisfaction, contract, moving_range)
        self._definition_position(resident)
    
    def _definition_position(self, agent:Resident) -> None:
        """ Definition agent's position

        Placing agents in cells in model space
        Args:
            agent (Resident): Resident agent
        """
        # Add the agent to a random grid cell
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        
        while self.grid.is_cell_empty((x, y)) == False:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
        self.grid.place_agent(agent, (x, y))
        self.schedule.add(agent)        
            
    def step(self) -> None:
        """ Step-by-step actions throughout the model space
        """
        self.datacollector.collect(self)
        self.schedule.step()   