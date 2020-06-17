from tkinter import *
import sys
import os.path
import json


class Error(Exception):
    pass


class Bad_word_detection(Error):
    pass


class File_name_error(Error):
    pass


class UserError(Error):
    pass


class Make_menu_interface():

    def __init__(self, name):
        self.name = name
        self.status = 0

    def make_interface(self):
        def file_save():
            def save_content():
                try:
                    filename = fentry.get()
                    filecontent = fcontent.get(0.0, END)
                    if 'fuck' in filecontent.lower():
                        fcontent.delete(0.0, END)
                        raise Bad_word_detection('Bad word was detected')

                    if filename.lower().find('.txt') == -1:
                        fentry.delete(0, END)
                        raise File_name_error("File name was not defined")

                except Bad_word_detection as e:
                    fcontent.insert(0.0, e)

                except File_name_error as e:
                    fentry.insert(0, e)

                else:
                    file = open(filename, 'w')
                    file.write(filecontent)

            if self.status == 1:
                froot = Toplevel()
                froot.title("save file")
                froot.geometry('400x600')

                Label(froot, text="file name").grid(row=0, column=0, sticky=W)
                fentry = Entry(froot, bg='lightgreen', width=30)
                fentry.grid(row=0, column=1, sticky=W)

                Label(froot, text="content").grid(row=1, column=0)
                fbutton = Button(froot, text='save', command=save_content)
                fbutton.grid(row=1, column=1, sticky=W)

                fcontent = Text(froot, bg='lightgreen', width=50, height=30)
                fcontent.grid(row=2, column=0, columnspan=2, sticky=W)

                froot.mainloop()
            else:
                statent.delete(0, END)
                statent.insert(0, 'You didn\'t submitted')

        def file_load():
            def load_content():
                def replace_bad_word(text, index=0, length=0):
                    c = ''
                    for i in range(length):
                        c += '*'
                    replacement = c
                    return '%s%s%s' % (text[:index], replacement, text[index + length:])

                def badword_detect(word, content):
                    try:
                        badwordlen = len(word)
                        lcon = content.lower()
                        count = lcon.count(word)
                        badwordindex = lcon.find(word)
                        if badwordindex != -1:
                            while count:
                                badwordindex = lcon.find(word)
                                lcon = replace_bad_word(lcon, badwordindex, badwordlen)
                                content = replace_bad_word(content, badwordindex, badwordlen)
                                count -= 1
                            raise Bad_word_detection("Bad word was detected\n\n")
                    except Bad_word_detection as e:
                        lcontent.delete(0.0, END)
                        lcontent.insert(0.0, e)
                        lcontent.insert(END, content)
                    else:
                        lcontent.delete(0.0, END)
                        lcontent.insert(END, content)
                    finally:
                        return content

                try:
                    filename = lentry.get()
                    if not os.path.exists(filename):
                        raise File_name_error('no such file in this directory')
                except File_name_error as e:
                    lentry.delete(0, END)
                    lentry.insert(0, e)
                else:
                    file = open(filename, 'r')
                    content = file.read()
                    content = badword_detect('fuck', content)
                    content = badword_detect('shit', content)
                    badword_detect('bitch', content)
                    # add any words that you want replace, use this form

            if self.status == 1:
                lroot = Toplevel()
                lroot.title('load file')
                lroot.geometry('400x600')

                Label(lroot, text='file name').grid(row=0, column=0, sticky=W)
                lentry = Entry(lroot, bg='lightblue', width=30)
                lentry.grid(row=0, column=1, sticky=W)

                Label(lroot, text='content').grid(row=1, column=0)
                lbutton = Button(lroot, text="load", command=load_content)
                lbutton.grid(row=1, column=1, sticky=W)

                lcontent = Text(lroot, bg='lightblue', width=50, height=30)
                lcontent.grid(row=2, column=0, columnspan=2, sticky=W)

                lroot.mainloop()
            else:
                statent.delete(0, END)
                statent.insert(0, 'You didn\'t submitted')

        def func_first():
            print("first")

        def func_second():
            print("second")

        def Exit_method():
            sys.exit()

        def Userexist():
            try:
                uid = IDent.get()
                upw = PWent.get()
                if uid not in user.keys():
                    raise KeyError
            except KeyError:
                IDent.delete(0, END)
                statent.delete(0, END)
                statent.insert(0, "There is no id")
                self.status = 0
            else:
                if user.get(uid) == upw:
                    self.status = 1
                    statent.delete(0, END)
                    statent.insert(0, 'Submitted')
                else:
                    PWent.delete(0, END)
                    statent.delete(0, END)
                    statent.insert(0, 'wrong password')
                    self.status = 0

        def Createuser():
            uid = IDent.get()
            upw = PWent.get()
            try:
                if uid in user.keys():
                    raise UserError('User is already exist')
                if len(uid) < 4:
                    raise UserError('Please use over 4chars in ID')
                elif len(upw) < 7:
                    raise UserError('Please use over 7chars in Password')
            except UserError as e:
                IDent.delete(0, END)
                PWent.delete(0, END)
                statent.delete(0, END)
                statent.insert(0, e)
            else:
                user[uid] = upw
                with open('users.json', 'w', encoding='utf-8') as modifyf:
                    json.dump(user, modifyf)
                IDent.delete(0, END)
                PWent.delete(0, END)
                statent.delete(0, END)
                statent.insert(0, 'Create succeed')

        with open('users.json', 'r') as f:
            user = json.load(f)
        print(user)

        self.name = Tk()
        self.name.title('my app')
        self.name.geometry('400x600')

        Label(self.name, text="ID").grid(row=0, column=0)
        IDent = Entry(self.name, bg="lightpink", width=30)
        IDent.grid(row=0, column=1)

        Label(self.name, text="Password").grid(row=1, column=0)
        PWent = Entry(self.name, bg="lightpink", width=30)
        PWent.grid(row=1, column=1)

        ubut = Button(self.name, text='submit', command=Userexist)
        ubut.grid(row=2, column=0)

        cbut = Button(self.name, text='create', command=Createuser)
        cbut.grid(row=2, column=1, sticky=W)

        statent = Entry(self.name, bg='lightcoral', width=30)
        statent.grid(row=3, column=0, columnspan=2)

        mmenu = Menu(self.name)
        smenu = Menu(mmenu)
        filemenu = Menu(smenu)
        funcmenu = Menu(smenu)

        mmenu.add_cascade(label="Menu", menu=smenu)

        smenu.add_cascade(label="file", menu=filemenu)
        filemenu.add_command(label="save", command=file_save)
        filemenu.add_command(label="load", command=file_load)

        smenu.add_cascade(label="function", menu=funcmenu)
        funcmenu.add_command(label="first", command=func_first)
        funcmenu.add_command(label="second", command=func_second)

        smenu.add_separator()

        smenu.add_command(label="exit", command=Exit_method)

        self.name.config(menu=mmenu)

    def start(self):
        self.name.mainloop()


if __name__ == '__main__':
    if not os.path.exists('users.json'):
        admin = {"admin": "admin"}
        with open('users.json', 'w', encoding='utf-8') as CreateFile:
            json.dump(admin, CreateFile)
    m1 = Make_menu_interface('root')
    m1.make_interface()
    m1.start()
