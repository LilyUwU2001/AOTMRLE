import tkinter as tk

def update_horizontal_counter(*args):
    # Aktualizuje wartość licznika na podstawie wartości poziomego scrollbara
    new_value = int(horizontal_scrollbar.get())
    horizontal_counter_var.set(new_value)

def update_vertical_counter(*args):
    # Aktualizuje wartość licznika na podstawie wartości pionowego scrollbara
    new_value = int(vertical_scrollbar.get())
    vertical_counter_var.set(new_value)

# Tworzenie głównego okna
root = tk.Tk()
root.title("Scrollbar - Poziomy i Pionowy")

# Zmienne przechowujące wartość liczników
horizontal_counter_var = tk.IntVar()
vertical_counter_var = tk.IntVar()

# Ustawienie początkowej wartości liczników na 0
horizontal_counter_var.set(0)
vertical_counter_var.set(0)

# Tworzenie etykiety z wartością poziomego licznika
horizontal_counter_label = tk.Label(root, textvariable=horizontal_counter_var, font=('Helvetica', 16))
horizontal_counter_label.pack(pady=10)

# Tworzenie poziomego scrollbara
horizontal_scrollbar = tk.Scale(root, from_=0, to=1000, orient=tk.HORIZONTAL, command=update_horizontal_counter)
horizontal_scrollbar.pack(fill=tk.X, padx=10)

# Ustawienie wartości początkowej poziomego scrollbara na 0
horizontal_scrollbar.set(0)

# Tworzenie etykiety z wartością pionowego licznika
vertical_counter_label = tk.Label(root, textvariable=vertical_counter_var, font=('Helvetica', 16))
vertical_counter_label.pack(padx=10)

# Tworzenie pionowego scrollbara
vertical_scrollbar = tk.Scale(root, from_=0, to=1000, orient=tk.VERTICAL, command=update_vertical_counter)
vertical_scrollbar.pack(fill=tk.Y)

# Ustawienie wartości początkowej pionowego scrollbara na 0
vertical_scrollbar.set(0)

# Uruchomienie pętli głównej
root.mainloop()
