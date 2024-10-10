import requests as rq
import json
import tkinter as tk
import random
import PIL.Image
import PIL.ImageTk

request = rq.get("http://pokeapi.co/api/v2/pokemon/?limit=1302")
pokemons = request.json()
gui = tk.Tk()
gui.minsize(400, 0)
gui.title("Who's That Pokemon?")
score = 0
roundCount = 0
limit = 5
usedpokemon = []

#Get a random pokemon
def GetPokemon():
    while True:
        randy = random.randint(0, 1301)
        request2 = rq.get(pokemons["results"][randy]["url"])
        if request2 not in usedpokemon:
            usedpokemon.append(request2)
            pokemon = request2.json()
            while True:
                if "-" in pokemon["name"]:
                    randy = random.randint(0, 1301)
                    request2 = rq.get(pokemons["results"][randy]["url"])
                    pokemon = request2.json()
                else:
                    break
            return pokemon

#Get the Types of the pokemon
def GetTypes(pokemon):
    types = []
    x = 0
    for each in pokemon["types"]:
        types.append(each["type"]["name"])
        x += 1
    return types


#Get the flavor text of the pokemon    
def GetFlavorText(pokemon):
    request3 = rq.get(pokemon["species"]["url"])
    species = request3.json()
    en = []
    x = 0
    for each in species["flavor_text_entries"]:
        if each["language"]["name"] == "en":
            en.append(each["flavor_text"])
    string = str(en[0])
    name = str(pokemon["name"])
    string = string.replace("\n", " ")
    string = string.replace("\f", " ")
    string = string.replace(name.upper(), "(This Pokemon)")
    string = string.replace(name.lower(), "(This Pokemon)")
    string = string.replace(name.capitalize(), "(This Pokemon)")
    string = string.replace("POKéMON", "pokemon")
    return string

#Get a wrong option for the quiz. Returns a pokemon name other than the one in the arguement
def GetOption(pokemon):
    pk = GetPokemon()
    while True:
        if pk["name"] == pokemon["name"]:
            pk = GetPokemon(pokemon)
        else:
            return pk["name"].capitalize()

#Get rid of everything
def Nuke():
    for each in gui.winfo_children():
        each.destroy()

#Displays the type of the mystery pokemon as a hint in exchange for a point
def DisplayTypeHint(pokemon):
    global score 
    score -= 1
    types = GetTypes(pokemon)
    tk.Message(gui, text=types, width=300).pack()
    hintButton.forget()

def DisplaySpriteHint(pokemon):
    global score
    score -= 6
    url = pokemon["sprites"]["front_default"]
    img_request = rq.get(url)
    data = img_request.content
    file = open("image.png", "wb")
    file.write(data)
    file.close()

    img = PIL.Image.open("image.png")
    img = PIL.ImageTk.PhotoImage(img)
    img.image = img

    label = tk.Label(gui, image=img)
    label.pack()
    hintButton2.forget()



#Message to display when the correct option is clicked
def CorrectMessage(isExtra):
    global score
    if isExtra == True:
        score += 5
    
    score += 10
    rightAnswer.forget()

    tk.Message(gui, text="Correct!", width=300).pack()
    tk.Button(gui, text="Continue", command=lambda: NewRound(False)).pack()
    if roundCount < (limit - 1):
        tk.Button(gui, text="Make the next question a hard one (+ 5 potential points)", command=lambda: NewRound(True)).pack()
    
#Message to display when a wrong option is clicked
def IncorrectMessage(button):
    global score
    score -= 2
    tk.Message(gui, text="Not quite", width=300).pack()
    button.forget()

#Method to start the game
def StartRound(isExtra):
    #The pokemon to guess
    poke = GetPokemon()
    tk.Label(gui, text="Score: "+str(score)).pack()
    tk.Label(gui, text="Round: "+str(roundCount+1)).pack()
    tk.Message(gui, text=GetFlavorText(poke)).pack()
    buttons = []
    global rightAnswer
    wrong1 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong1))
    wrong2 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong2))
    wrong3 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong3))
    wrong4 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong4))
    wrong5 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong5))
    wrong6 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong6))
    wrong7 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong7))
    wrong8 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong8))
    wrong9 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong9))
    wrong10 = tk.Button(gui, text=GetOption(poke), command=lambda: IncorrectMessage(wrong10))
    rightAnswer = tk.Button(gui, text=poke["name"].capitalize(), command=lambda: CorrectMessage(isExtra))
    buttons.append(rightAnswer)
    buttons.append(wrong1)
    buttons.append(wrong2)
    buttons.append(wrong3)
    buttons.append(wrong4)
    buttons.append(wrong5)
    buttons.append(wrong6)
    if isExtra == True:
        buttons.append(wrong7)
        buttons.append(wrong8)
        buttons.append(wrong9)
        buttons.append(wrong10)
    global hintButton
    global hintButton2
    hintButton = tk.Button(gui, text="Display the types of the pokemon (- 1 point)", command= lambda: DisplayTypeHint(poke))
    hintButton2 = tk.Button(gui, text="Display pokemon sprite (- 6 points)", command=lambda: DisplaySpriteHint(poke))
    hintButton.pack(pady = (0, 10))
    hintButton2.pack(pady = (0, 15))
    random.shuffle(buttons)
    for each in buttons:
        each.pack(pady = (5, 5))

#Starts a new round if the round count has not exceeded the limit
def NewRound(isExtra):
    global roundCount
    roundCount += 1
   
    if roundCount < limit:
        Nuke()
        global score
        StartRound(isExtra)
    else:
        Nuke()
        tk.Message(gui, text="Game Over").pack()
        tk.Message(gui, text="Final Score: "+str(score)).pack()

    

StartRound(False)
tk.mainloop()