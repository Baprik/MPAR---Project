import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mdp


def init_grap(etats, liste_x,etat_actuel, save_file = False):
    G = nx.DiGraph(directed=True)
    G.add_nodes_from(etats)
    create_edges(G, etats, liste_x,etat_actuel, save_file)

def create_edges(G, etats, liste_x,etat_actuel,save_file):
    nodes_label = {}
    edge_label ={}
    nodes_inter = []
    current_state = etat_actuel
    
    for x in liste_x:
        create_edge(G, x, nodes_label, edge_label,nodes_inter)

    pos = nx.spectral_layout(G)
    # Tracé du graphe
    nx.draw_networkx_nodes(G, pos, nodelist=etats, node_shape='o', node_color='skyblue', node_size=300)
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_inter, node_shape='o', node_color='black', node_size=50)
    nx.draw_networkx_nodes(G, pos, nodelist=[current_state], node_shape='o', node_color='red', node_size=300)

    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', connectionstyle = 'arc3, rad = 0.1')
    print(G)
    print(nodes_inter)
    print(etats)
    #print()
    nx.draw_networkx_labels(G, pos, labels=nodes_label, font_size=10, font_color='black', font_weight='bold')

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_label)

    plt.title("")
    if save_file:
        plt.savefig('plot.png')
    else:
        plt.show()


    
        
def create_edge(G,x, nodes_label, edge_label,nodes_inter):
    if x[3]:#action présente 
        node_intermediare = x[0]+x[4]
        if node_intermediare not in G:
            G.add_node(node_intermediare)
            nodes_inter.append(node_intermediare)
            
            
        G.add_edge(x[0], node_intermediare)
        G.add_edge(node_intermediare, x[1])
        nodes_label[x[0]] = x[0]
        nodes_label[x[1]] = x[1]
        #nodes_label[node_intermediare] = node_intermediare

        edge_label[(x[0],node_intermediare)] = x[4]

        edge_label[(node_intermediare, x[1])] = x[2]
    else: 
        G.add_edge(x[0], x[1])
        nodes_label[x[0]] = x[0]
        nodes_label[x[1]] = x[1]
        edge_label[(x[0], x[1])] = x[2]



class MainWindow(tk.Toplevel):
    def __init__(self,printer : mdp.gramListener):
        super().__init__()
        self.printer = printer

        
        self.title("Application tkinter en trois parties")

        # Création des cadres pour chaque partie
        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(side="top", fill="both", expand=True)

        self.text_frame = ttk.Frame(self)
        self.text_frame.pack(side="top", fill="both", expand=True)

        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(side="top", fill="both", expand=True)

        # Partie pour afficher une image
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(padx=10, pady=10)

        self.current_image = None

        # Afficher l'image dans le Label
        
        self.show_image("plot.png")

        # Partie pour afficher du texte
        self.text_label = ttk.Label(self.text_frame, text="Si vous devez faire un choix, indiquer le (ex: 'a')\nSinon, presser directement 'Entrer' pour parcourir le graphe")
        self.text_label.pack(padx=10, pady=10)

        # Partie pour entrer du texte manuellement
        self.input_entry = ttk.Entry(self.input_frame, width=40)
        self.input_entry.pack(padx=10, pady=10)
        self.input_entry.bind("<Return>", self.on_enter_pressed)

    def show_image(self, file_path):
        try:
            # Charger l'image
            image = Image.open(file_path)
            # Redimensionner si nécessaire
            max_size = (1500, 1500)
            image.thumbnail(max_size, Image.ANTIALIAS)
            # Convertir l'image pour tkinter

            self.tk_image = ImageTk.PhotoImage(image)

            # Afficher l'image dans le Label
            self.image_label.config(image=self.tk_image)
        except Exception as e:
            print(f"Error loading image: {e}")


    def on_enter_pressed(self, event):
        choix = self.input_entry.get()
        choix_possible = self.printer.possible_choices(self.printer.current_state)
        if choix_possible == None: 
            new_text = "Presser 'Enter' pour continuer le parcours"
            print(new_text)
            self.text_label.config(text=new_text) 
            self.printer.current_state = self.printer.etat_suivant(self.printer.current_state,choix_possible)
            init_grap(self.printer.states, self.printer.trans, self.printer.current_state, save_file = True)
            self.show_image("plot.png")
            
            
        else :
            if choix not in set(choix_possible):
                new_text = "Ceci n'est pas un choix possible : " + str(choix) + "\nVoici la liste des choix possibles: " + str(set(choix_possible))
                print(new_text)
                self.text_label.config(text=new_text)
                self.input_entry.delete(0, tk.END)  # Efface le texte saisi
            else: 
            
                #parcours le graphe + on actu l'état courrant 
                self.printer.current_state = self.printer.etat_suivant(self.printer.current_state,choix)
                init_grap(self.printer.states, self.printer.trans, self.printer.current_state, save_file = True)
                self.show_image("plot.png")
            



def launch_interface(printer : mdp.gramPrintListener ):
    init_grap(printer.states, printer.trans, printer.current_state, save_file = True)
    app = MainWindow(printer)
    app.mainloop()

        
        
        
        
        
            
        
        
        