import tkinter as tk
from tkinter import Toplevel, messagebox
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io

class BarcodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerador de Códigos de Barras")

        self.label = tk.Label(master, text="Insira os códigos de barras (um por linha):")
        self.label.pack(pady=10)

        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.default_codes = ["ABC123", "DEF456", "GHI789", "JKL012", "MNO345"]
        self.text_area.insert(tk.END, "\n".join(self.default_codes))

        self.generate_button = tk.Button(master, text="Gerar Códigos de Barras", command=self.generate_barcodes)
        self.generate_button.pack(pady=10)

        self.image_objects = []
        self.current_index = 0

    def generate_barcodes(self):
        codes = self.text_area.get("1.0", tk.END).strip().splitlines()
        self.image_objects = []

        for code in codes:
            if code:
                try:
                    barcode_instance = barcode.get('code128', code, writer=ImageWriter())
                    buffer = io.BytesIO()
                    barcode_instance.write(buffer)
                    buffer.seek(0)

                    img = Image.open(buffer)
                    self.image_objects.append(img)

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao gerar o código de barras: {e}")

        if self.image_objects:
            self.current_index = 0
            self.show_generated_barcode()
        else:
            messagebox.showinfo("Atenção", "Nenhum código de barras foi gerado.")

    def show_generated_barcode(self):
        new_window = Toplevel(self.master)
        new_window.title("Código de Barras Gerado")

        self.label_img = tk.Label(new_window)
        self.label_img.pack(pady=10)

        self.show_image()

        button_frame = tk.Frame(new_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.back_button = tk.Button(button_frame, text="Voltar", command=self.prev_image)
        self.next_button = tk.Button(button_frame, text="Próximo", command=self.next_image)

        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.update_button_visibility()

    def show_image(self):
        img = self.image_objects[self.current_index]
        img = img.resize((300, int(300 * img.height / img.width)), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        self.label_img.config(image=photo)
        self.label_img.image = photo

    def next_image(self):
        if self.current_index < len(self.image_objects) - 1:
            self.current_index += 1
            self.show_image()
            self.update_button_visibility()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
            self.update_button_visibility()

    def update_button_visibility(self):
        if self.current_index == 0:
            self.back_button.pack_forget()
        else:
            self.back_button.pack(side=tk.LEFT, padx=5)

        if self.current_index >= len(self.image_objects) - 1:
            self.next_button.pack_forget() 
        else:
            self.next_button.pack(side=tk.RIGHT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeGeneratorApp(root)
    root.mainloop()
