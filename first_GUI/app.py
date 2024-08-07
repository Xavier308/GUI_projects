import tkinter as tk

def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Ventana Sencilla")

    # Configurar el tamaño de la ventana
    root.geometry('300x200')  # Ancho x Alto

    # Crear un etiqueta (label)
    label = tk.Label(root, text="¡Hola, Tkinter!")
    label.pack(pady=20)  # Centrar y agregar padding vertical

    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()
