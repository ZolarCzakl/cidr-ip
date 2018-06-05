#!/usr/bin/env python3

"""
Conversion de notation CIDR en notation pointée et vice-versa.
Calcule également le nombre de sous-réseaux, d'adresses IP et d'hôte
disponibles.
Détermine la classe et la plage d'adresse attribuable.
Rod février 2018
"""

from tkinter import *
from tkinter import ttk


def from_cidr(cidr):
    """ Convertit la notation CIDR en notation pointée."""
    if cidr[0] == "/":
        cidr = cidr[1:]
    try:
        cidr = int(cidr)
        if cidr > 32 or cidr < 0:
            message.set(
                "\nEntrez un nombre entier de 0 à 32, avec ou sans '/'.\n")
            return('','','')
        else:
            oct_cidr = "1" * cidr + "0" * (32 - cidr)
            binaire.set(oct_cidr)
            oct1 = str(int(oct_cidr[:8], 2))
            oct2 = str(int(oct_cidr[8:16], 2))
            oct3 = str(int(oct_cidr[16:24], 2))
            oct4 = str(int(oct_cidr[24:], 2))
            masq = oct1 + "." + oct2 + "." + oct3 + "." + oct4
            nb_adr = ((256 - int(oct1))
                     *(256 - int(oct2))
                     *(256 - int(oct3))
                     *(256 - int(oct4)))
            message.set('\n\n')
            return(cidr, masq, nb_adr)            
    except ValueError:        
        message.set("\nEntrez un nombre entier de 0 à 32, avec ou sans '/'.\n")
        return('','','')

def from_masq(masq):
    """ Convertit la notation pointée en notation CIDR."""
    try:
        oct1, oct2, oct3, oct4 = masq.split(".")
        oct1 = str(bin(int(oct1)))[2:]
        oct2 = str(bin(int(oct2)))[2:]
        oct3 = str(bin(int(oct3)))[2:]
        oct4 = str(bin(int(oct4)))[2:]
        check_bin = oct1 + oct2 + oct3 + oct4
        binaire.set(check_bin)
        if "1" not in check_bin:
            cidr = "0"
            return(from_cidr(cidr))
        else:
            check_bin = check_bin.split("0")
            check = True
            for e in check_bin[1:]:
                if "1" in e:
                    check = False                    
                    message.set('\nmasque invalide\n')
                    return( "", "", "")
                    break
            if check:
                cidr = str(len(check_bin[0]))
                return(from_cidr(cidr))
    except ValueError:
        message.set('\n4 groupes de nombres entiers séparés par des points\n')
        return("", "", "")

def from_sr(sr):
    sous_res = {2 : "25", 4 : "26", 8 : "27", 16 : "28", 32 : "29",
                64 : "30", 128 : "31", 256: "32"}
    try:
        sr = int(sr)
        if sr == 1 or sr == 0:
            message.set('\nTous les masques de /0 à /24\n')
            return('')
        elif sr < 257:        
            while sr not in sous_res:            
                sr += 1            
            return(sous_res[sr])
        else:
            message.set('\npas de correspondance\n')
            return('')
    except ValueError:
        message.set('\nEntrez un nombre entier\n')
        return('')

def adr_host(cidr, nb_adr):
    """ Calcule le nombre de sous-réseaux, d'adresses IP
    et d'hôtes disponibles
    """
    try:
        if int(cidr) < 24:
            sr = "1"
            host = str(nb_adr - 2)
        elif int(cidr) < 31:
            sr = str(256//nb_adr)
            host = str(nb_adr - 2)
        elif int(cidr) == 31:
            sr, host = str(256//nb_adr), 2
        else:
            sr, host = str(256//nb_adr), 1
            
        adr = str(nb_adr)
        
        return(sr, adr, host)
    except ValueError:
        return("", "", "")

def find_class(cidr):
    try:
        if cidr < 16:
            return("A")
        elif cidr <24:
            return("B")
        else:
            return("C")
    except TypeError:
        return('')

def plage_ip(net_classe):
    classes = {'A' : ('0.0.0.0', '127.255.255.255'),
               'B' : ('128.0.0.0', '191.255.255.255'),
               'C' : ('192.0.0.0', '223.255.255.255'),
               'D' : ('224.0.0.0', '239.255.255.255'),
               'E' : ('240.0.0.0', '255.255.255.255')}
    if net_classe in classes:        
        return(classes[net_classe])
    else:
        return('', '')

def go(event=None):
    """ Enregistre les données entrées."""
    cidr = ent_cidr.get()
    masq = ent_masq.get()
    sr = ent_sr.get()
    if cidr:
        cidr, masq, nb_adr = from_cidr(cidr)
        sr, adr, host = adr_host(cidr, nb_adr)
        net_classe = find_class(cidr)
    elif masq:
        cidr, masq, nb_adr = from_masq(masq)
        sr, adr, host = adr_host(cidr, nb_adr)
        net_classe = find_class(cidr)
    elif sr:
        cidr = from_sr(sr)
        if cidr:
            cidr, masq, nb_adr = from_cidr(cidr)
            sr, adr, host = adr_host(cidr, nb_adr)
            net_classe = find_class(cidr)
        else:
            net_classe, adr, host = '','',''   
    ip_from, ip_to = plage_ip(net_classe)
    reset()
    ent_cidr.insert(0, str(cidr))
    ent_masq.insert(0, str(masq))
    ent_sr.insert(0, sr)
    addr.set(adr)
    hos.set(host)
    classe.set(net_classe)
    ip1.set(ip_from)
    ip2.set(ip_to)

def reset(envent=None):
    """Vide les champs d'entrée."""
    ent_cidr.delete(0, END)
    ent_masq.delete(0, END)
    ent_sr.delete(0, END)

root = Tk()
root.title("CIDR <->")
root.resizable(0,0)

message = StringVar()
message.set('\nCliquez dans la fenêtre de votre choix et entrez une valeur.\n')
ip1 = StringVar()
ip2 = StringVar()
classe = StringVar()
addr = StringVar()
hos = StringVar()
binaire = StringVar()

Label(root, textvariable=message).grid(row=0, rowspan=2, columnspan=3)
Label(root, text="        CIDR         ", bg='grey').grid(row=2)
Label(root, text="      Classique      ", bg='grey').grid(row=2, column=1)
Label(root, text="   Nb sous-réseaux   ", bg='grey').grid(row=2, column=2)
ent_cidr = Entry(root)
ent_cidr.grid(row=3, column=0)
ent_masq = Entry(root)
ent_masq.grid(row=3, column=1)
ent_sr = Entry(root)
ent_sr.grid(row=3, column=2)

Label(root, textvariable=binaire).grid(row=4,columnspan=3)
Label(root, text="        Classe       ", bg='grey').grid(row=5)
Label(root, text="     Nb adresses     ", bg='grey').grid(row=5, column=1)
Label(root, text="      Nb hôtes       ", bg='grey').grid(row=5, column=2)
Label(root, textvariable=classe).grid(row=6)
Label(root, textvariable=addr).grid(row=6, column=1)
Label(root, textvariable=hos).grid(row=6, column=2)
Label(root, text="  de        ", bg='grey').grid(row=7, column=1, sticky='W')
Label(root, text="  à         ", bg='grey').grid(row=7, column=2, sticky='W')
Label(root, textvariable=ip1).grid(row=8, column=1)
Label(root, textvariable=ip2).grid(row=8, column=2)



Button(root, text="Go!", command=go, bg='grey').grid(row=9)
Button(root, text="Reset", command=reset, bg='grey').grid(row=9, column=2)

root.bind('<Return>', go)
ent_cidr.bind('<Button-1>', reset)
ent_masq.bind('<Button-1>', reset)
ent_sr.bind('<Button-1>', reset)

root.mainloop()
