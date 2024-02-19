"""module for CalculatorController"""


class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def evaluate_expression(self, expression):
        return self.model.evaluate_expression(expression)

    def clear_history(self):
        self.model.history = []
