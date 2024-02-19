"""CalculatorUI, with 2 keypads and display area."""

import tkinter as tk
from tkinter import ttk
from math import exp, log, log10, log2, sqrt, factorial

class CalculatorUI(tk.Tk):
    """User Interface for a keypad."""
    def __init__(self):
        super().__init__()
        self.display = None
        self.history_text = None
        self.history = []  # Maintain a history list
        self.init_components()

    def init_components(self):
        """Create components and layout the UI."""
        # Create a frame for history
        history_frame = tk.Frame(self)
        history_frame.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.history_text = tk.Text(history_frame, height=5, state='disabled',
                                    font=('Verdana', 12), padx=14, pady=14)
        self.history_text.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.display = tk.Text(self, height=2, state='disabled',
                               font=('Verdana', 14), padx=14, pady=14)
        self.display.tag_configure("right", justify="right")
        self.display.pack(side=tk.TOP, fill=tk.X, expand=False)

        keypad = self.make_keypad()
        operators = self.make_operator_pad()

        keypad.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        operators.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    def on_button_click(self, value):
        """Handle button clicks."""
        if value == '=':
            try:
                expression = self.display.get('1.0', 'end-1c')
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
                print("Error", e)
        elif value == 'DEL':
            self.display.configure(state='normal')
            current_text = self.display.get('1.0', 'end-1c')
            new_text = current_text[:-1]  # Remove the last character
            self.display.delete('1.0', tk.END)
            self.display.insert(tk.END, new_text, "right")
            self.display.configure(state='disabled')
        elif value == 'CLR':
            self.display.configure(state='normal')
            self.display.delete('1.0', tk.END)
            self.display.configure(state='disabled')
        elif value in ['exp', 'sqrt', 'log', 'log10', 'log2', 'factorial']:
            # Handle common mathematical functions
            current_text = self.display.get('1.0', 'end-1c').strip()
            if current_text:
                # If there's content in the display, apply the function
                self.display.configure(state='normal')
                self.display.delete('1.0', tk.END)
                self.display.insert(tk.END, f"{value}({current_text})", "right")
                self.display.configure(state='disabled')
        else:
            self.display.configure(state='normal')
            self.display.insert(tk.END, value, "right")
            self.display.configure(state='disabled')

    def make_operator_pad(self) -> tk.Frame:
        """Create the operator."""
        frame = tk.Frame(self)

        # Create buttons for basic operators
        basic_operators = ['=', '+', '-', '*', '/']
        for i, operator in enumerate(basic_operators):
            button = tk.Button(frame, text=operator, command=lambda o=operator: self.on_button_click(o))
            button.grid(row=i, column=0, padx=2, pady=2, sticky="nsew")
            frame.grid_rowconfigure(i, weight=1)

        # Create a Combobox for additional functions
        functions = ['exp', 'sqrt', 'log', 'log10', 'log2', 'factorial', '%', '(', ')']
        combo = ttk.Combobox(frame, values=functions, state="readonly")
        combo.set("exp")  # Set the default function
        combo.grid(row=len(basic_operators), column=0, padx=2, pady=2, sticky="nsew")
        combo.bind("<<ComboboxSelected>>", lambda event: self.on_button_click(combo.get()))

        # Create buttons for DEL and CLR
        del_clr_buttons = ['DEL', 'CLR']
        for i, button_text in enumerate(del_clr_buttons):
            button = tk.Button(frame, text=button_text, command=lambda b=button_text: self.on_button_click(b))
            button.grid(row=i, column=1, padx=2, pady=2, sticky="nsew")
            frame.grid_rowconfigure(i, weight=1)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        return frame

    def make_keypad(self) -> tk.Frame:
        """Create the numeric keypad."""
        frame = tk.Frame(self)
        keys = list('789456123 0.')
        for i, key in enumerate(keys):
            button = tk.Button(frame, text=key, command=lambda k=key: self.on_button_click(k))
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2, sticky="nsew")
            frame.grid_columnconfigure(i % 3, weight=1)
            frame.grid_rowconfigure(i // 3, weight=1)
            button.grid(sticky="nsew")
        return frame

    def run(self):
        """Start the application."""
        self.mainloop()