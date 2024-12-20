import tkinter as tk
from tkinter import filedialog, messagebox
import os
import PyPDF2

def split_pdf(input_path, output_path, start_page, end_page):
    """
    Extrae un rango de páginas de un PDF.

    Args:
        input_path (str): Ruta del archivo PDF de entrada.
        output_path (str): Ruta del archivo PDF de salida.
        start_page (int): Primera página del rango (base 1).
        end_page (int): Última página del rango (base 1).
    """
    try:
        # Abrir el archivo PDF de entrada
        with open(input_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            
            # Verificar que las páginas sean válidas
            if start_page < 1 or end_page > len(reader.pages) or start_page > end_page:
                return False, "El rango de páginas es inválido."
            
            # Crear un nuevo escritor de PDF
            writer = PyPDF2.PdfWriter()
            
            # Añadir las páginas al nuevo archivo
            for i in range(start_page - 1, end_page):
                writer.add_page(reader.pages[i])
            
            # Guardar el archivo de salida
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
        return True, f"PDF dividido con éxito. Guardado en: {output_path}"
    except Exception as e:
        return False, f"Error al dividir el PDF: {e}"

def select_pdf():
    # Abrir un diálogo para seleccionar el archivo PDF
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_input_path.delete(0, tk.END)
        entry_input_path.insert(0, file_path)

def split_pdf_gui():
    input_path = entry_input_path.get()
    if not os.path.exists(input_path):
        messagebox.showerror("Error", "Por favor, selecciona un archivo PDF válido.")
        return
    
    try:
        start_page = int(entry_start_page.get())
        end_page = int(entry_end_page.get())
    except ValueError:
        messagebox.showerror("Error", "Las páginas deben ser números enteros.")
        return
    
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return
    
    success, message = split_pdf(input_path, output_path, start_page, end_page)
    if success:
        messagebox.showinfo("Éxito", message)
    else:
        messagebox.showerror("Error", message)

# Crear la ventana principal
root = tk.Tk()
root.title("PDF Splitter")
root.geometry("500x300")

# Etiqueta y entrada para el archivo PDF
label_input_path = tk.Label(root, text="Archivo PDF:")
label_input_path.pack(pady=10)
entry_input_path = tk.Entry(root, width=50)
entry_input_path.pack(pady=5)
btn_browse = tk.Button(root, text="Seleccionar PDF", command=select_pdf)
btn_browse.pack(pady=5)

# Campos para páginas de inicio y fin
label_start_page = tk.Label(root, text="Página de inicio:")
label_start_page.pack(pady=5)
entry_start_page = tk.Entry(root, width=10)
entry_start_page.pack(pady=5)

label_end_page = tk.Label(root, text="Página final:")
label_end_page.pack(pady=5)
entry_end_page = tk.Entry(root, width=10)
entry_end_page.pack(pady=5)

# Botón para dividir el PDF
btn_split = tk.Button(root, text="Dividir PDF", command=split_pdf_gui, bg="green", fg="white")
btn_split.pack(pady=20)

# Iniciar el bucle principal
root.mainloop()
