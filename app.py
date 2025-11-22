import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO

# --- CONFIGURATION ---
MODEL_PATH = "weights.pt"
# Coin Values
COIN_VALUES = {
    "5ft": 5,
    "10ft": 10,
    "50ft": 50,
    "100ft": 100,
    "200ft": 200
}

# Color Scheme (BGR Format for OpenCV)
COIN_COLORS = {
    "5ft": (0, 215, 255),  # Gold/Orange
    "10ft": (230, 230, 250),  # Light Silver/Blue
    "50ft": (50, 205, 50),  # Lime Green
    "100ft": (226, 43, 138),  # Purple/Pinkish
    "200ft": (0, 0, 255)  # Bright Red
}
DEFAULT_COLOR = (0, 255, 0)  # Green Fallback

class CoinCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parallel Processing Coin Counter")
        self.root.geometry("1200x800")

        # Load YOLO Model
        print("Loading AI Model...")
        try:
            self.model = YOLO(MODEL_PATH)
            print("Model Loaded Successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            return

        # --- GUI LAYOUT ---
        # Top Bar
        top_frame = tk.Frame(root, bg="#2D2D2D", height=80)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_upload = tk.Button(top_frame, text="📂 Upload Image", command=self.upload_image,
                                    font=("Segoe UI", 14, "bold"), bg="#4CAF50", fg="white",
                                    padx=20, pady=10, borderwidth=0)
        self.btn_upload.pack(side=tk.LEFT, padx=30, pady=15)

        # Main Content Area
        content_frame = tk.Frame(root, bg="#1E1E1E")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Image Display
        self.lbl_image = tk.Label(content_frame, text="No image loaded", bg="#1E1E1E", fg="#888")
        self.lbl_image.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Right: Sidebar stats
        self.txt_details = Text(content_frame, width=35, bg="#2D2D2D", fg="white",
                                font=("Consolas", 12), borderwidth=0)
        self.txt_details.pack(side=tk.RIGHT, fill=tk.Y)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.process_image(file_path)

    def process_image(self, image_path):
        # 1. Run Inference
        results = self.model.predict(source=image_path, conf=0.45)
        result = results[0]

        # Get the image as a numpy array to draw on
        original_image = result.orig_img
        h, w, _ = original_image.shape

        # --- DYNAMIC DRAWING SCALE ---
        draw_scale = max(1.0, w / 1000.0)
        box_thickness = int(4 * draw_scale)
        text_thickness = int(2 * draw_scale)
        font_scale = 0.7 * draw_scale
        padding = int(10 * draw_scale)

        total_value = 0
        coin_counts = {}

        # 2. Loop through detections
        # result.boxes.data contains [x1, y1, x2, y2, conf, class_id]
        for box in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            class_id = int(class_id)

            # Get Label Name directly from the model
            label_name = result.names[class_id]

            # Math
            value = COIN_VALUES.get(label_name, 0)
            total_value += value
            coin_counts[label_name] = coin_counts.get(label_name, 0) + 1

            # --- VISUALIZATION ---
            color = COIN_COLORS.get(label_name, DEFAULT_COLOR)

            # Draw Box
            cv2.rectangle(original_image, (x1, y1), (x2, y2), color, box_thickness)

            # Draw Text Background
            label_text = f"{label_name} {int(score * 100)}%"
            (text_w, text_h), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                                                         text_thickness)
            cv2.rectangle(original_image,
                          (x1, y1 - text_h - padding * 2),
                          (x1 + text_w + padding, y1),
                          color, -1)

            # Draw Text (White text for better contrast on colored boxes)
            cv2.putText(original_image, label_text,
                        (x1 + int(padding / 2), y1 - padding),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), text_thickness)

        # 3. Update Sidebar
        self.txt_details.delete(1.0, tk.END)
        self.txt_details.insert(tk.END, "\n  SUMMARY REPORT\n", "header")
        self.txt_details.insert(tk.END, "  " + "-" * 25 + "\n")

        sorted_coins = sorted(coin_counts.items(), key=lambda item: COIN_VALUES.get(item[0], 0), reverse=True)

        for coin_name, count in sorted_coins:
            # Add colored square to sidebar
            color_rgb = COIN_COLORS.get(coin_name, DEFAULT_COLOR)[::-1]  # BGR to RGB
            color_hex = "#%02x%02x%02x" % color_rgb
            tag_name = f"color_{coin_name}"
            self.txt_details.tag_configure(tag_name, foreground=color_hex, font=("Consolas", 14, "bold"))
            self.txt_details.insert(tk.END, "  ■ ", tag_name)
            line = f"{count}x  {coin_name:<8} = {count * COIN_VALUES.get(coin_name, 0)} Ft\n"
            self.txt_details.insert(tk.END, line)

        self.txt_details.insert(tk.END, "\n  " + "-" * 25 + "\n")
        self.txt_details.insert(tk.END, f"  TOTAL: {total_value} Ft\n", "total")

        self.txt_details.tag_configure("header", font=("Segoe UI", 16, "bold"), foreground="#4CAF50")
        self.txt_details.tag_configure("total", font=("Segoe UI", 20, "bold"), foreground="#FFD700")

        # 4. Display Image
        img_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        display_h = 650
        ratio = display_h / img_pil.height
        display_w = int(img_pil.width * ratio)
        img_pil = img_pil.resize((display_w, display_h), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img_pil)
        self.lbl_image.config(image=img_tk, text="")
        self.lbl_image.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = CoinCounterApp(root)
    root.mainloop()