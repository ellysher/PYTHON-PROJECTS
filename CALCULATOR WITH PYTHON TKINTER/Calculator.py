import tkinter as tk
from tkinter import font as tkfont
import re

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("300x400")
        self.master.minsize(250, 350)
        self.master.configure(bg="#f0f0f0")
        
        # Set the window icon (using a title instead of an icon file)
        self.master.title("🧮 Calculator")
        
        # Variables
        self.current_expression = ""
        self.total_expression = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        # Create and configure custom fonts
        self.display_font = tkfont.Font(family="Arial", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=12)
        
        # Create the display and buttons
        self.create_display()
        self.create_buttons()
        
        # Configure grid weight to make the interface responsive
        for i in range(5):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.master.grid_columnconfigure(i, weight=1)

    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.master, bg="#e0e0e0", highlightbackground="#999", 
                                highlightthickness=1)
        display_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Configure display frame to be responsive
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Display label
        self.display = tk.Label(display_frame, textvariable=self.display_var, 
                             font=self.display_font, bg="#e0e0e0", anchor="e", padx=10, pady=10)
        self.display.grid(row=0, column=0, sticky="nsew")

    def create_buttons(self):
        # Button styles
        button_style = {
            "font": self.button_font,
            "borderwidth": 1,
            "relief": tk.RAISED,
            "padx": 10,
            "pady": 10
        }
        
        # Define buttons with their grid positions, colors, and callbacks
        buttons = [
            {"text": "C", "row": 1, "column": 0, "bg": "#ff9999", "command": self.clear},
            {"text": "(", "row": 1, "column": 1, "bg": "#ccccff", "command": lambda: self.add_to_expression("(")},
            {"text": ")", "row": 1, "column": 2, "bg": "#ccccff", "command": lambda: self.add_to_expression(")")},
            {"text": "÷", "row": 1, "column": 3, "bg": "#ccccff", "command": lambda: self.add_to_expression("/")},
            
            {"text": "7", "row": 2, "column": 0, "bg": "#ffffff", "command": lambda: self.add_to_expression("7")},
            {"text": "8", "row": 2, "column": 1, "bg": "#ffffff", "command": lambda: self.add_to_expression("8")},
            {"text": "9", "row": 2, "column": 2, "bg": "#ffffff", "command": lambda: self.add_to_expression("9")},
            {"text": "×", "row": 2, "column": 3, "bg": "#ccccff", "command": lambda: self.add_to_expression("*")},
            
            {"text": "4", "row": 3, "column": 0, "bg": "#ffffff", "command": lambda: self.add_to_expression("4")},
            {"text": "5", "row": 3, "column": 1, "bg": "#ffffff", "command": lambda: self.add_to_expression("5")},
            {"text": "6", "row": 3, "column": 2, "bg": "#ffffff", "command": lambda: self.add_to_expression("6")},
            {"text": "-", "row": 3, "column": 3, "bg": "#ccccff", "command": lambda: self.add_to_expression("-")},
            
            {"text": "1", "row": 4, "column": 0, "bg": "#ffffff", "command": lambda: self.add_to_expression("1")},
            {"text": "2", "row": 4, "column": 1, "bg": "#ffffff", "command": lambda: self.add_to_expression("2")},
            {"text": "3", "row": 4, "column": 2, "bg": "#ffffff", "command": lambda: self.add_to_expression("3")},
            {"text": "+", "row": 4, "column": 3, "bg": "#ccccff", "command": lambda: self.add_to_expression("+")},
            
            {"text": "0", "row": 5, "column": 0, "columnspan": 2, "bg": "#ffffff", "command": lambda: self.add_to_expression("0")},
            {"text": ".", "row": 5, "column": 2, "bg": "#ffffff", "command": lambda: self.add_to_expression(".")},
            {"text": "=", "row": 5, "column": 3, "bg": "#99ff99", "command": self.evaluate}
        ]
        
        # Create all buttons
        for button in buttons:
            btn = tk.Button(self.master, text=button["text"], bg=button["bg"], 
                          command=button["command"], **button_style)
            
            # Determine column span
            columnspan = button.get("columnspan", 1)
            
            # Add hover effect
            btn.bind("<Enter>", lambda event, b=btn: self.on_button_hover(event, b))
            btn.bind("<Leave>", lambda event, b=btn: self.on_button_leave(event, b))
            
            # Position the button
            btn.grid(row=button["row"], column=button["column"], 
                    columnspan=columnspan, padx=2, pady=2, sticky="nsew")

    def on_button_hover(self, event, button):
        """Change button color on hover"""
        current_bg = button.cget("background")
        # Darken the button slightly
        if current_bg == "#ffffff":  # Number buttons
            button.configure(background="#f0f0f0")
        elif current_bg == "#ccccff":  # Operator buttons
            button.configure(background="#aaaaee")
        elif current_bg == "#99ff99":  # Equals button
            button.configure(background="#77dd77")
        elif current_bg == "#ff9999":  # Clear button
            button.configure(background="#ee7777")

    def on_button_leave(self, event, button):
        """Restore button color when mouse leaves"""
        text = button.cget("text")
        # Restore original color
        if text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            button.configure(background="#ffffff")
        elif text in ["+", "-", "×", "÷", "(", ")"]:
            button.configure(background="#ccccff")
        elif text == "=":
            button.configure(background="#99ff99")
        elif text == "C":
            button.configure(background="#ff9999")

    def add_to_expression(self, value):
        """Add the given value to the expression and update the display"""
        # If the display shows an error or just "0", clear it first
        current_display = self.display_var.get()
        if current_display == "Error" or current_display == "0":
            self.current_expression = ""
        
        # Append the new value to the expression
        self.current_expression += value
        
        # Update the display
        self.display_var.set(self.format_expression(self.current_expression))

    def format_expression(self, expression):
        """Format the expression for display by replacing operators with symbols"""
        # Replace operators with more readable symbols
        formatted = expression.replace("*", "×").replace("/", "÷")
        return formatted

    def clear(self):
        """Clear the current expression and reset the display"""
        self.current_expression = ""
        self.display_var.set("0")

    def evaluate(self):
        """Evaluate the current expression and display the result"""
        if not self.current_expression:
            return
            
        try:
            # Use regular expression to validate the expression (optional)
            if not self.is_valid_expression(self.current_expression):
                self.display_var.set("Error")
                return
                
            # Safe evaluation using Python's eval
            result = eval(self.current_expression)
            
            # Format the result
            if isinstance(result, float):
                # Remove trailing zeros for float results
                result_str = str(result)
                if result_str.endswith('.0'):
                    result_str = result_str[:-2]
                self.display_var.set(result_str)
            else:
                self.display_var.set(str(result))
                
            # Update the current expression to the result for continued calculations
            self.current_expression = str(result)
            
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by zero")
            self.current_expression = ""
        except Exception as e:
            self.display_var.set("Error")
            self.current_expression = ""

    def is_valid_expression(self, expression):
        """Check if the expression is valid to prevent security issues with eval()"""
        # Check for valid characters only
        valid_pattern = r'^[0-9\+\-\*\/\(\)\.\s]*$'
        return bool(re.match(valid_pattern, expression))

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
