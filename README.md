
# Certificate Generator

This is a GUI-based Certificate Generator application built using Python and Tkinter. The application allows you to load a certificate template, customize the font style, size, and color, and generate certificates for a list of names. The certificates are saved as PDF files.

## Features

- **Load Certificate Template:** Select an image file (PNG, JPG, etc.) as the certificate template.
- **Font Customization:** Choose from available system fonts, adjust the font size, and select a font color using presets or a color picker.
- **Text Positioning:** Drag and position the text on the certificate preview. Snap to the center for accurate alignment.
- **Preview:** Live preview of the certificate as you make adjustments.
- **Generate Certificates:** Input a list of names (comma-separated), and generate certificates for each name in PDF format.

## Screenshot
![image](https://github.com/user-attachments/assets/5a6e0e3c-2e38-4322-82df-b14c37ed17ad)

## Requirements

- Python 3.8
- `tkinter` (should be included with Python)
- `Pillow` library for image processing
- `reportlab` library for generating PDF files

You can install the required libraries using pip:

```bash
pip install pillow reportlab
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/certificate-generator.git
cd certificate-generator
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

## Direct Usage

1. **Load Template:**
   - Click on the "Select Certificate Template" button to load your certificate template image (Average Canva Template Design as a png format preferrably).

2. **Customize Font:**
   - Select the font from the dropdown.
   - Adjust the font size using the increment/decrement buttons or the dropdown list.
   - Choose a font color using the color picker or default color buttons.

3. **Enter Names:**
   - Input the names (comma-separated or if its from a list where each name is on a new line ( uses \n to differentiate) in the text box.

4. **Position the Text:**
   - Drag the text in the preview to position it on the certificate. The text will snap to the center when close.

5. **Generate Certificates:**
   - Click the "Generate Certificates" button to save certificates for each name in the provided list as PDF files.

## Adding Names from a File (Experimental)

If you have a list of names in a text file, you can load them directly into the application by modifying the code as follows:

- Add the following code in `main.py` after the `load_template` function:

```python
def load_names_from_file(self):
    file_path = filedialog.askopenfilename(title="Select Names File", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            names = file.readlines()
        names = [name.strip() for name in names if name.strip()]
        self.names_entry.insert(0, ', '.join(names))
```

- Add a button in the `setup_ui` method to load names from a file:

```python
tk.Button(self.master, text="Load Names from File", command=self.load_names_from_file).pack(pady=10)
```
## Simple Image Certificate

If you want to check the initial code that just gives you simple image outputs for each certificate, the code for that is simple to read too
Run:
```bash
python imgOutput.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
```

