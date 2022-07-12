from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

import agentmodel.model as model
import agentmodel.tools.func as func
import setting

def main():
    chart = ChartModule(
        [
            {
                "Label": "SegregationRate",
                "Color": "Black"
            }
        ],
        data_collector_name='datacollector'
    )
    
    grid = CanvasGrid(
        func.agent_portrayal, 
        setting.GRID_WIDTH, 
        setting.GRID_HEIGHT, 
        setting.CANVAS_WIDTH, 
        setting.CANVAS_HEIGHT
    )
    server = ModularServer(
        model.SegregationModel, 
        [grid, chart], 
        "segregation Model", 
        {
            "num":setting.N,
            "width":setting.GRID_WIDTH, 
            "height":setting.GRID_HEIGHT, 
            "rate":setting.RATE,
            "moving_range":setting.MOVING_RANGE,
            "satisfaction":setting.SATISFACTION,
            "condition_contract":setting.CONTRACT
        }
    )
    server.port = setting.PORT
    server.launch()         
    

if __name__ == "__main__":
    main()