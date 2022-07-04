from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

from models.model import SegregationModel
from models.visualization import agent_portrayal
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
        agent_portrayal, 
        setting.GRID_WIDTH, 
        setting.GRID_HEIGHT, 
        setting.CANVAS_WIDTH, 
        setting.CANVAS_HEIGHT
    )
    server = ModularServer(
        SegregationModel, 
        [grid, chart], 
        "segregation Model", 
        {
            "N":setting.N,
            "width":setting.GRID_WIDTH, 
            "height":setting.GRID_HEIGHT, 
            "rate":setting.RATE,
            "moving_range":setting.MOVING_RANGE,
            "satisfaction":setting.SATISFACTION
        }
    )
    server.port = setting.PORT
    server.launch()         

if __name__ == "__main__":
    main()