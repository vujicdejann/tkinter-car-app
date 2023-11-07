import tkinter as tk
from threading import Thread
import socket
import json

# Globalne promenljive za komunikaciju
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Povezivanje na server
try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
except ConnectionRefusedError:
    print("Server nije dostupan.")


# Header funkcionalnosti: horizontalni scroll poruke
def scroll_message(header_label):
    message = "Dobrodošli u sistem za upravljanje bazom automobila"
    while True:
        header_label.config(text=message)
        message =  message[1:] + message[0]
        header_label.after(100)

# Funkcije za rad sa abzom podataka
def create_table():
    send_request_to_server("create_table")

def insert_record():
    data = {
        'naziv' : entry_naziv.get(),
        'cena'  : float(entry_cena.get())
    }
    send_request_to_server("insert_record", data)

def read_records():
    data = {
        'id'    : entry_id.get(),
        'naziv' : entry_naziv.get(),
        'cena'  : entry_cena.get()
    }
    send_request_to_server("read_records", data)

def update_record():
    data = {
        'id'   : entry_id.get(),
        'cena' : float(entry_cena.get())
    }
    send_request_to_server("update_record", data)

def delete_record():
    data = {
        'naziv' : entry_naziv.get()
    }
    send_request_to_server("delete_record", data)

# Slanje zahteva serveru
def send_request_to_server(action, data=None):
    request = {'action' : action, 'data' : data}
    client_socket.sendall(json.dumps(request).encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    listbox_responses.insert(tk.END, response)


# GUI
root = tk.Tk()
root.title()
root.geometry('800x800')

# Header GUI
header = tk.Frame(root, width=800, height=50)
header_label = tk.Label(header, text='', width=800)
header_label.pack()
header.pack(side=tk.TOP, fill=tk.X)
thread = Thread(target=scroll_message, args=(header_label,))
thread.daemon = True
thread.start()

# Body GUI
body = tk.Frame(root, width=800, height=700)

# Elementi za unos
entry_id = tk.Entry(body)
entry_id.pack()

entry_naziv = tk.Entry(body)
entry_naziv.pack()

entry_cena = tk.Entry(body)
entry_cena.pack()

# Dugmad za akcije
button_create_table = tk.Button(body, text='Kreiraj tabelu', command=create_table)
button_create_table.pack()

button_insert_record = tk.Button(body, text='Unesi zapis', command=insert_record)
button_insert_record.pack()

button_read_records =  tk.Button(body, text='Citaj zapise', command=read_records)
button_read_records.pack()

button_delete_record = tk.Button(body, text='Obrisi zapis', command=delete_record)
button_delete_record.pack()

# Lista za odgovore servera
listbox_responses = tk.Listbox(body)
listbox_responses.pack()
body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Footer GUI
footer = tk.Frame(root, width=800, height=50)
footer_label = tk.Label(footer, text='©2022 Andrijana Perduh BROJ INDEKSA', width=800)
footer_label.pack()
footer.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()


