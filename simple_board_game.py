import random
from tkinter import *
import os


class Player:
    def __init__(self):
        self.name = ""
        self.position = 0

    def getName(self):
        return self.name

    def getPosition(self):
        return self.position

    def setName(self, n):
        self.name = n

    def setPosition(self, p):
        self.position = p


        
class Dice:
    def __init__(self):
        self.point = 0

    def roll(self):
        self.point = int(random.random() * 6 + 1)
        return self.point



class Game:
    def __init__(self):
        self.P1 = Player()
        self.P2 = Player()
        self.dice = Dice()
        
        self.gui = Tk()
        self.gui.geometry('400x400')
        self.gui.title("A simple board game")

        self.playerFrame = Frame(self.gui)

        self.player1Frame = Frame(self.playerFrame)
        self.player2Frame = Frame(self.playerFrame)

        self.l1 = Label(self.player1Frame)
        self.l2 = Label(self.player2Frame)
        
        self.e1 = StringVar()
        self.name1 = Entry(self.player1Frame, textvariable = self.e1)
        
        self.e2 = StringVar()
        self.name2 = Entry(self.player2Frame, textvariable = self.e2)

        self.l1.pack()
        self.name1.pack_forget()

        self.player1Frame.pack(anchor = 'nw')

        self.l2.pack()
        self.name2.pack_forget()

        self.player2Frame.pack(anchor = 'nw')

        self.okButton = Button(self.playerFrame, text = "OK", command = self.savePlayer)
        self.okButton.pack_forget()
        self.playerFrame.pack()

        self.msg = StringVar()
        self.msg.set("""Welcome to the simple board game!
Go to Menu to start a new game.""")
        self.msgLabel = Label(self.gui, textvariable = self.msg, wraplength = 380, justify='left')

        self.buttonFrame = Frame(self.gui)

        self.menu = Menu(self.gui)

        self.fileMenu = Menu(self.menu, tearoff = 0)
        self.fileMenu.add_command(label = "Start a new game", command = self.gameInit)
        self.fileMenu.add_command(label = "Display player positions", command = self.getPosition)
        self.menu.add_cascade(label = "Menu", menu = self.fileMenu)

        self.helpMenu = Menu(self.menu, tearoff = 0)
        self.helpMenu.add_command(label = "Display game help", command = self.gameHelp)
        self.helpMenu.add_command(label = "Exit", command = exit)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label = "About", command = self.about)
        self.menu.add_cascade(label = "Help", menu = self.helpMenu)
        
        
        self.playButton = Button(self.buttonFrame, text = "Play a round", command = self.oneRound)
        self.playButton.pack_forget()

        self.buttonFrame.pack()
        self.msgLabel.pack()

        self.gui.config(menu = self.menu)
        
        self.gui.mainloop()
        

    def gameInit(self):
        self.playButton.pack_forget()
        self.msg.set("")
        self.e1.set("")
        self.e2.set("")
        self.l1.config(text = "Name of first player: ")
        self.l2.config(text = "Name of second player: ")
        self.name1.pack()
        self.name2.pack()
        self.okButton.pack()

    def savePlayer(self):
        if self.nameValidate():
            nameP1 = self.e1.get()
            nameP2 = self.e2.get()
            self.P1.setName(nameP1)
            self.P2.setName(nameP2)
            self.P1.setPosition(0)
            self.P2.setPosition(0)
            self.msg.set("Player saved!")
            self.okButton.forget()
            self.playButton.pack()
        else:
            self.msg.set("Please set a valid name!")

    def nameValidate(self):
        name1 = self.e1.get()
        name2 = self.e2.get()
        if name1.strip(" ") == "" or name2.strip(" ") == "":
            return False
        if name1 == name2:
            return False
        else:
            return True
        

    def oneRound(self):
        self.l1.config(text = "Player " + self.P1.getName())
        self.l2.config(text = "Player " + self.P2.getName())
        move1 = self.dice.roll()
        move2 = self.dice.roll()
        
        lp1 = self.P1.getPosition()
        lp2 = self.P2.getPosition()
        
        if lp1 < 50 and lp2 < 50:
            self.e1.set(" rolled: " + str(move1))
            self.e2.set(" rolled: " + str(move2))
            p1 = move1 + lp1
            p2 = move2 + lp2
            sp1 = str(p1)
            sp2 = str(p2)
            if p1 % 11 == 0:
                p1 = p1 - 5
                sp1 = str(p1) + " (penalty)"
            if p2 % 11 == 0:
                p2 = p2 - 5
                sp2 = str(p2) + " (penalty)"
            moveMsg1 = self.P1.getName() + " rolled a " + str(move1) + ", and moves from position " + str(lp1) + " to " + sp1
            moveMsg2 = self.P2.getName() + " rolled a " + str(move2) + ", and moves from position " + str(lp2) + " to " + sp2
            self.P1.setPosition(p1)
            self.P2.setPosition(p2)
            self.msg.set(moveMsg1 + '\n' + moveMsg2)
            
            winner = self.checkWinner()
            if winner:
                winnerMsg = "** Congratulations, this game was won by:" + winner + " **"
                self.msg.set(moveMsg1 + '\n' + moveMsg2 + '\n' + winnerMsg)
        else:
            self.displayWinner()
        self.msgLabel.pack()

            
    def checkWinner(self):
        wp = ""
        if self.P1.getPosition() >= 50:
            wp = wp + " " + self.P1.getName()
        if self.P2.getPosition() >= 50:
            wp = wp + " " + self.P2.getName()
        return wp


    def displayWinner(self):
        winner = self.checkWinner()
        if winner:
            displayMsg = "Game finished!" + '\n' + "Go to Menu to start a new game." + '\n'+ "Last game was won by:" + winner
            self.msg.set(displayMsg)
            
        
    def getPosition(self):
        if self.P2.getName():
            self.l1.config(text = "Player " + self.P1.getName())
            self.l2.config(text = "Player " + self.P2.getName())
            p1 = " is at position " + str(self.P1.getPosition())
            p2 = " is at position " + str(self.P2.getPosition())
            self.e1.set(p1)
            self.e2.set(p2)
            self.displayWinner()
        else:
            self.msg.set("No player is in the game!")


    def gameHelp(self):
        helpMsg = """User instruction:
In the game, players roll their own dices and move several steps forward corresponding to the rolling points in a round.
If any player reaches the special positions 11/22/33/44, this player will be penalised by having 5 subtracted from the current position.
The winner is the one who reaches a final position of 50 on the board first.
If two players reaches position 50 in the same round, both wins."""
        self.msg.set(helpMsg)

    def about(self):
        aboutMsg = """Author: Nancy-C
Version: 15/12/2017"""
        self.msg.set(aboutMsg)



G = Game()
        
