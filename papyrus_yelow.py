import tkinter as tk

root = tk.Tk()
root.geometry("400x200")

label = tk.Label(
    root,
    text="Galben murdar",
    font=("Papyrus", 24),
    fg="#BEB41E",        # culoare text
    bg="#202020"         # fundal închis
)
label.pack(pady=40)

root.mainloop()