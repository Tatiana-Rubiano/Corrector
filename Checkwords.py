from spellchecker import SpellChecker
from bs4 import BeautifulSoup
from string import ascii_lowercase
import requests
import pandas as pd
import numpy as np
from tkinter import *

spell = SpellChecker()
spell.word_frequency.load_text_file('./dicmine.dic')
ve = StringVar

def chars_filter(s, valid_chars):
    return "".join(c for c in s if c in valid_chars)


def main():

    raiz = Tk()
    raiz.title("URL")
    miFrame = Frame(raiz, width=300, height=300)
    miFrame.pack()

    def fun():
        ve = urlRec.get()
        miFrame.quit()
        return ve

        # labels

    peticion = Label(miFrame, text="Digite su URL")
    peticion.grid(row=0, column=0)
    # entry
    urlRec = Entry(miFrame)
    urlRec.grid(row=0, column=1)

    # Button
    send = Button(miFrame, text="Enviar", command=fun)
    send.grid(row=0, column=2)

    raiz.mainloop()

#LECTURA URL

    url_in = fun()
    print(url_in)
    source = requests.get(url_in).text
    soup = BeautifulSoup(source, "html.parser")
    root = soup.body

    for tag in root.find_all(["script", "style", "code", "pre"]):
        tag.decompose()

    text = root.get_text().replace("\n", " ").lower()
    text = chars_filter(text, ascii_lowercase + "áéíóúñü ")
    text = str(text)
    sep = ' '
    lista = text.split(sep)

    palabras= pd.DataFrame(lista,columns=["Palabras Revisadas"])
    palabras.replace('', np.nan, inplace=True)
    palabras.dropna(inplace=True)
    palabras.reset_index(inplace=True)
    print(palabras)
    palabras.to_csv('palabras.csv')


    misspelled = spell.unknown(lista)
    df = pd.DataFrame()
    for word in misspelled:
        inc = word
        co = spell.correction(word)
        sug = spell.candidates(word)
        tab = [co,inc]
        df = pd.DataFrame(np.array([tab]), columns=['CORRECTA', 'INCORRECTA']).append(df, ignore_index=True,sort=True)


    dicc = Tk()
    dicc.title("Palabras")
    frame2 = Frame(dicc, width=800, height=600)
    frame2.pack()

    new_word = StringVar

    def write():

        new_word = word.get()
        print(new_word)
        f = open('dicmine.dic', 'a')
        f.write('\n' + new_word)
        f.close()
        word.delete(0, END)

# labels

    let = Label(frame2, text="Agregar al diccionario")
    let.grid(row=1, column=0)
    # entry
    word = Entry(frame2)
    word.grid(row=1, column=1)

    # Button
    enviar = Button(frame2, text="Enviar", command=write).grid(row=1, column=2)

    palabras=Label(frame2,text=df,justify='left',anchor='center')
    palabras.grid(row=0, column=1)

    def out():
        dicc.quit()

    salir = Button(frame2, text="Salir", command=out).grid(row=2, column=1)

    dicc.mainloop()


if __name__ == "__main__":
     main()