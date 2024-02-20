"""an intermediary between view and model."""
from view import calculatorView
from model import calculatorModel
from math import *


class calculatorController:
    def __init__(self):
        self.model = calculatorModel()
        self.view = calculatorView()

    def on_button_click(self, value):
        """Handle button clicks."""
        self.clear_error()  # Clear any previous error messages

        if value == '=':
            expression = self.view.get('1.0', 'end-1c')
            valid = self.check_expression_validity(expression)

            if valid:
                try:
                    # Replace factorial with custom_factorial
                    expression = expression.replace('factorial', 'self.custom_factorial')
                    result = eval(expression.replace("^", "**"))
                    # Add the expression and result to history
                    history_entry = f"{expression} = {result}\n"
                    self.history.append((expression, result))
                    # Update the history text
                    self.history_text.configure(state='normal')
                    self.history_text.insert(tk.END, history_entry)
                    self.history_text.configure(state='disabled')

                    # Update the display with the result
                    self.display.configure(state='normal')
                    self.display.delete('1.0', tk.END)
                    self.display.insert(tk.END, str(result), "right")
                    self.display.configure(state='disabled')
                except Exception as e:
                    self.show_error(str(e))
            else:
                # Expression is invalid
                self.display.configure(state='normal', fg='red')
                self.bell()  # Make a sound
                self.after(2000, lambda: self.display.configure(fg='black'))  # Restore color after 2 seconds

        elif value == 'DEL':
            self.display.configure(state='normal')
            current_text = self.display.get('1.0', 'end-1c').strip()

            if current_text and current_text[-1] in ['+', '-', '*', '/']:
                # If the last character is an operator, delete the whole operator
                new_text = current_text[:-1]
            elif current_text.endswith("sqrt("):
                # If the expression ends with "sqrt(", delete the whole "sqrt("
                new_text = current_text[:-5]
            elif current_text.endswith("exp(", "log2("):
                # If the expression ends with "exp(" or "log2(", delete the whole "exp(" or "log2("
                new_text = current_text[:-4]
            elif current_text.endswith("ln("):
                # If the expression ends with "ln(", delete the whole "ln("
                new_text = current_text[:-3]
            elif current_text.endswith('log10('):
                # If the expression ends with 'log10(', delete the whole 'log10('
                new_text = current_text[:-6]
            else:
                # Otherwise, delete the last character
                new_text = current_text[:-1]

            self.display.clear_display()
            self.display.update_display(new_text)

            # Check if the color is red and restore it to black
            if self.display.cget("fg") == 'red':
                self.display.configure(fg='black')

        elif value == 'CLR':
            self.display.configure(state='normal')
            self.display.delete('1.0', tk.END)
            self.display.configure(state='disabled')

            # Check if the color is red and restore it to black
            if self.display.cget("fg") == 'red':
                self.display.configure(fg='black')

        elif value == '(' or value == ')':
            self.display.configure(state='normal')
            self.display.insert(tk.END, value, "right")
            self.display.configure(state='disabled')

        elif value in ['exp', 'sqrt', ('ln' or 'log'), 'log10', 'log2']:
            # Handle common mathematical functions
            self.insert_function(f"{value}(")
        else:
            self.display.configure(state='normal')
            self.display.insert(tk.END, value, "right")
            self.display.configure(state='disabled')