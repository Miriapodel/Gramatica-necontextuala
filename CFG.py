#In Rules, variabilele sunt de tipul ,VARIABILA,
#In Rules, tranzitia este marcat prin ->

import random


def citire_fisier(nume_fisier):
    # Adaug toate datele din fisier intr-o variabila

    fisier = []
    try:
        with open(nume_fisier) as f:
            for linie in f:
                fisier.append(linie)

        return fisier

    # Tratez cazul in care fisierul nu exista si trimit o eroare

    except:
        print("Fisierul nu exista")
        return None


def file_parser(fisier):
    structura_fisier = {}  # Memorez structura fisierului intr un dictionar
    sectiune_curenta = ''

    for linie in fisier:
        if linie[0] == '[' and linie[-2] == ']':  # Verific daca linia curenta anunta inceputul unei noi sectiuni

            # Populez dictionarul in stilul structurii fisierului. Fiecare sectiune este o cheie ale carei valori sunt
            # datele care se afla in sectunea respectiva

            nume_sectiune = linie.rstrip('\n').strip(']').lstrip('[')
            sectiune_curenta = nume_sectiune
            if nume_sectiune not in structura_fisier:  # Sectiunea curenta este folosita ca o cheie
                if nume_sectiune == 'Rules':
                    structura_fisier[
                        nume_sectiune] = {}  # Daca sectiunea curenta este 'Actions' elementele care urmeaza sa fie citite vor fi stocate tot intr un dictionar
                else:
                    structura_fisier[
                        nume_sectiune] = []  # Daca sectiunea curenta nu este 'Actions' elementele care urmeaza sa fie citite vor fi stocate intr o lista
        else:
            if (linie[0] != '#' and sectiune_curenta != '') or (linie[0] == '#' and len(
                    linie) == 2 and sectiune_curenta != ''):  # Verific daca linia curenta este un comentariu, iar in caz afirmativ o ignor
                data = linie.rstrip('\n')

                if sectiune_curenta == 'Rules':
                    if "->" not in data:
                        print("Sectiunea Rules nu este definita corect")
                        return False
                    data = data.split("->")  # Impart linia curenta in parti componente

                    if data[0] not in structura_fisier[sectiune_curenta]:
                        structura_fisier[sectiune_curenta][data[
                            0]] = []  # Daca elementul nu a fost adaugat deja in actions, il adaucam ca cheie si creem un dictonar pentru valorile lui

                    structura_fisier[sectiune_curenta][data[0]].append(
                        data[1])  # Adaugam starile in care se duce starea curenta in lista

                else:
                    structura_fisier[sectiune_curenta].append(data)

    return structura_fisier


def verificare_corectitudine_sigma(structura):
    if 'Sigma' not in structura: # Verific daca s a citit sectiunea Sigma
        print("Nu exista simboluir")
        return False

    elif len(structura['Sigma']) == 0:  # Verific daca sectiunea este goala
        print("Sectiunea Sigma este goala")
        return False

    else:

        if sorted(structura['Sigma']) != sorted(
                list(set(structura['Sigma']))):  # Verific unicitatea elementelor din limbaj
            print("Multimea de simboluri nu are elemente unice")
            return False

        for element in structura['Sigma']: # Verific daca simbolurile si variabilele au aceleasi notatii
            if element in structura['Vars']:
                print("Unele simboluri sunt aceleasi ca unele variabile")
                return False

    return True


def verificare_corectitudine_vars(structura):
    litere = [0 for i in range(26)]

    if 'Vars' not in structura:
        print("Nu exista States")
        return False

    elif len(structura['Vars']) == 0:  # Verific daca sectiunea States este sau nu goala
        print("Sectiunea Vars este goala")
        return False

    else:
        if sorted(structura['Vars']) != sorted(
                list(set(structura['Vars']))):  # Verific unicitatea elementelor din limbaj
            print("Multimea de variabile nu are elemente unice")
            return False

        for element in structura['Vars']: # Verific daca fiecare variabila incepe cu litera mare
            if element[0] != element[0].upper():
                print("Variabilele nu incep cu litera mare")
                return False

    return True


def verificare_corectitudine_rules(structura):
    if 'Rules' not in structura:  # Verific daca exista Actions ca sectiune in fisierul de configuratie
        print("Nu exista sectiunea Rules")
        return False

    elif len(structura['Rules']) == 0:  # Verific daca functia de tranzitie e goala sau nu
        print("Sectiunea Rules este goala")
        return False

    # Verific daca datele din actions sunt corecte, mai exact daca cele trei elemente trimise pe cate o linie apartin sectiunii
    # States ( primul element si al treilea ) si sectiunii Sigma ( elementul din mijloc )

    for element in structura['Rules']:
        if element not in structura['Vars']:
            print("Substitutia nu este facuta pentru o variabila")
            return False
        for substitutie in structura['Rules'][element]:
            substitutie = substitutie.split(",")
            for caracter in substitutie:
                if caracter not in structura['Vars'] and caracter not in structura['Sigma'] and caracter != '':
                    return False

    return True

    # Verific daca functia pentru tranzitii contine elemente corecte


def verificare_corectitudine_fisier(structura):
    corect_Sigma = verificare_corectitudine_sigma(structura)

    if corect_Sigma is False:
        return False

    corect_vars = verificare_corectitudine_vars(structura)

    if corect_vars is False:
        return False

    corect_rules = verificare_corectitudine_rules(structura)

    if corect_rules is False:
        return False

    return True


def exista_variabila(string):
    for char in string: # Daca string pe care il citim nu are litere mari inseamna ca nu e variabila
        if ord('A') <= ord(char) <= ord('Z'):
            return 1

    return 0


def generare(structura):
    rezultat = structura['Rules'][structura['Vars'][0]][0]

    while exista_variabila(rezultat):
        schimbare = 0
        substitutie = '' # Aici se va retine noul string dupa fiecare substitutie

        rezultat = rezultat.split(",")

        for char in rezultat:
            if char != '':
                if ord(char[0]) < ord('A') or ord(char[0]) > ord('Z'): # Verific daca elementul  nu e o variabila
                    substitutie += char # In caz afirmativ, il las asa cum e, fara sa fac o substitutie
                else:
                    if ord('A') <= ord(char[0]) <= ord('Z'): # Cazul in care elementul este o variabila
                        if schimbare == 0: # Trebuie sa fac substitutie
                            schimbare = 1

                            newchar = structura['Rules'][char][random.randint(0, len(structura['Rules'][char]) - 1)] #Aleg la intamplare un element nou din cele posibile
                            substitutie += newchar # Adaug elementul ales la intamplare
                        else:
                            if ord('A') <= ord(char[0]) <= ord('Z'):
                                char = ',' + char + ','

                            substitutie += char

        rezultat = substitutie

        if len(rezultat) > 100: # Limita maxima pe care poate sa o aiba un rezultat. In cazul in care acesta depaseste limita, se inlocuiesc toate variabilele care mai sunt de inlocuit cu terminali si se opreste generarea
            substitutie = ''
            rezultat = rezultat.split(",")

            # Substitutia se realizeaza ca la pasul anterior

            for char in rezultat:
                if char != '':
                    if ord(char[0]) < ord('A') or ord(char[0]) > ord('Z'):
                        substitutie += char
                    else:
                        if ord('A') <= ord(char[0]) <= ord('Z'):
                            newchar = ''

                            for elem in structura['Rules'][char]:
                                if exista_variabila(elem) == 0:
                                    newchar = elem
                                    break

                            substitutie += newchar

            rezultat = substitutie
            break

    return rezultat


def start_app():
    nume_fisier = "config2.in"  # Citesc numele fisierului in care se afla configuratia
    date_fisier = citire_fisier(nume_fisier)  # Colectez toate informatiile din fisier in aceasta variabila

    if date_fisier is not None:
        structura_fisier = file_parser(date_fisier)  # Structurez informatiile pe sectiuni intr un dictionar

        if structura_fisier is not False:


            if verificare_corectitudine_fisier(structura_fisier): # Daca fisierul contine date corecte incep generarea
                for i in range(10):
                    print(generare(structura_fisier))



start_app()