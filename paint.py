import customtkinter as ctk
import numpy as np
from PIL import Image, ImageDraw
from tkinter import filedialog, messagebox


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grayscale Paint App")

        ctk.set_appearance_mode("dark")

        # Canvas not created yet
        self.canvas = None
        self.image = None
        self.draw = None

        self.brush_size = 10
        self.brush_color = ctk.IntVar(value=255)  # grayscale 0–255

        # UI Layout
        self.init_ui()

    def init_ui(self):
        controls = ctk.CTkFrame(self.root)
        controls.pack(side="left", fill="y", padx=10, pady=10)

        # Canvas size entry
        ctk.CTkLabel(controls, text="Canvas Width").pack(pady=5)
        self.width_entry = ctk.CTkEntry(controls)
        self.width_entry.insert(0, "400")
        self.width_entry.pack()

        ctk.CTkLabel(controls, text="Canvas Height").pack(pady=5)
        self.height_entry = ctk.CTkEntry(controls)
        self.height_entry.insert(0, "400")
        self.height_entry.pack()

        ctk.CTkButton(controls, text="Create Canvas",
                      command=self.create_canvas).pack(pady=10)

        # Brush control
        ctk.CTkLabel(controls, text="Brush Size").pack(pady=5)
        self.size_slider = ctk.CTkSlider(
            controls, from_=1, to=50,
            command=self.update_brush_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack()

        # Color slider (0-255 grayscale)
        ctk.CTkLabel(controls, text="Brush Color (Gray 0–255)").pack(pady=5)
        ctk.CTkSlider(
            controls, from_=0, to=255,
            variable=self.brush_color
        ).pack()

        ctk.CTkButton(controls, text="Clear Canvas",
                      command=self.clear_canvas).pack(pady=10)

        ctk.CTkButton(controls, text="Save as .png",
                      command=self.save_png).pack(pady=5)

        ctk.CTkButton(controls, text="Save Matrix (0–1)",
                      command=self.save_matrix).pack(pady=5)

    def create_canvas(self):
        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
        except:
            messagebox.showerror("Error", "Width/Height must be numbers")
            return

        # Remove previous canvas if exists
        if self.canvas:
            self.canvas.destroy()

        self.canvas = ctk.CTkCanvas(self.root, width=w, height=h, bg="black")
        self.canvas.pack(side="left", padx=1, pady=10)

        # Create a Pillow image for saving
        self.image = Image.new("L", (w, h), 0)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.draw_event)

    def update_brush_size(self, val):
        self.brush_size = int(float(val))

    def draw_event(self, event):
        if self.image is None:
            return

        x, y = event.x, event.y
        c = int(self.brush_color.get())
        fill = (c,)

        # Draw circle on screen
        self.canvas.create_oval(
            x - self.brush_size // 2, y - self.brush_size // 2,
            x + self.brush_size // 2, y + self.brush_size // 2,
            fill=f"#{c:02x}{c:02x}{c:02x}", outline="")

        # Draw circle on Pillow image
        self.draw.ellipse(
            [x - self.brush_size // 2, y - self.brush_size // 2,
             x + self.brush_size // 2, y + self.brush_size // 2],
            fill=fill
        )

    def clear_canvas(self):
        if self.canvas:
            self.canvas.delete("all")
        if self.image:
            self.draw.rectangle([0, 0, *self.image.size], fill=0)

    def save_png(self):
        if self.image is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png")])
        if path:
            self.image.save(path)
            messagebox.showinfo("Saved", f"Saved PNG:\n{path}")

    def save_matrix(self):
        if self.image is None:
            return

        arr = np.array(self.image).astype(np.float32) / 255.0

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("TXT", "*.txt"), ("NumPy Binary", "*.npy"),
                       ("CSV", "*.csv")]
        )
        if not path:
            return

        if path.endswith(".npy"):
            np.save(path, arr)
        else:
            np.savetxt(path, arr, fmt="%.6f")

        messagebox.showinfo("Saved", f"Saved matrix:\n{path}")


if __name__ == "__main__":
    root = ctk.CTk()
    PaintApp(root)
    root.mainloop()

