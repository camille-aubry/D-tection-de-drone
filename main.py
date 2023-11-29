#!/usr/bin/python3
# -*- coding: utf-8 -*


"""
    ##Projet SIE ##

    Version 1 fait en juin-septembre 2019
    Par Gendarmerie Nationnale, STSISI, SIRD

    main.py contenant le script principal, celui qui appelle les processus indépendants.

"""

# ## IMPORT ## #


# Importation des modules
import lib.sniff
import lib.json2

from lib.sh.sh import airmon_ng

# Librairies natives Python
import sys
import signal
import os

from multiprocessing import Process, Queue


# ## VARIABLE ## #



import subprocess

# Exécutez la commande pour passer en mode monitor sur votre interface WiFi

interface = "wlp0s20f3"
interface_wifi = "wlp0s20f3mon"  # Remplacez par le nom de votre interface


# ## FONCTIONS ## #

import subprocess


# Exemple d'utilisation :
# airmon_ng("start", "votre_interface_wifi", 6)  # Démarre le mode monitor sur le canal 6
# airmon_ng("stop", "votre_interface_wifi")      # Arrête le mode monitor

def monitorStart():
    """
        Fonction qui démarre le mode monitor.
    """
    
    print("Mode monitor de l'interface " + interface)


    try:

        airmon_ng("start", interface, 6)
        airmon_ng("check", "kill")
        subprocess.check_call(f"sudo ifconfig {interface_wifi} up", shell=True)
        print("Interface wlx00c0cab26e90 est maintenant en mode monitor.")

    except subprocess.CalledProcessError as e:
        #print("erreur ",e)
        if e == f"Requested device {interface}] does not exist.":
            print("Votre interface est déja en mode monitor")
        else:
            print(f"Erreur lors du passage en mode monitor : {e}")



def monitorStop():
    """
        Fonction qui stoppe le mode monitor et lance l'interface d'origine.
    """

    #airmon_ng("stop", "wlan0mon").exit_code == 0
    # En fonction de l'OS, permet de relancer les interfaces réseaux
    subprocess.check_call(f"sudo ifconfig {interface_wifi} down", shell=True)
    subprocess.check_call(f"sudo iwconfig {interface_wifi} mode Managed", shell=True)
    subprocess.check_call(f"sudo ifconfig {interface_wifi} up", shell=True)
    subprocess.check_call(f"sudo service network-manager restart", shell=True)



def signal_handler(signal, frame):
    """
        Fonction qui stoppe les workers dans l'ordre puis la fonction monitorStop.
    """

    # Arret des workers
    worker_sniffer.terminate()
    worker_json.terminate()
    
    print("\nArret du script.")
    #monitorStop()
    
    # Quitte le programme
    sys.exit(0)



#######################################################
#####             Programme principal             #####
#######################################################


# Début du script
print("Lancement du script.")
print("----------------------")

try:
    # lancement du monitor
    print("Lancement du mode monitor.")
    monitorStart()

except Exception as err:
    print("")
    print("------ ERREUR ---------")
    #print("erreur",err)

    print("impossible de passer en mode monitor " )

    if f"RAN: /usr/sbin/airmon-ng start {interface} 6" in str(err):
        print("Votre interface n'existe pas vérifier le nom ou est deja en mode monitor")

    print("Si vous souhaitez quitter le programme taper crt+C")

    print("----------------")

if __name__ == "__main__":
    """
        Ne se lance que si le script main.py est lancé directement ce qui évite l'import non voulu
        et surtout évite de lancer cette partie du code plusieurs fois. Cela génère des erreurs.
    """
    
    # 'mon' doit être rajouté car sur la plupart des OS linux l'interface en mode monitor prend 'mon' à la fin de son nom. 
    # à vérifier en fonction de l'interface et de l'OS.
    
    # Définitions des listes Queue servant pour l'échange de donnée entre les process
    queue_beacon_sie = Queue(maxsize=3000)


    # Définition des workers, les processus indépendant.
    worker_sniffer = Process(target=lib.sniff.sniffer,
                             args=(queue_beacon_sie, interface_wifi, ), name="sniffer")

    worker_json = Process(target=lib.json2.verif_and_construction_json,
                          args=(queue_beacon_sie, ), name="json")

    # Lancement des workers
    worker_sniffer.start()
    worker_json.start()
    print("En recherche de drone : ")

    # Arret des workers avec Ctrl + c
    signal.signal(signal.SIGINT, signal_handler)
