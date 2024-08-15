import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class CertificateGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Certificate Generator")
        self.master.geometry("1000x800")
        self.master.resizable(False, False)

        # Initialize variables
        self.template_image = None
        self.font_dict = self.load_fonts()
        self.selected_font = tk.StringVar()
        self.selected_font.set("Select Font")
        self.font_size = tk.IntVar()
        self.font_size.set(48)
        self.text_position = (0, 0)
        self.names = []
        self.preview_text = "John Doe"

        # Setup UI
        self.setup_ui()

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
        tk.Label(font_frame, text="Select Font: ").pack(side=tk.LEFT)
        font_menu = tk.OptionMenu(font_frame, self.selected_font, *self.font_dict.keys(), command=lambda _: self.update_preview())
        font_menu.pack(side=tk.LEFT, padx=5)
        tk.Label(font_frame, text="Font Size: ").pack(side=tk.LEFT, padx=20)
        tk.Entry(font_frame, textvariable=self.font_size, width=5).pack(side=tk.LEFT)
        tk.Button(font_frame, text="Update Preview", command=self.update_preview).pack(side=tk.LEFT, padx=10)

        # Names input
        names_frame = tk.Frame(self.master)
        names_frame.pack(pady=10)
        tk.Label(names_frame, text="Enter Names (comma-separated): ").pack(side=tk.LEFT)
        self.names_entry = tk.Entry(names_frame, width=50)
        self.names_entry.pack(side=tk.LEFT, padx=5)

        # Placeholder for canvas dimensions
        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="grey")
        self.canvas.pack(pady=10)
        self.canvas_text = None
        self.canvas.bind("<B1-Motion>", self.move_text)
        self.canvas.bind("<ButtonRelease-1>", self.set_text_position)

        # Generate button
        tk.Button(self.master, text="Generate Certificates", command=self.generate_certificates).pack(pady=10)

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
            font = ImageFont.truetype(font_path, self.font_size.get())
        except Exception as e:
            messagebox.showerror("Font Error", f"Error loading font: {e}")
            return

        # Using textbbox to get text dimensions
        text_bbox = draw.textbbox((0, 0), self.preview_text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        if self.text_position == (0, 0):
            position = ((self.canvas_width - text_width) // 2, (self.canvas_height - text_height) // 2)
            self.text_position = position
        else:
            position = self.text_position
        draw.text(position, self.preview_text, font=font, fill="black")
        self.tk_image = ImageTk.PhotoImage(self.preview_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def move_text(self, event):
        if not self.template_image:
            return
        self.text_position = (event.x, event.y)
        self.update_preview()

    def set_text_position(self, event):
        self.text_position = (event.x, event.y)
        self.update_preview()

    def generate_certificates(self):
        names_input = self.names_entry.get()
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
                # Scale the font size relative to the template size
                scaled_font_size = int(self.font_size.get() * (self.template_image.width / self.canvas_width))
                font = ImageFont.truetype(font_path, scaled_font_size)
            except Exception as e:
                messagebox.showerror("Font Error", f"Error loading font: {e}")
                return

            # Using textbbox to get text dimensions
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            # Calculate position relative to original image size
            position = (
                int(self.text_position[0] * (self.template_image.width / self.canvas_width)),
                int(self.text_position[1] * (self.template_image.height / self.canvas_height))
            )
            draw.text(position, name, font=font, fill="black")
            output_path = os.path.join(output_dir, f"certificate_{name}.pdf")
            cert_image.save(output_path, "PDF", resolution=100.0)

        messagebox.showinfo("Success", "Certificates generated successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateGenerator(root)
    root.mainloop()
