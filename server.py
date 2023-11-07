import socket
import threading 
import sqlite3 
import json 
import tkinter as tk 
from datetime import datetime 

# Funkcija za kreiranje baze podataka i tabele automobili
def create_database_and_table():
    conn = sqlite3.connect('baza01.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS automobili (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        naziv TEXT NOT NULL,
                        cena REAL NOT NULL
                   )
                   ''')
    conn.commit()
    conn.close()

# Funkcija za rad sa bazom podataka
def insert_record(data):
    conn = sqlite3.connect('baza01.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO automobili (naziv, cena) VALUES (?, ?) ''', 
        (data['naziv'], data['cena'])
        )
    conn.commit()
    conn.close()
    return 'Novi automobil je dodat u bazu'

def read_records(data):
    conn = sqlite3.connect('baza01.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, naziv, cena FROM automobili WHERE id = ? OR naziv = ? OR cena = ?', 
                   (data.get('id', ''), data.get('naziv', ''), data.get('cena', ''))
                   )
    records = cursor.fetchall()
    conn.close()
    return records

def update_record(data):
    conn = sqlite3.connect('baza01.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE automobili SET cena = ? WHERE id = ? ''', 
        (data['cena'], data['id'])
    )
    conn.commit()
    conn.close()
    return 'Zapis je ažuriran.'

def delete_record(data):
    conn = sqlite3.connect('baza01.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM automobili WHERE naziv = ? ''', 
        (data['naziv'],)
        )
    conn.commit()
    conn.close()
    return 'Zapis je obrisan.'

# Funkcija koja obradjuje zahteve klijenta
def handle_client_request(client_socket, listbox):
    while client_socket:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            request_data = json.loads(request)
            action = request_data['action']
            data = request_data['data']

            if action == 'create_table':
                create_database_and_table()
                response = 'Tabela automobili je kreirana.'
            elif action == 'insert_record':
                response = insert_record(data)
            elif action == 'read_records':
                records = read_records(data)
                response = json.dumps(records)
            elif action == 'update_record':
                response = update_record(data)
            elif action == 'delete_record':
                response = delete_record(data)
            else:
                response = 'Nepoznata akcija.'

            client_socket.sendall(response.encode('utf-8'))
            listbox.insert(tk.END, f"Odgovor : {response}")

# Funkcija za pokretanje servera
def run_server(listbox):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen()
    listbox.insert(tk.END, "Server slusa dolazne transakcije...")

    while True:
        client_socket, addr = server_socket.accept()
        listbox.insert(tk.END, f"Povezan klijent: {addr}")
        threading.Thread(target=handle_client_request, args=(client_socket, listbox)).start()

# GUI Server
server_root = tk.Tk()
server_root.title()
server_root.geometry('100x800')
listbox_request = tk.Listbox(server_root)
listbox_request.pack(fill=tk.BOTH, expand=True)
server_thread = threading.Thread(target=run_server, args=(listbox_request,))
server_thread.daemon = True
server_thread.start()
server_root.mainloop()