import re
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

def generar_automata(rfc):
    # Crear un grafo dirigido
    G = nx.DiGraph()
    
    estados = set()  # Conjunto para almacenar los estados utilizados

    # Agregar estado inicial
    estado_inicial = 'q0'
    G.add_node(estado_inicial)
    estados.add(estado_inicial)

    # Agregar transiciones
    estado_actual = estado_inicial
    for i, c in enumerate(rfc):
        nuevo_estado = 'q{}'.format(i+1)
        G.add_node(nuevo_estado)
        if c != '*' and c != '(' and c != ')':
            estados.add(nuevo_estado)
            G.add_edge(estado_actual, nuevo_estado, label=c)
            estado_actual = nuevo_estado

    # Visualizar el grafo
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, nodelist=estados, node_size=700)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    edge_labels = {(n1, n2): d['label'] for n1, n2, d in G.edges(data=True)}
    
    # Modificar los labels para eliminar los símbolos ()*
    cleaned_edge_labels = {}
    for key, value in edge_labels.items():
        cleaned_value = value.replace('(', '').replace(')', '').replace('*', '')
        cleaned_edge_labels[key] = cleaned_value
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=cleaned_edge_labels)
    plt.title("Automata valida: " + rfc)
    plt.axis('off')
    plt.show()

def validar_rfc(rfc):
    # Verificar si las letras son R, U, R y P (sin importar mayúsculas o minúsculas)
    return rfc.lower().startswith("m") and all(c.lower() in "mamc" for c in rfc)

def on_submit():
    rfc = entry.get()
    if validar_rfc(rfc):
        generar_automata(rfc)
    else:
        messagebox.showerror("Error", "Ingresa los primeros 4 dígitos de tu RFC ")

# Configuración de la interfaz gráfica
root = ThemedTk(theme="equilux")  # Puedes cambiar "equilux" por otros temas disponibles
root.title("Validación de RFC")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_input = ttk.Label(frame, text="Ingresa las letras de tu RFC :", font=("Helvetica", 12))
label_input.grid(row=0, column=0, pady=10)

entry = ttk.Entry(frame, width=30, font=("Helvetica", 12))
entry.grid(row=1, column=0, pady=10)

button_submit = ttk.Button(frame, text="Validar", command=on_submit)
button_submit.grid(row=2, column=0, pady=10)

root.mainloop()
