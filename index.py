import tkinter as tk
from tkinter import messagebox
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io

class BarcodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerador de Códigos de Barras")
        self.master.geometry("400x600")
        self.master.configure(bg="#f7f7f7")

        self.label = tk.Label(master, text="Insira os códigos de barras (um por linha):", bg="#f7f7f7", font=("Arial", 10))
        self.label.pack(pady=10)

        self.text_area = tk.Text(master, height=10, width=50, font=("Arial", 10), wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.configure(bg="#ffffff", fg="#000000", bd=2, relief="groove")

        self.default_codes = ["ABC123", "DEF456", "GHI789", "JKL012", "MNO345"]
        self.text_area.insert(tk.END, "\n".join(self.default_codes))

        button_frame = tk.Frame(master, bg="#f7f7f7")
        button_frame.pack(pady=10)

        self.generate_button = tk.Button(button_frame, text="Gerar Códigos de Barras", command=self.generate_barcodes, font=("Arial", 10), bg="#4CAF50", fg="white", bd=0)
        self.zpl_button = tk.Button(button_frame, text="Gerar Texto ZPL", command=self.generate_zpl, font=("Arial", 10), bg="#2196F3", fg="white", bd=0)

        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.zpl_button.pack(side=tk.LEFT, padx=5)

        self.image_frame = tk.Frame(master, bg="#f7f7f7")
        self.image_frame.pack(pady=10)

        self.label_img = tk.Label(self.image_frame, bg="#f7f7f7")
        self.label_img.pack()

        self.back_button = tk.Button(master, text="Voltar", command=self.prev_image, font=("Arial", 10), bg="#FFC107", fg="black", bd=0)
        self.next_button = tk.Button(master, text="Próximo", command=self.next_image, font=("Arial", 10), bg="#FFC107", fg="black", bd=0)

        self.back_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.next_button.pack(side=tk.RIGHT, padx=5, pady=10)

        self.image_objects = []
        self.current_index = 0

        self.back_button.pack_forget()
        self.next_button.pack_forget()

    def generate_barcodes(self):
        codes = self.text_area.get("1.0", tk.END).strip().splitlines()
        self.image_objects = []

        for code in codes:
            if code:
                try:
                    font_path = "C:/Windows/Fonts/arial.ttf"
                    barcode_instance = barcode.get('code128', code, writer=ImageWriter())
                    barcode_instance.writer.font_path = font_path
                    buffer = io.BytesIO()
                    barcode_instance.write(buffer)
                    buffer.seek(0)

                    img = Image.open(buffer)
                    self.image_objects.append(img)

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao gerar o código de barras: {e}")

        if self.image_objects:
            self.current_index = 0
            self.show_image()
            self.update_button_visibility()
        else:
            messagebox.showinfo("Atenção", "Nenhum código de barras foi gerado.")
            self.update_button_visibility()

    def generate_zpl(self):
        codes = self.text_area.get("1.0", tk.END).strip().splitlines()
        zpl_text = ""

        for code in codes:
            if code:
                zpl_text += f"^XA^PR6,6,2^PW789\n^FO70,440^BCN,120,Y,N,N^FD{code}^FS\n^PQ1^XZ\n\n"

        if zpl_text:
            self.show_zpl_window(zpl_text)
        else:
            messagebox.showinfo("Atenção", "Nenhum código ZPL gerado.")

    def show_zpl_window(self, zpl_text):
        zpl_window = tk.Toplevel(self.master)
        zpl_window.title("Texto ZPL Gerado")
        zpl_window.geometry("400x300")

        label = tk.Label(zpl_window, text="Texto ZPL gerado:", font=("Arial", 10))
        label.pack(pady=10)

        text_area = tk.Text(zpl_window, height=10, width=50, font=("Arial", 10), wrap=tk.WORD)
        text_area.pack(padx=10, pady=10)
        text_area.insert(tk.END, zpl_text)
        text_area.config(state=tk.NORMAL)

        close_button = tk.Button(zpl_window, text="Fechar", command=zpl_window.destroy, font=("Arial", 10), bg="#f44336", fg="white")
        close_button.pack(pady=10)

        text_area.focus()
        text_area.selection_clear(0, tk.END)

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
        if self.image_objects:
            self.back_button.pack(side=tk.LEFT, padx=5)
            self.next_button.pack(side=tk.RIGHT, padx=5)
            self.back_button.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.current_index < len(self.image_objects) - 1 else tk.DISABLED)
        else:
            self.back_button.pack_forget()
            self.next_button.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeGeneratorApp(root)
    root.mainloop()
