#Import Modules
from tkinter import *
from tkinter import scrolledtext
import json


#create root window 
root = Tk()

root.title("Query Creator")

root.geometry('625x300')


VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']



def firstFull(item):
    return item[:4]


def lastFull(item):
    return item[-4:]

def firstStripped(item):
    return item[:3]

def lastStripped(item):
    return item[-3:]

def stripVowels(item):

    newItem = list()

    for letter in item[1:-1]:
        if letter not in VOWELS:
            newItem += letter

    newItem.insert(0, item[0])
    newItem.append(item[-1])

    return "".join(newItem) 

def stripNoRepeat(newItem):

    noRepeat = list()


    #remove duplicate consinents
    for i in range(len(newItem) - 1):
        if newItem[i] != newItem[i + 1]:
            noRepeat += newItem[i]
    
    noRepeat += newItem[-1]

    return "".join(noRepeat)

#middle query for item names with vowels 
def getMiddleQuery_1(item):

    middle = item[(len(item)//2) - 2:(len(item)//2) + 2]

    return middle

#middle query for item names without vowels
def getMiddleQuery(item):

    middle = item[(len(item)//2) - 2:(len(item)//2) + 1]

    return middle

def clear():

    queries.delete(0, END)

def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def do_popup_1(event):
    try:
        m_1.tk_popup(event.x_root, event.y_root)
    finally:
        m_1.grab_release()

def paste():

    clipboard = root.clipboard_get()

    terms.insert('end', clipboard)

def copy():

    inp = terms.get()
    root.clipboard_clear()
    root.clipboard_append(inp)

def paste_1():

    clipboard = root.clipboard_get()

    queries.insert('end', clipboard)

def copy_1():

    inp = queries.get()
    root.clipboard_clear()
    root.clipboard_append(inp)


def createQueries():
    key = terms.get()

    list = key.split(",")
    queryList = []

    queries.delete(0, END)


    try:

        for item in list:

            item = item.strip()

            #One full inner query needed for items with 4 or 5 character length
            if (len(item) < 6 and len(item) > 3):
                queryList.append(firstFull(item))
                
                #Remove all vowels but the first and last
                stripedItem = stripVowels(item)

                #If vowels were striped and the striped item is more than 2 characters
                if(stripedItem != item and len(stripedItem) > 2):
                    queryList.append(stripedItem)

                noRepeatItem = stripNoRepeat(stripedItem)

                if(noRepeatItem[:3] != stripedItem[:3] and len(noRepeatItem) > 2):
                    queryList.append(firstStripped(noRepeatItem))

            #all items requiring 2 or more full inner queries 
            elif(len(item) > 5):

                #first 4 letter inner query
                queryList.append(firstFull(item))
                #last 4 letter inner query
                queryList.append(lastFull(item))

                #strip vowels from item name 
                strippedItem = stripVowels(item)

                #add stripped item name to query list
                if(len(strippedItem) < 6 and len(strippedItem) > 2):
                    if(len(strippedItem) > 3):
                        queryList.append(firstStripped(strippedItem))
                    else:
                        queryList.append(strippedItem)
                elif(len(strippedItem) > 5):
                    queryList.append(firstStripped(strippedItem))
                    queryList.append(lastStripped(strippedItem))

                #remove repeat consonants
                noRepeatItem = stripNoRepeat(strippedItem)

                #if no repeat consonant item is not the same as stripped item and greated than 2 letters add to query list
                if(noRepeatItem[:3] != strippedItem[:3] and len(noRepeatItem) > 2):
                    queryList.append(firstStripped(noRepeatItem))


                #get a middle query for items 7 or more letters long 
                if(len(item) > 6):

                    midQueries = getMiddleQuery_1(item)

                    queryList.append(midQueries)

                    #if the stripped item is longer than 8 letters and has stripped letters get a middle query 
                    if(len(strippedItem) > 7):
                        midQueriesStripped = getMiddleQuery(strippedItem)
                        if(midQueriesStripped != midQueries):
                            queryList.append(midQueriesStripped)   

            else:
                queryList.append(item)


        queries.insert(0, ",".join(queryList))

    except Exception:
        queries.insert("There was an issue in parsing the terms list")




#label for category key
lbl = Label(root, text = "Category/Product Terms: ")
lbl.grid(padx = 10, pady = 10)

#Entry for category key
terms = Entry(root, width = 100)
terms.bind('Control-v', lambda _:'break')
terms.bind('Control-c', lambda _:'break')
terms.bind('Control-x', lambda _:'break')
terms.bind('<Button-3>', do_popup)
terms.grid(row=1, padx = 10, pady = 10)

#clear button 
termBtn = Button(root, text = "Clear Query List", command = clear)
termBtn.grid(row=2, padx = 10, pady = 10)


#button to search for current category terms
termBtn = Button(root, text = "Create Inner Queries", command = createQueries)
termBtn.grid(row=3, padx = 10, pady = 30)


queries = Entry(root, width = 100)
queries.bind('Control-v', lambda _:'break')
queries.bind('Control-c', lambda _:'break')
queries.bind('Control-x', lambda _:'break')
queries.bind('<Button-3>', do_popup_1)
queries.grid(row=4, padx= 10, pady = 10)


m = Menu(root, tearoff = 0)
m.add_command(label = "Copy", command = copy)
m.add_command(label = "Paste", command = paste)

m_1 = Menu(root, tearoff = 0)
m_1.add_command(label = "Copy", command = copy_1)
m_1.add_command(label = "Paste", command = paste_1)



#loop the program
root.mainloop()