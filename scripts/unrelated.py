import tkinter as tk

alphabet = "abcdefghijklmnopqrstuvwxyz".strip()

def openDecypher():
    root = tk.Tk()
    root.geometry("250x300")
    root.config(bg="black")
    root.title("caesar shift")

    tk.Label(root,text="CEASAR SHIFT", bg="black", fg="white", font=("Helvetica", 20)).pack()
    tk.Label(root,text="encrypted \/", bg="black", fg="white").pack()

    encrypted = tk.Entry(root, bg="black", fg="white")
    encrypted.pack()

    tk.Label(root,text="decrypted \/", bg="black", fg="white").pack()

    decrypted = tk.Entry(root, bg="black", fg="white")
    decrypted.pack()

    tk.Button(root,text="DECRYPT", bg="black", fg="white", command=lambda:decrypted.insert(0, decrypt(encrypted.get(), shift))).pack()
    tk.Button(root,text="ENCRYPT", bg="black", fg="white", command=lambda:encrypted.insert(0, decrypt(decrypted.get(), shift))).pack()

    tk.Label(root,text="shift by (left)", bg="black", fg="white").pack()

    shift = tk.Entry(root, bg="black", fg="white")
    shift.pack()

    shift.insert(0, "1")

    root.mainloop()

def decrypt(encrypted, shift):

    shiftamount = int(shift.get())

    decrypted = ""

    for char in encrypted:
        if char in alphabet:
            index = alphabet.find(char)
            new_index = (index - shiftamount) % 26
            decrypted += alphabet[new_index]
        elif char == " ":
            decrypted += char

    return decrypted