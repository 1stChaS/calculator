"""Display the calculator user interface."""
from model import CalculatorModel
from view import CalculatorUI
from controller import CalculatorController

if __name__ == '__main__':
    model = CalculatorModel()
    view = CalculatorUI(model)
    controller = CalculatorController(model, view)
    controller.run()

