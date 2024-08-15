import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class CertificateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")

        # Small window cuz glitch ( don't ask me how this fixes it, it just works)
        self.root.geometry("800x600")

        # Load certificate template
        self.template_path = filedialog.askopenfilename(title="Select Certificate Template", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        self.template_image = Image.open(self.template_path)

        # Scale the certificate for preview purposes 700 X 400
        self.preview_scale_factor = min(700 / self.template_image.width, 400 / self.template_image.height)
        self.preview_image = self.template_image.resize(
            (int(self.template_image.width * self.preview_scale_factor), 
             int(self.template_image.height * self.preview_scale_factor)), 
            Image.Resampling.LANCZOS
        )

        self.font_name = tk.StringVar(value="Helvetica")
        self.font_size = 48  #standard font size
        self.preview_text = "Preview Name"
        self.text_position_y = 300  # Only y-coordinate; x will be centered
        self.locked_text_position_y = int(self.text_position_y * self.preview_scale_factor)
        self.locked_font_size = int(self.font_size * self.preview_scale_factor)

        # Load all fonts from the C:/Windows/Fonts directory
        self.font_paths = self.load_fonts()

        self.setup_ui()
        self.update_preview()

    def load_fonts(self):
        font_dir = "C:/Windows/Fonts"
        font_files = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
        font_paths = {}
        for font_file in font_files:
            try:
                font_name = ImageFont.truetype(os.path.join(font_dir, font_file)).getname()[0]
                font_paths[font_name] = os.path.join(font_dir, font_file)
            except Exception as e:
                print(f"Could not load font {font_file}: {e}")
        return font_paths

    def setup_ui(self):
        # Font selection
        font_label = tk.Label(self.root, text="Select Font:")
        font_label.grid(row=0, column=0, sticky="e")
        font_options = list(self.font_paths.keys())
        font_menu = tk.OptionMenu(self.root, self.font_name, *font_options, command=lambda _: self.update_preview())
        font_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Font size
        size_label = tk.Label(self.root, text="Font Size:")
        size_label.grid(row=1, column=0, sticky="e")
        font_sizes = [12, 24, 36, 48, 60, 72, 84]  # Popular font sizes
        size_menu = tk.OptionMenu(self.root, tk.StringVar(value=str(self.font_size)), *font_sizes, command=self.set_font_size)
        size_menu.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Names input field
        names_label = tk.Label(self.root, text="Enter Names (comma-separated):")
        names_label.grid(row=2, column=0, sticky="e")
        self.names_entry = tk.Entry(self.root, width=50)
        self.names_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Preview canvas
        self.canvas = tk.Canvas(self.root, width=700, height=400)
        self.canvas.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.canvas.bind("<B1-Motion>", self.drag_text)
        self.canvas.bind("<ButtonRelease-1>", self.lock_position)

        # Generate Certificates button
        generate_button = tk.Button(self.root, text="Generate Certificates", command=self.generate_certificates)
        generate_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        # Disable window resize behavior
        self.root.resizable(False, False)

    def set_font_size(self, selected_size):
        self.font_size = int(selected_size)
        self.locked_font_size = int(self.font_size * self.preview_scale_factor)
        self.update_preview()

    def update_preview(self):
        # Draw the text on the template image
        preview_copy = self.preview_image.copy()

        # Get the font path from the mapping
        font_path = self.font_paths.get(self.font_name.get(), "C:/Windows/Fonts/arial.ttf")
        font = ImageFont.truetype(font_path, self.locked_font_size)

        # Center the text horizontally
        text_bbox = font.getbbox(self.preview_text)
        text_width = text_bbox[2] - text_bbox[0]
        center_x = (self.preview_image.width - text_width) // 2
        self.locked_text_position = [center_x, self.locked_text_position_y]

        draw = ImageDraw.Draw(preview_copy)
        draw.text(self.locked_text_position, self.preview_text, font=font, fill="black")

        # Convert to ImageTk for tkinter
        self.tk_image = ImageTk.PhotoImage(preview_copy)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(width=self.preview_image.width, height=self.preview_image.height)

    def drag_text(self, event):
        # Update text position during drag (only y-coordinate)
        self.locked_text_position_y = event.y
        self.update_preview()

    def lock_position(self, event):
        # Finalize position when drag is done (only y-coordinate)
        self.locked_text_position_y = event.y
        self.update_preview()

    def generate_certificates(self):
        if not self.locked_text_position or not self.locked_font_size:
            messagebox.showwarning("Error", "Please adjust and lock the name position before generating.")
            return

        names = [name.strip() for name in self.names_entry.get().split(',')]
        if not names:
            messagebox.showwarning("Input Error", "Please enter at least one name.")
            return

        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return

        font_path = self.font_paths.get(self.font_name.get(), "C:/Windows/Fonts/arial.ttf")

        for name in names:
            # Use original image for final output
            final_image = self.template_image.copy()

            # Recalculate position and font size for the original image size
            final_text_position_y = int(self.locked_text_position_y / self.preview_scale_factor)
            final_font_size = int(self.locked_font_size / self.preview_scale_factor)

            font = ImageFont.truetype(font_path, final_font_size)

            # Center the text horizontally on the original image
            text_bbox = font.getbbox(name)
            text_width = text_bbox[2] - text_bbox[0]
            center_x = (self.template_image.width - text_width) // 2
            final_text_position = [center_x, final_text_position_y]

            draw = ImageDraw.Draw(final_image)
            draw.text(final_text_position, name, font=font, fill="black")

            output_path = os.path.join(output_dir, f"certificate_{name}.png")
            final_image.save(output_path)

        messagebox.showinfo("Success", "Certificates generated successfully!")

# Main application loop
root = tk.Tk()
app = CertificateApp(root)
root.mainloop()