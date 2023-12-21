import tkinter as tk
import os

TITLE_FONT = ("Helvetica", 18, "bold")
font=("Arial",50,"bold")
data = os.listdir("/sys/class/net")

class Interface(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("1000x900")

        self.frames = {}
        for F in (StartPage, WifiPage,Monitoring, MonitoringRealise):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
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


        buttonCloseWindow = tk.Button(self,
                                      text='Close Window',
                                      height=3,
                                      width=25,
                                      command=self.close_window)
        buttonCloseWindow['font'] = TITLE_FONT
        buttonCloseWindow.place(relx=0.5, rely=0.65, anchor='center')


    def close_window(self):
        self.quit()
        self.destroy()

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
                           command=lambda: self.recuperation_interface())

        bouton.place(relx=0.5,rely=0.75,anchor='center')


    def recuperation_interface(self):
        global interface_selec

        self.interface = self.choix_wifi.selection_get()
        interface_selec = self.interface
        return self.controller.show_frame("Monitoring")

    def return_interface(self):
        return self.interface

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
                           command=self.quitter)

        button['font'] = TITLE_FONT
        button.place(relx=0.5, rely=0.4, anchor='center')

    def quitter(self):
        return self.controller.show_frame("MonitoringRealise")

class MonitoringRealise(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,
                         text="Passage en Mode Monitoring réalisé avec succés ",
                         font=("Arial",30,"bold"),
                         height=3)
        label.pack(side="bottom", fill="x", pady=300)

        carte=tk.Button(self,
                        text="Quitter",
                        height=3,
                        width=25,
                        command=lambda: self.quitter())
        carte['font'] = TITLE_FONT
        carte.place(relx=0.5, rely=0.75, anchor='center')

    def quitter(self):
        self.destroy()
        self.quit()