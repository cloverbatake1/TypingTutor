#!/usr/bin/python3.6

import tkinter as tk
import random
import re

class Word:
    def __init__(self, name, x):
        self.x = x
        self.y = 40
        self.name = name
        self.label0 = tk.Label(frm, text= name,  borderwidth=0, font=('fixedSys', fontsize), fg='black', bg='white')
        self.label1 = tk.Label(frm, text='', borderwidth=0, font=('fixedSys', fontsize), fg='black', bg='cyan')
        self.label2 = tk.Label(frm, text='', borderwidth=0, font=('fixedSys', fontsize), fg='black', bg='white') # erase left frame of label1

    def __del__(self):
        self.label0.destroy()
        self.label1.destroy()
        self.label2.destroy()

    def dispLabel(self, keytype):
        global fRun, menuLabel, hiscore, score, scoreLabel
        if self.name.startswith(keytype):
            self.label1.configure(text=keytype)
        else:
            self.label1.configure(text='')
        self.label0.place(x=self.x, y=self.y)
        self.label1.place(x=self.x, y=self.y)
        self.label2.place(x=self.x, y=self.y)
        self.y += 1
        if self.y > 640:
            if score > hiscore:
                hiscore = score
                scoreLabel.configure(text='*** HiScore:%d ***,    Score:%d,    Miss:%d' % (hiscore, score, miss))
            fRun = False
            menuLabel.pack()

def launch():
    # launch the new word
    global texts, words #, speed , fRun
    if fRun == True:
        if len(texts) == 0:
            with open('/home/cloverbatake/bin/typing/words.txt', mode='r') as f:
                texts = f.readlines()
            for txt in texts:
                if not re.search(r'\w', txt):
                    texts.remove(txt)
        txt = random.choice(texts)
        words.append(Word(str.strip(txt), random.randint(0, 10) * 100))
        texts.remove(txt)
        frm.after(round(speed * 35), launch) # adjust 35 for prevent overlap words



def key(event):
    global keytype, num, words, hiscore, score, scoreLebel, texts, fRun, menuLabel, speed, miss
    if fRun == True:
        for word in words:
            if event.char == '\b':
                keytype = keytype[:-1]
                break
            elif word.name.startswith(keytype + event.char):
                # partial match
                keytype += event.char
                break
            elif (word.name == keytype) and (event.char == '\r'):
                # exact match
                score += 1
                scoreLabel.configure(text='HiScore:%d,    Score:%d,    Miss:%d' % (hiscore, score, miss))
                words.remove(word)
                del word
                keytype = ''
                break
        else:
            # no match
            miss += 1
            scoreLabel.configure(text='HiScore:%d,    Score:%d,    Miss:%d' % (hiscore, score, miss))
            print('\a') # beep

    elif fRun == False:
        if (event.char == 's'):
            speed = 120
            score = 0
            miss = 0
            scoreLabel.configure(text='HiScore:%d,    Score:%d,    Miss:%d' % (hiscore, score, miss))
            for word in words:
                del word
            words.clear()
            texts.clear()
            keytype = ''
            menuLabel.pack_forget()
            fRun = True
            main()
            launch()
        elif (event.char == 'q'):
            exit()


def main():
    global keytype, fRun, speed

    if fRun == True:
        speed *= 0.9999
        if speed < 30:
            speed = 30
        for word in words:
            word.dispLabel(keytype)
        frm.after(round(speed), main)




fontsize = 30
frm = tk.Tk()
frm.title('Typing Tutor')
frm.geometry("1250x540")
frm.attributes("-zoomed", "1")
frm.configure(bg='white')
scoreLabel = tk.Label(frm, text= 'HiScore:0,    Score:0,    Miss:0',  borderwidth=0, font=('fixedSys', fontsize), fg='black', bg='yellow')
scoreLabel.pack()
menuLabel = tk.Label(frm, text= 's: Start, q: Quit',  borderwidth=0, font=('fixedSys', fontsize), fg='white', bg='green')
menuLabel.pack()

words = [] # words on screen
keytype = ''# word in the middle of writing
score = 0 # number of correct
hiscore = 0
miss = 0 # type miss
texts = [] # waiting text
fRun = False # gaming

frm.bind("<Key>", key)
frm.focus_set()
frm.mainloop()


