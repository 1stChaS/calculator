"""View represents the HTML files, which interact with the end user."""
import tkinter as tk
from tkinter import ttk
from math import exp, log, log10, log2, sqrt, factorial


class calculatorView(tk.Tk):
    """User Interface"""
    def __init__(self):
        self.title('Calculator')
        super().__init__()
        self.display = None
        self.history_text = None
        self.error_label = None
        self.history = []  # Maintain a history list
        self.init_components()

    def init_components(self):
        """Create components and layout the UI."""
        # Create a frame for history
        history_frame = tk.Frame(self)
        history_frame.pack(side=tk.TOP, anchor=tk.NE, fill=tk.X, expand=False)
        self.history_text = tk.Text(history_frame, height=7, state='disabled',
                                    font=('Verdana', 15), padx=15, pady=15)
        self.history_text.tag_configure("right", justify="right")
        self.history_text.pack(side=tk.TOP, anchor=tk.E, fill=tk.X, expand=False)

        # Create a label for error messages
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=False)

        self.display = tk.Text(self, height=2, state='disabled',
                               font=('Verdana', 15), padx=15, pady=15)
        self.display.tag_configure("right", justify="right")
        self.display.pack(side=tk.TOP, fill=tk.X, expand=False)

        keypad = self.make_keypad()
        operators = self.make_operator_pad()

        keypad.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        operators.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    def insert_function(self, func):
        """Insert a mathematical function based on the current input."""
        current_text = self.display.get('1.0', 'end-1c').strip()
        if current_text and current_text[-1] in ['+', '-', '*', '/']:
            # If the last character is an operator, insert the function
            self.display.configure(state='normal')
            self.display.insert(tk.END, func, "right")
            self.display.configure(state='disabled')
        else:
            # Otherwise, just insert the function
            self.display.configure(state='normal')
            self.display.insert(tk.END, func, "right")
            self.display.configure(state='disabled')

    def check_expression_validity(self, expression):
        """Check the validity of the expression."""
        try:
            eval(expression)
            return True
        except Exception as e:
            self.show_error(str(e))
            return False

    def show_error(self, message):
        """Display an error message on the UI."""
        self.error_label.configure(text=message)

    def clear_error(self):
        """Clear the error message on the UI."""
        self.error_label.configure(text="")

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
        functions = ['exp', 'sqrt', 'ln', 'log10', 'log2']
        combo = ttk.Combobox(frame, values=functions, state="readonly")
        combo.set("exp")  # Set the default function
        combo.grid(row=len(basic_operators), column=0, padx=2, pady=2, sticky="nsew")
        combo.bind("<<ComboboxSelected>>", lambda event: self.on_button_click(combo.get()))

        # Create buttons for (, ), DEL, and CLR
        parentheses_buttons = ['(', ')']
        del_clr_buttons = ['DEL', 'CLR']
        for i, button_text in enumerate(parentheses_buttons + del_clr_buttons):
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
