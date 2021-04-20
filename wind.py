from tkinter import *
from speaks import say_print
from  greetings import goodbye
from os import sys
from greetings import help_u, hi_me
from tkinter import messagebox
from tkinter import ttk 



root = Tk()

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control) 
tab_control.add(tab1, text='Первая')  
tab_control.pack(expand=1, fill='both')  

tab2 = ttk.Frame(tab_control) 
tab_control.add(tab2, text='Помощь')  
tab_control.pack(expand=1, fill='both')  

'''
frame_top = Frame(tab1, bg='#ffb700', bd=1)
frame_top.place(relx=0, rely=0.15, relwidth=1, relheight=0.5)

frame_bot = Frame(tab1, bg='#ffb100', bd=1)
frame_bot.place(relx=0, rely=0.45, relwidth=1, relheight=0.5)
'''
root.title('Голосовой помощние Nonima')
root.geometry('1000x600')

def clicked():  
    messagebox.showinfo(command=say_print)

btn = Button(tab1, text='"Эй, Нонима"', font=("Arial Bold", 24), command=say_print)
btn.place(relx=0, rely=0.75, relwidth=1, relheight=0.5)
btn.pack()	

btn1 = Button(tab1, text='"Пока, Нонима"', font=("Arial Bold", 24), command=sys.exit)
btn1.pack()

lbl1 = Label(tab2, text='Давайте, я расскажу, как со мной работать'
	'\nПо команде "google" - открою браузер и покажу результаты поиска по запросу.'
    '\nПо команде "видео" -  выведу результаты поиск на ютубе'
    '\nПо команде "википедия" - готова зачитать 2 преложения.'
    '\nПо команде "погода" - выведу погоду на сегодня'
    '\nПо команде "до связи" - я отключаюсь', font=("Arial Bold", 20))  
lbl1.place(relx=0, rely=0.15, relwidth=1, relheight=0.5)



root.title('Голосовой помощние Nonima')
root.geometry('1000x600')

root.mainloop()