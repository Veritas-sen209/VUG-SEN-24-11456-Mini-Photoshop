
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class MiniPhotoshop:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photoshop App")
        self.root.geometry("800x600")
        self.image = None
        self.processed_image = None

        # Buttons
        Button(root, text="Open Image", command=self.open_image).pack(pady=5)
        Button(root, text="Grayscale", command=self.grayscale).pack(pady=5)
        Button(root, text="Blur", command=self.blur).pack(pady=5)
        Button(root, text="Sharpen", command=self.sharpen).pack(pady=5)
        Button(root, text="Edge Detection", command=self.edge_detect).pack(pady=5)
        Button(root, text="Brightness + Contrast", command=self.brightness_contrast).pack(pady=5)
        Button(root, text="Save Image", command=self.save_image).pack(pady=5)

        self.panel = Label(root)
        self.panel.pack()

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"), ("All files","*.*")])
        if path:
            img = cv2.imread(path)
            if img is None:
                messagebox.showerror("Open Image", "Failed to open image. The file may be corrupted or an unsupported format.")
                return
            self.image = img
            self.processed_image = self.image.copy()
            self.display_image(self.image)

    def display_image(self, img):
        if img is None or getattr(img, "size", None) == 0 or (hasattr(img, "ndim") and img.size == 0):
            messagebox.showerror("Display Image", "No image to display.")
            return
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            messagebox.showerror("Image Error", f"OpenCV error while converting image: {e}")
            return

        img_pil = Image.fromarray(img_rgb)

        # Resize preserving aspect ratio to fit within 500x400
        max_w, max_h = 500, 400
        w, h = img_pil.size
        ratio = min(max_w / w, max_h / h, 1.0)
        new_size = (int(w * ratio), int(h * ratio))
        img_tk = ImageTk.PhotoImage(img_pil.resize(new_size, Image.LANCZOS))

        self.panel.configure(image=img_tk)
        self.panel.image = img_tk

    def grayscale(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)

    def blur(self):
        if self.image is not None:
            blur = cv2.GaussianBlur(self.image, (9, 9), 0)
            self.processed_image = blur
            self.display_image(blur)

    def sharpen(self):
        if self.image is not None:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharp = cv2.filter2D(self.image, -1, kernel)
            self.processed_image = sharp
            self.display_image(sharp)

    def edge_detect(self):
        if self.image is not None:
            edges = cv2.Canny(self.image, 100, 200)
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.processed_image = edges_bgr
            self.display_image(edges_bgr)

    def brightness_contrast(self):
        if self.image is not None:
            bright = cv2.convertScaleAbs(self.image, alpha=1.3, beta=40)
            self.processed_image = bright
            self.display_image(bright)

    def save_image(self):
        if self.processed_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG","*.jpg;*.jpeg"),("PNG","*.png"),("All files","*.*")])
            if path:
                success = cv2.imwrite(path, self.processed_image)
                if not success:
                    messagebox.showerror("Save Image", "Failed to save the image.")
                else:
                    messagebox.showinfo("Save Image", "Image saved successfully.")

if __name__ == "__main__":
    root = Tk()
    app = MiniPhotoshop(root)
    root.mainloop()
