import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Chỉnh sửa ảnh")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_square)
        self.canvas.bind("<ButtonRelease-1>", self.save_image)

        self.start_x = None
        self.start_y = None

        self.image = None
        self.draw = None
        self.photo_image = None

        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((400, 400))
            self.draw = ImageDraw.Draw(self.image)

            self.photo_image = ImageTk.PhotoImage(self.image)  # Chuyển đổi PIL Image thành PhotoImage
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw_square(self, event):
        if self.start_x is not None and self.start_y is not None:
            current_x = event.x
            current_y = event.y
            self.canvas.delete("square")
            self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                current_x,
                current_y,
                outline="black",
                dash=(5,),
                tags="square",
            )

    def save_image(self, event):
        if self.start_x is not None and self.start_y is not None:
            current_x = event.x
            current_y = event.y
            self.canvas.delete("square")
            square_region = (
                min(self.start_x, current_x),
                min(self.start_y, current_y),
                max(self.start_x, current_x),
                max(self.start_y, current_y),
            )
            cropped_image = self.image.crop(square_region)
            cropped_image.save("result.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
