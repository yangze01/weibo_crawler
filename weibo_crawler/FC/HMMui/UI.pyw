from tkinter import*
from tkinter.filedialog import*
import main
import Lexicon
import Rule
from tkinter.messagebox import *
#the choose file window
def choose_file():
    clean()
    #filename is to save the name of user-choosing
    filename=askopenfilename(initialdir = 'C:/Python')
    fo = open(filename,"r",encoding="gbk")
    text.delete(0.0,END)
    text.insert(0.0,fo.read())
    fo.close()
    #these two lines of code are to put the curse and scroll bar to the end
    text.focus_force()
    text.see(END)

#the save file window
def save_file():
    filename =asksaveasfilename(initialdir = 'C:/Python')
    fo = open(filename,"w",encoding="gbk")
    t = text_output.get(0.0,END)
    fo.write(t)
    fo.close()
    Prompt_box("File Saving is OK. ")

#this funcion is to call the main.py to segment the words and sentences
def SegSentence(text_to_seg,isToSentence=TRUE):
    text_to_seg = main.preprocess(text_to_seg)
    global text_output
    if(isToSentence):
        #we want to segment the paragraph into sentences
        sentenceList = main.segmentSentence(text_to_seg)
        text_output.insert(END,"Result for segmentation of sentences: \n")
        i = 1

        for s in sentenceList:
            #put the sentence into the textbox
            text_output.insert(END,str(i)+'.: ')
            text_output.insert(END,str(s)+"\n")
            i+=1
    else:
        text_output.insert(END,"\n\nResult for segmentation of words: \n")
        sentenceListForWords = main.segmentSentence(text_to_seg,True)
        i = 1
        for s in sentenceListForWords:
            words = main.segmentWord(s)
            text_output.insert(END,str(i)+'.: ')
            for w in words:
                #put the words into the textbox
                text_output.insert(END,w + " | ")
            text_output.insert(END,"\n")
            i+=1
        text_output.insert(END,"\nIf you aren't satisfied with result, you can add words or update the frequency in the lexicon.")
    #make the scroll bar to the end
    text_output.focus_force()
    text_output.see(END)

#the Lexicon Modify window
def Lexicon_modify():
    # a b is the two entries' context
    a=StringVar()
    b=StringVar()
    Lexicon_window=Toplevel(root)
    Lexicon_window.title('Lexicon')
    Lexicon_window.geometry('520x305+420+200')###2
    Lexicon_contain=Text(Lexicon_window,width=40,height=20,bd=4)
    Lexicon_contain.grid(row=0,column=0,rowspan=25)
    sl_3= Scrollbar(Lexicon_window)
    sl_3.grid(row=0,column=1,rowspan=25,sticky='ns')
    Lexicon_contain['yscrollcommand'] = sl_3.set
    sl_3['command'] =Lexicon_contain.yview

    label_1=Label(Lexicon_window,text='Word : ',width=10)
    label_1.grid(row=1,column=2)


    modify_contain=Entry(Lexicon_window,width=13,textvariable = a)
    modify_contain.grid(row=1,column=3)
    label_2=Label(Lexicon_window,text='Frequency : ',width=10)
    label_2.grid(row=2,column=2)

    label_3=Label(Lexicon_window,text='INFO : You can delete and modify\n words in the left box directly. ',width=30)
    label_3.grid(row=10,column=2,columnspan=20)


    cipin=Entry(Lexicon_window,width=13,textvariable = b)
    cipin.grid(row=2,column=3)
    #to add word into the box
    def AddWord(word,freq):
        try:
            fre = int(freq)
            str = word+" "+freq+'\n'
            Lexicon_contain.insert(END,str)
            #gundongtiao
            Lexicon_contain.focus_force()
            Lexicon_contain.see(END)
            Prompt_box("Okay!")
        except:
            Prompt_box("Your input is invalid.")
    #to save the current context into the box
    def SaveDict():
        try:
            fo = open(Lexicon.url,"w",encoding="gbk")
            fo.write(Lexicon_contain.get(0.0,END))
            fo.close()
            main.isInitialized = False
            Prompt_box("Okay!")
        except:
            Prompt_box("Error.")
    finish_but=Button(Lexicon_window,bd=3,text='Finish',command=SaveDict)#comand
    finish_but.grid(row=26,column=0,ipadx=16)

    #Lexicon_contain.insert(END,a.get()+' '+b.get()+'\n')
    modify_but=Button(Lexicon_window,bd=3,text='ADD',command=lambda:AddWord(a.get(),b.get()))
    modify_but.grid(row=3,column=3,ipadx=16)
    fo = Lexicon.loadDict()
    lst = Lexicon.readDict(fo)
    for l in lst:
        "".split()
        word,freq = l.split(" ")[0:2]
        Lexicon_contain.insert(END,word+" "+freq+"\n")
#The Rule Modify Window
def Rule_modify():
    Rule_window=Toplevel(root)
    Rule_window.title('Rule')
    Rule_window.geometry('520x305+420+200')
    rule_contain=Text(Rule_window,width=40,height=20,bd=4)
    rule_contain.grid(row=0,column=0,rowspan=25)
    sl_3= Scrollbar(Rule_window)
    sl_3.grid(row=0,column=1,rowspan=25,sticky='ns')
    rule_contain['yscrollcommand'] = sl_3.set
    sl_3['command'] =rule_contain.yview
    def save():
        try:
            with open(Rule.RuleUrl,'w',encoding='gbk')  as fo:
                fo.write(rule_contain.get(0.0,END))
            main.isInitialized = False
            Prompt_box("Okay!")
        except:
            Prompt_box("Error!")

    finish_but=Button(Rule_window,bd=3,text='Finish',command=save)#comand
    finish_but.grid(row=26,column=0,ipadx=16)
    label_1=Label(Rule_window,text='Rule to add : ')
    label_1.grid(row=1,column=2)
    modify_contain=Text(Rule_window,width=27,height=8)
    modify_contain.grid(row=2,column=2)
    modify_but=Button(Rule_window,bd=3,text='Add',command=lambda:rule_contain.insert(END,modify_contain.get(1.0,END)))
    modify_but.grid(row=4,column=2,ipadx=16)

    label_3=Label(Rule_window,text='INFO : You can delete and modify\n rules in the left box directly. ',width=30)
    label_3.grid(row=10,column=2,columnspan=20)

    #initialize
    with open(Rule.RuleUrl,"r",encoding="gbk") as fo:
        rule_contain.insert(END,fo.read()+'\n')

#the about box
def about_box():
    about_box=Toplevel(root)
    about_box.title('About')
    about_box.geometry('400x80+450+300')###12
    contain=Label(about_box,text='Program Name: RossetaSeg'+'\n'+'Authors: Yuchen Lin & Zhaorun Han'+'\n'+'Version: 1.0.2  ( 2015.1.9)'+'\n'+'Email: yuchenlin@sjtu.edu.cn')
    contain.pack()

#the instruction box
def instruction_box():
    instruction_box=Toplevel(root)
    instruction_box.title('Instructions')
    instruction_box.geometry('450x360+450+200')###11
    ins_title='Instructions:'
    label_title=Label(instruction_box,text=ins_title)
    label_title.configure(font='Dotum 12 bold')
    label_title.pack()
    ins ='''
How to segment a text file ?
 1.File -> open
 2.Press the right button 'To sentences'.
 3.Press the right button 'To words'.
 4.Press the 'Save' button to Save the file.

How to modify lexicon ?
 1.Lexicon-> modify
 2.You can add a word with its frequency on the right plane.
 3.You can directly modify or delete words or frequencies on the left box.
 4.Press Finish to save the lexicon.

How to modify rules ?
There are two kinds of rules for you to choose.
One is "CHANGE a WITH b", the other one is "DELETE x".
 1.Rule-> modify
 2.You can add a rule on the right plane.
 3.You can directly modify or delete rules on the left box.
 4.Press Finish to save the rules.

    '''
    label=Label(instruction_box,text=ins,justify=LEFT)
    label.pack()


def Prompt_box(contain,title="INFO"):
    showinfo(title,contain)

root=Tk(className=' RossetaSeg')
root.geometry('723x525+320+95')
#the menu
menu_but_F=Menubutton(root,text='File',underline=0)
menu_but_F.grid(row=0,column=0,ipadx=20)
menu_but_F.menu=Menu(menu_but_F)
menu_but_F.menu.add_command(label='Open',command=choose_file)
menu_but_F.menu.add_command(label='Exit',command=root.destroy)
menu_but_F['menu']=menu_but_F.menu

menu_but_L=Menubutton(root,text='Lexicon',underline=0)
menu_but_L.grid(row=0,column=1,ipadx=20)
menu_but_L.menu=Menu(menu_but_L)
menu_but_L.menu.add_command(label='Modify',command=Lexicon_modify)
menu_but_L['menu']=menu_but_L.menu

menu_but_R=Menubutton(root,text='Rule',underline=0)
menu_but_R.grid(row=0,column=2,ipadx=20)
menu_but_R.menu=Menu(menu_but_R)
menu_but_R.menu.add_command(label='Modify',command=Rule_modify)
menu_but_R['menu']=menu_but_R.menu

menu_but_H=Menubutton(root,text='Help',underline=0)
menu_but_H.grid(row=0,column=3,ipadx=20)
menu_but_H.menu=Menu(menu_but_H)
menu_but_H.menu.add_command(label='Instructions',command=instruction_box)
menu_but_H.menu.add_command(label='About',command=about_box)
menu_but_H['menu']=menu_but_H.menu
#the Main Seg window
text=Text(root,height=18,bd=5)
text.grid(row=1,column=0,columnspan=25,rowspan=7)
but_to_sentense=Button(root,bd=3,text='GET Sentences',command=(lambda:SegSentence(text.get('1.0',END))))
but_to_sentense.grid(row=3,column=35,ipadx=17)
but_to_words=Button(root,bd=3,text='GET Words',command=(lambda:SegSentence(text.get('1.0',END),False)))
but_to_words.grid(row=5,column=35,ipadx=26)

sl = Scrollbar(root)
sl.grid(row=1,column=26,sticky='ns',rowspan=7)
text['yscrollcommand'] = sl.set
sl['command'] = text.yview


#the output text box
text_output=Text(root,height=18,bd=5)
text_output.grid(row=8,column=0,columnspan=25,rowspan=7)
sl_2= Scrollbar(root)
sl_2.grid(row=8,column=26,sticky='ns',rowspan=7)
text_output['yscrollcommand'] = sl_2.set
sl_2['command'] = text_output.yview
save_but=Button(root,text='Save',command=save_file,bd=3)
save_but.grid(row=14,column=35,ipadx=45)

def clean():
    text.delete(0.0,END)
    text_output.delete(0.0,END)
clean_but=Button(root,text='Clean',command=clean,bd=3)
clean_but.grid(row=10,column=35,ipadx=45)

text.insert(0.0,"Input")
text_output.insert(0.0,'Output')
root.mainloop()
