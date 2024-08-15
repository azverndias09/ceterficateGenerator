import tkinter as tk
from tkinter import ttk

class FontSizeSelector(tk.Frame):
    def __init__(self, master, initial_size=12, update_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.font_size = tk.IntVar(value=initial_size)
        self.update_callback = update_callback  # Callback function to update preview

        # Font size presets
        self.presets = [8, 9, 10, 11, 12, 14, 18, 24, 30, 36, 48, 60, 72, 96]
        
        # Minus button
        self.minus_button = tk.Button(self, text="-", command=self.decrement_size)
        self.minus_button.grid(row=0, column=0, padx=(0, 5))

        # Manual entry / dropdown for presets
        self.size_entry = ttk.Combobox(self, values=self.presets, textvariable=self.font_size, width=4)
        self.size_entry.grid(row=0, column=1)
        self.size_entry.bind("<Return>", self.update_font_size)
        self.size_entry.bind("<<ComboboxSelected>>", self.update_font_size)

        # Plus button
        self.plus_button = tk.Button(self, text="+", command=self.increment_size)
        self.plus_button.grid(row=0, column=2, padx=(5, 0))

    def increment_size(self):
        current_size = self.font_size.get()
        self.font_size.set(current_size + 1)
        self.update_font_size()

    def decrement_size(self):
        current_size = self.font_size.get()
        if current_size > 1:
            self.font_size.set(current_size - 1)
        self.update_font_size()

    def update_font_size(self, event=None):
        # Auto-update the preview with the new font size
        if self.update_callback:
            self.update_callback()
