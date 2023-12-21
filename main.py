#!/usr/bin/python3
# -*- coding: utf-8 -*


"""
    ##Projet SIE ##

    Version 1 fait en juin-septembre 2019
    Par Gendarmerie Nationnale, STSISI, SIRD

    main.py contenant le script principal, celui qui appelle les processus indépendants.

"""

# ## IMPORT ## #

# Librairies natives Python
import signal
import subprocess
import sys
from multiprocessing import Process, Queue
import Interfarce_graphique


# Importation des modules
import lib.json2
import lib.sniff

# ## VARIABLE ## #
#wlx00c0cab26e90

#Taper iwconfig pour connaitre le nom de votre interface wifi


# ## LES FONCTIONS ## #
def monitorStart():
    """
        Fonction qui démarre le mode monitor de votre interface graphique.
    """
    
    print("Passage en mode monitor de l'interface  " + interface)


    try:
        subprocess.check_call("sudo rfkill unblock all",shell=True)
        subprocess.check_call(f"sudo ifconfig {interface} down", shell=True)
        subprocess.check_call(f"sudo iwconfig {interface} mode monitor", shell=True)
        subprocess.check_call(f"sudo ifconfig {interface} up", shell=True)

       
        print("Interface ",interface,"est maintenant en mode monitor.")

    except subprocess.CalledProcessError as e:
        print("erreur")


def monitorStop():
    """
        Fonction qui stoppe le mode monitor et lance l'interface d'origine.
    """

    subprocess.check_call(f"sudo ifconfig {interface} down", shell=True)
    subprocess.check_call(f"sudo iwconfig {interface} mode Managed", shell=True)
    subprocess.check_call(f"sudo ifconfig {interface} up", shell=True)
    subprocess.check_call(f"sudo service network-manager restart", shell=True)



def signal_handler(signal, frame):
    """
        Fonction qui stoppe les workers dans l'ordre puis la fonction monitorStop.
    """

    # Arret des workers
    worker_sniffer.terminate()
    worker_json.terminate()
    
    print("\nArret du script.")
    monitorStop()
    
    # Quitte le programme
    sys.exit(0)

def ouverture_interface_graphique():
    app = Interfarce_graphique.Interface()
    Frame = app.returnFrame()
    app.mainloop()
    return app,Frame



#######################################################
#####             Programme principal             #####
#######################################################




# Début du script
print("Lancement du script.")
print("----------------------")

app,Frame =ouverture_interface_graphique()


FrameStart=Frame["StartPage"]
FrameWifi=Frame["WifiPage"]
FrameMonitoring=["Monitoring"]


interface=FrameWifi.return_interface()
app.destroy()
print(interface)





try:
    # lancement du monitor
    print("Lancement du mode monitor.")
    monitorStart()

except Exception as erreur:

    if f"RAN: /usr/sbin/airmon-ng start {interface} 6" in str(erreur):

        print("Votre interface n'existe pas vérifier le nom ou est deja en mode monitor")
        


    print("Si vous souhaitez quitter le programme taper crt+C")



if __name__ == "__main__":
    """
        Ne se lance que si le script main.py est lancé directement ce qui évite l'import non voulu
        et surtout évite de lancer cette partie du code plusieurs fois. Cela génère des erreurs.
    """

    # Définitions des listes Queue servant pour l'échange de donnée entre les process
    queue_beacon_sie = Queue(maxsize=3000)


    # Définition des workers, les processus indépendant.
    worker_sniffer = Process(target=lib.sniff.sniffer,
                             args=(queue_beacon_sie, interface ), name="sniffer")

    worker_json = Process(target=lib.json2.verif_and_construction_json,
                          args=(queue_beacon_sie, ), name="json")

    # Lancement des workers
    worker_sniffer.start()
    worker_json.start()
    print("----------------")
    print("En recherche de drone : ")

    # Arret des workers avec Ctrl + c
    signal.signal(signal.SIGINT, signal_handler)
