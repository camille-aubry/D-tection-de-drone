import tkinter as tk  # python3
import os
import tkintermapview

from PIL import Image,ImageTk

import test

# import Tkinter as tk   # python

TITLE_FONT = ("Helvetica", 18, "bold")
font=("Arial",50,"bold")
data = os.listdir("/sys/class/net")


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("1000x900")

        self.frames = {}
        for F in (StartPage, WifiPage, CartePage,Monitoring):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''

        frame = self.frames[page_name]
        frame.tkraise()

    def returnFrame(self):
        return self.frames
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="DÉTECTION DE DRONE", font=font)
        label.pack(side="top", fill="x", pady=100)

        button1 = tk.Button(self,
                            text="Wifi Mode Monitoring",
                            height=3,
                            width=25,
                            command=lambda: controller.show_frame("WifiPage"))
        button1['font']=TITLE_FONT
        button1.place(relx=0.5,rely=0.35,anchor='center')

        button2 = tk.Button(self,
                            text="Carte Drone",
                            height=3,
                            width=25,
                            command=lambda: controller.show_frame("CartePage"))
        button2['font'] = TITLE_FONT
        button2.place(relx=0.5, rely=0.5, anchor='center')

        buttonCloseWindow = tk.Button(self,
                                      text='Close Window',
                                      height=3,
                                      width=25,
                                      command=self.close_window)
        buttonCloseWindow['font'] = TITLE_FONT
        buttonCloseWindow.place(relx=0.5, rely=0.65, anchor='center')




    def close_window(self):
        quitter()

class WifiPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,
                         text="Choix de votre interface Wifi :",
                         font=font,
                         height=5)
        label.pack(side="top", fill="x", pady=0)

        self.choix_wifi = tk.Listbox(self,
                                     width=20,
                                     height=len(data),
                                     font="Verdana 40 bold",
                                     selectbackground="blue", )

        self.choix_wifi.place(relx=0.5,rely=0.5,anchor='center')

        for index, element in enumerate(data):
            self.choix_wifi.insert(index, element)

        bouton = tk.Button(self,
                           text="Valider",
                           height=3,
                           width=25,
                           font=TITLE_FONT,
                           command=lambda: [self.recuperation_interface(),controller.show_frame("Monitoring")])

        bouton.place(relx=0.5,rely=0.75,anchor='center')


    def recuperation_interface(self):
        global interface_selec

        self.interface = self.choix_wifi.selection_get()
        interface_selec = self.interface

class CartePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.liste_markeur=[]


        label = tk.Label(self,
                         text="Carte Drone",
                         font=font)
        label.pack(side="top", fill="x", pady=10)

        self.map_widget = tkintermapview.TkinterMapView(self,
                                                        width=1000,
                                                        height=650,
                                                        corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.map_widget.set_position(49.356795, 1.17459)
        self.map_widget.set_zoom(17)


        button = tk.Button(self,
                           text="Accueil",
                           height=2,
                           width=15,
                           font=TITLE_FONT,
                           command=lambda: controller.show_frame("StartPage"))
        button.place(relx=0.1, rely=0.15, anchor='n')


    def ajout_markeur(self,latitude,longitude,drone):
        markeur = self.map_widget.set_marker(latitude,
                                             longitude,
                                             text=f"DRONE{drone}")
        self.liste_markeur.append(markeur)
        self.update()

class Monitoring(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,
                         text="Passage en Mode Monitoring de l'interface ",
                         font=("Arial",30,"bold"),
                         height=3)
        label.pack(side="top", fill="x", pady=5)


        button = tk.Button(self,
                           text="Valider",
                            height=3,
                            width=25,
                           command=self.close_window)

        button['font'] = TITLE_FONT
        button.place(relx=0.5, rely=0.4, anchor='center')

    def close_window(self):
        test.lancement_recherche_drone(interface_selec)
        self.update()

        label = tk.Label(self,
                         text="Passage en Mode Monitoring réalisé avec succés ",
                         font=("Arial",30,"bold"),
                         height=3)
        label.pack(side="bottom", fill="x", pady=300)

        carte=tk.Button(self,
                        text="Voir le carte",
                        height=3,
                        width=25,
                        command=lambda: [self.controller.show_frame("CartePage"), self.mainloop()])
        carte['font'] = TITLE_FONT
        carte.place(relx=0.5, rely=0.75, anchor='center')







interface_selec=""


def ouverture():
    app = SampleApp()
    Frame = app.returnFrame()
    app.mainloop()
    return app,Frame


def quitter(app):
    app.destroy()

def ajout_markeur_autre(app,map,Latitude,Longiture,drone):
    app.mainloop()
    map.ajout_markeur(Latitude,Longiture,drone)