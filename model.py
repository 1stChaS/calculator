"""Model: It consists of pure application logic, which interacts with the database.
It includes all the information to represent data to the end user"""
import tkinter as tk


class calculatorModel(tk.Tk):
    """Keypad class"""

    def __init__(self, parent, keynames=None, columns=1, **kwargs):
        # call the superclass constructor with all args except
        super().__init__(parent, **kwargs)
        # keynames and columns
        if keynames is None:
            keynames = []
        # keys = ['1', '2', '3', '4']
        # keypad = Keypad(parent, keynames=keys, columns=2)
        self.keynames = keynames
        self.init_components(columns)

    def init_components(self, columns) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        """
        for key in self.keynames:
            button = tk.Button(self, text=key)
            button.grid(sticky="nsew")
            self.grid_columnconfigure(self.keynames.index(key) % columns, weight=1)
            self.grid_rowconfigure(self.keynames.index(key) // columns, weight=1)
            button.bind("<Button-1>", self.key_handler)

    def key_handler(event):
        """"""
        # don't fix
        key = event.widget['text']
        print("You pressed", key)

    # Keypad.bind("<Button-1>", key_handler)

    def bind(self, todo):
        """Bind an event handler to an event sequence."""
        # Write a bind method with exactly the same parameters
        # as the bind method of Tkinter widgets.
        # Use the parameters to bind all the buttons in the keypad
        # to the same event handler.
        for i in self.winfo_children():
            i.bind(todo)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for i in self.winfo_children():
            i[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        lst = []
        for i in self.winfo_children():
            lst.append(i)
        return lst

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.
        """
        for i in self.winfo_children():
            i.configure(cnf, **kwargs)

    # Write a property named 'frame' the returns a reference to
    # the the superclass object for this keypad.
    # This is so that a programmer can set properties of a keypad's frame,
    # e.g. keypad.frame.configure(background='blue')
    @property
    def frame(self):
        return super()
