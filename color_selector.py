import tkinter as tk
from tkinter import colorchooser

class FontColorSelector(tk.Frame):
    def __init__(self, master, initial_color="#000000", update_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.selected_color = tk.StringVar(value=initial_color)
        self.update_callback = update_callback  # Callback to update the preview

        # Default colors
        self.default_colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFFFFF"]

        # Color selection buttons
        for color in self.default_colors:
            color_button = tk.Button(self, bg=color, width=2, height=1, command=lambda c=color: self.set_color(c))
            color_button.pack(side=tk.LEFT, padx=5)

        # Eyedropper tool
        self.eyedropper_button = tk.Button(self, text="Pick Color", command=self.pick_color)
        self.eyedropper_button.pack(side=tk.LEFT, padx=5)

        # Selected color display
        self.color_display = tk.Label(self, textvariable=self.selected_color, bg=self.selected_color.get(), width=10)
        self.color_display.pack(side=tk.LEFT, padx=5)

    def set_color(self, color):
        self.selected_color.set(color)
        self.color_display.config(bg=color)
        if self.update_callback:
            self.update_callback()

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.set_color(color_code)

