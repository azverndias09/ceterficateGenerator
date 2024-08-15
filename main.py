import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from font_selector import FontSizeSelector
from color_selector import FontColorSelector

class CertificateGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Certificate Generator")
        self.master.geometry("1000x850")  # Increased height to 850
        self.master.resizable(False, False)

        # Initialize variables
        self.template_image = None
        self.font_dict = self.load_fonts()
        self.selected_font = tk.StringVar()
        self.text_position = (0, 0)
        self.names = []
        self.preview_text = "John Doe"
        self.text_color = "#000000"  # Default color is black

        # Snap threshold in pixels
        self.snap_threshold = 20

        # Track the offset between the cursor and text position
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Setup UI
        self.setup_ui()

        # Set default font
        default_font = "Arial"  # Change this to whatever default font you prefer
        if default_font in self.font_dict:
            self.selected_font.set(default_font)
        self.update_preview()

    def load_fonts(self):
        font_dir = "C:/Windows/Fonts"
        font_files = [f for f in os.listdir(font_dir) if f.lower().endswith(('.ttf', '.otf'))]
        font_dict = {}
        for font_file in font_files:
            try:
                font_path = os.path.join(font_dir, font_file)
                font = ImageFont.truetype(font_path, 12)
                font_name = font.getname()[0]
                font_dict[font_name] = font_path
            except Exception as e:
                print(f"Error loading font {font_file}: {e}")
        return font_dict

    def setup_ui(self):
        # Template selection
        tk.Button(self.master, text="Select Certificate Template", command=self.load_template).pack(pady=10)

        # Font selection
        font_frame = tk.Frame(self.master)
        font_frame.pack(pady=10)
        
        # Font Selection with Scrollable Combobox
        tk.Label(font_frame, text="Select Font: ").pack(side=tk.LEFT)
        self.font_combobox = ttk.Combobox(font_frame, textvariable=self.selected_font, values=list(self.font_dict.keys()), width=30)
        self.font_combobox.pack(side=tk.LEFT, padx=5)
        self.font_combobox.bind("<<ComboboxSelected>>", lambda _: self.update_preview())

        # Font Size Selector (auto-update on size change)
        self.font_size_selector = FontSizeSelector(font_frame, initial_size=48, update_callback=self.update_preview)
        self.font_size_selector.pack(side=tk.LEFT, padx=20)
        
        # Font Color Selector
        color_frame = tk.Frame(self.master)
        color_frame.pack(pady=10)
        tk.Label(color_frame, text="Select Font Color: ").pack(side=tk.LEFT)
        self.font_color_selector = FontColorSelector(color_frame, initial_color=self.text_color, update_callback=self.update_preview)
        self.font_color_selector.pack(side=tk.LEFT, padx=20)
        
        # Names input
        names_frame = tk.Frame(self.master)
        names_frame.pack(pady=10)
        tk.Label(names_frame, text="Enter Names (comma-separated): ").pack(side=tk.LEFT)
        self.names_entry = tk.Entry(names_frame, width=50)
        self.names_entry.pack(side=tk.LEFT, padx=5)

        # Generate button (moved to the top of the preview window)
        tk.Button(self.master, text="Generate Certificates", command=self.generate_certificates).pack(pady=10)

        # Placeholder for canvas dimensions
        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="grey")
        self.canvas.pack(pady=10)
        self.canvas_text = None
        self.canvas.bind("<B1-Motion>", self.move_text)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<ButtonRelease-1>", self.set_text_position)

    def load_template(self):
        template_path = filedialog.askopenfilename(title="Select Certificate Template", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if template_path:
            self.template_image = Image.open(template_path).convert("RGB")
            self.adjust_canvas_aspect_ratio()
            self.display_template()

    def adjust_canvas_aspect_ratio(self):
        # Adjust canvas size based on the aspect ratio of the template image
        template_width, template_height = self.template_image.size
        aspect_ratio = template_width / template_height

        # Define maximum dimensions for the canvas
        max_canvas_width = 800
        max_canvas_height = 500

        if aspect_ratio >= 1:  # Wide image
            self.canvas_width = max_canvas_width
            self.canvas_height = int(self.canvas_width / aspect_ratio)
        else:  # Tall image
            self.canvas_height = max_canvas_height
            self.canvas_width = int(self.canvas_height * aspect_ratio)

        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

    def display_template(self):
        if not self.template_image:
            return
        self.preview_image = self.template_image.copy()
        self.preview_image = self.preview_image.resize((self.canvas_width, self.canvas_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.preview_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.update_preview()

    def update_preview(self):
        if not self.template_image or self.selected_font.get() == "Select Font":
            return
        self.preview_image = self.template_image.copy()
        self.preview_image = self.preview_image.resize((self.canvas_width, self.canvas_height), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(self.preview_image)
        try:
            font_path = self.font_dict[self.selected_font.get()]
            font_size = self.font_size_selector.font_size.get()  # Get the font size from the selector
            font = ImageFont.truetype(font_path, font_size)
            text_color = self.font_color_selector.selected_color.get()  # Get the color from the color selector
        except Exception as e:
            messagebox.showerror("Font Error", f"Error loading font: {e}")
            return

        # Calculate text dimensions
        text_bbox = draw.textbbox((0, 0), self.preview_text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        # Center the text horizontally and position it vertically based on user input
        position_x = (self.canvas_width - text_width) // 2
        position_y = self.text_position[1]

        # Update position
        self.text_position = (position_x, position_y)

        # Draw text
        draw.text(self.text_position, self.preview_text, font=font, fill=text_color)
        self.tk_image = ImageTk.PhotoImage(self.preview_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def start_drag(self, event):
        # Calculate offset when drag starts
        draw = ImageDraw.Draw(self.preview_image)
        font_path = self.font_dict[self.selected_font.get()]
        font = ImageFont.truetype(font_path, self.font_size_selector.font_size.get())
        text_bbox = draw.textbbox((0, 0), self.preview_text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        # Calculate offsets from the cursor to the center of the text
        self.drag_offset_x = event.x - (self.text_position[0] + text_width // 2)
        self.drag_offset_y = event.y - (self.text_position[1] + text_height // 2)

    def move_text(self, event):
        if not self.template_image:
            return
        # Calculate the center positions
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2

        # Get text width for accurate centering
        draw = ImageDraw.Draw(self.preview_image)
        font_path = self.font_dict[self.selected_font.get()]
        font = ImageFont.truetype(font_path, self.font_size_selector.font_size.get())
        text_bbox = draw.textbbox((0, 0), self.preview_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]

        # Adjust position based on drag offset
        adjusted_x = event.x - self.drag_offset_x - text_width // 2
        adjusted_y = event.y - self.drag_offset_y

        # Snap to center if within threshold
        snap_x = adjusted_x if abs(adjusted_x + text_width // 2 - center_x) > self.snap_threshold else center_x - text_width // 2
        snap_y = adjusted_y if abs(adjusted_y - center_y) > self.snap_threshold else center_y

        self.text_position = (snap_x, snap_y)
        self.update_preview()

    def set_text_position(self, event):
        self.move_text(event)

    def generate_certificates(self):
        names_input = self.names_entry.get()
        
        # Automatically replace newlines with commas and split names
        names_input = names_input.replace("\n", ",")
        
        if not names_input:
            messagebox.showerror("Input Error", "Please enter at least one name.")
            return
        
        self.names = [name.strip() for name in names_input.split(',') if name.strip()]
        
        if not self.names:
            messagebox.showerror("Input Error", "Please enter valid names.")
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return

        for name in self.names:
            cert_image = self.template_image.copy()
            draw = ImageDraw.Draw(cert_image)
            try:
                font_path = self.font_dict[self.selected_font.get()]
                font_size = int(self.font_size_selector.font_size.get() * (self.template_image.width / self.canvas_width))
                font = ImageFont.truetype(font_path, font_size)
                text_color = self.font_color_selector.selected_color.get()
            except Exception as e:
                messagebox.showerror("Font Error", f"Error loading font: {e}")
                return

            # Calculate text dimensions for each name
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            # Center the text horizontally and adjust the vertical position
            position_x = (self.template_image.width - text_width) // 2
            position_y = int(self.text_position[1] * (self.template_image.height / self.canvas_height))

            # Draw text
            draw.text((position_x, position_y), name, font=font, fill=text_color)
            output_path = os.path.join(output_dir, f"certificate_{name}.pdf")
            cert_image.save(output_path, "PDF", resolution=100.0)

        messagebox.showinfo("Success", "Certificates generated successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateGenerator(root)
    root.mainloop()
