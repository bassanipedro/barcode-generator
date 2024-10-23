import tkinter as tk
from tkinter import Toplevel, Scrollbar, Canvas, Frame, messagebox
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io
import re

class BarcodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerador de Códigos de Barras")

        self.label = tk.Label(master, text="Insira os códigos de barras (um por linha):")
        self.label.pack(pady=10)

        self.text_area = tk.Text(master, height=10, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.default_code = "ABC123"
        self.text_area.insert(tk.END, self.default_code)

        self.generate_button = tk.Button(master, text="Gerar Códigos de Barras", command=self.generate_barcodes)
        self.generate_button.pack(pady=10)

        self.image_references = []

    def generate_barcodes(self):
        codes = self.text_area.get("1.0", tk.END).strip().splitlines()
        image_objects = []

        for code in codes:
            if code:
                try:
                    barcode_instance = barcode.get('code128', code, writer=ImageWriter())
                    buffer = io.BytesIO()
                    barcode_instance.write(buffer)
                    buffer.seek(0)

                    img = Image.open(buffer)
                    image_objects.append(img)

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao gerar o código de barras: {e}")

        if image_objects:
            self.show_generated_barcodes(image_objects)
        else:
            messagebox.showinfo("Atenção", "Nenhum código de barras foi gerado.")
    
    def show_generated_barcodes(self, image_objects):
        new_window = Toplevel(self.master)
        new_window.title("Códigos de Barras Gerados")

        canvas = Canvas(new_window)
        scrollbar = Scrollbar(new_window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        for img in image_objects:
            try:
                img = img.resize((300, int(300 * img.height / img.width)), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                label_img = tk.Label(scrollable_frame, image=photo)
                label_img.image = photo
                label_img.pack(pady=5)

                self.image_references.append(photo)

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeGeneratorApp(root)
    root.mainloop()
