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
        if not os.path.exists('users.json'):
            admin = {"admin": "admin"}
            with open('users.json', 'w', encoding='utf-8') as CreateFile:
                json.dump(admin, CreateFile)
        self.name = name
        self.status = 0
        self.coorlist = list()
        self.xcoord = list()
        self.ycoord = list()

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
                    fcontent.delete(0.0, END)
                    fcontent.insert(0.0, 'save succeed')

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

        def canvas_move():
            def setcoor():
                coorstr = coorent.get()
                if len(coorstr.split(',')) < 6:
                    canvstat.delete(0, END)
                    canvstat.insert(0, 'Please insert at least 3 coordinates')
                else:
                    try:
                        testcoord = list(map(int, coorstr.split(',')))
                    except ValueError:
                        canvstat.delete(0, END)
                        canvstat.insert(0, "Please input numbers")
                    else:
                        self.coorlist = coorstr.split(',')
                        coorent.delete(0, END)
                        coorent.insert(0, str(len(self.coorlist) // 2) + ' coordinates input succeed')

            def startcanvas():
                def moveup(event):
                    for index, item in enumerate(canv.coords(1)):
                        if index % 2 != 0:
                            self.ycoord.append(item)
                    if min(self.ycoord) < 1:
                        pass
                    else:
                        canv.move(1, 0, -5)
                        canv.update()
                    self.ycoord = []

                def movedown(event):
                    for index, item in enumerate(canv.coords(1)):
                        if index % 2 != 0:
                            self.ycoord.append(item)
                    if max(self.ycoord) > 400:
                        pass
                    else:
                        canv.move(1, 0, 5)
                        canv.update()
                    self.ycoord = []

                def moveleft(event):
                    for index, item in enumerate(canv.coords(1)):
                        if index % 2 == 0:
                            self.xcoord.append(item)
                    if min(self.xcoord) < 5:
                        pass
                    else:
                        canv.move(1, -5, 0)
                        canv.update()
                    self.xcoord = []

                def moveright(event):
                    for index, item in enumerate(canv.coords(1)):
                        if index % 2 == 0:
                            self.xcoord.append(item)
                    if max(self.xcoord) > 400:
                        pass
                    else:
                        canv.move(1, 5, 0)
                        canv.update()
                    self.xcoord = []

                if len(self.coorlist) == 0:
                    canvstat.delete(0, END)
                    canvstat.insert(0, 'Please press submit button before start')
                else:
                    canvasapp = Toplevel()
                    canvasapp.title('start move')
                    canv = Canvas(canvasapp, width=400, height=400)
                    canv.pack()

                    coordinate = list(map(int, self.coorlist))
                    canv.create_polygon(coordinate)
                    self.coorlist = []

                    canv.bind("<Up>", moveup)
                    canv.bind("<Down>", movedown)
                    canv.bind("<Left>", moveleft)
                    canv.bind("<Right>", moveright)
                    canv.focus_set()

                    canv.mainloop()

            if self.status == 1:
                canvmainroot = Toplevel()
                canvmainroot.title('canvas')
                canvmainroot.geometry('400x600')

                Label(canvmainroot, text='input coordinate').grid(row=0, column=0, columnspan=2)
                coorent = Entry(canvmainroot, width=30)
                coorent.grid(row=1, column=0, columnspan=2)
                submitbut = Button(canvmainroot, text='submit', command=setcoor)
                submitbut.grid(row=2, column=0)
                startbut = Button(canvmainroot, text='start', command=startcanvas)
                startbut.grid(row=2, column=1)
                canvstat = Entry(canvmainroot, width=30)
                canvstat.grid(row=3, column=0, columnspan=2)
                canvstat.insert(0, "use this form (x1,y1,x2,y2,...)")

                canvmainroot.mainloop()
            else:
                statent.delete(0, END)
                statent.insert(0, 'You didn\'t submitted')

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

        def Finduser():
            def replacePW():
                userid = Fident.get()
                userpw = Fcpwent.get()
                newpw = Fnpwent.get()
                if userid not in user.keys():
                    Fstatent.delete(0, END)
                    Fident.delete(0, END)
                    Fstatent.insert(0, f'[{userid}] is not exist')
                else:
                    if user[userid] == userpw:
                        if len(newpw) < 7:
                            Fstatent.delete(0, END)
                            Fnpwent.delete(0, END)
                            Fstatent.insert(0, 'Please use over 7chars in Password')
                        else:
                            user[userid] = newpw
                            Fstatent.delete(0, END)
                            Fstatent.insert(0, "replace succeed")
                    else:
                        Fstatent.delete(0, END)
                        Fcpwent.delete(0, END)
                        Fstatent.insert(0, 'Please check your current password')

            def findPW():
                userid = Fident.get()
                try:
                    userpw = '[' + userid + "]'s password is '" + user[userid] + "'"
                    if userid not in user.keys():
                        raise KeyError
                except KeyError:
                    Fstatent.delete(0, END)
                    Fstatent.insert(0, f'[{userid}] is not exist')
                else:
                    Fstatent.delete(0, END)
                    Fstatent.insert(0, userpw)

            fuserroot = Toplevel()
            fuserroot.title('find user')
            fuserroot.geometry('400x600')

            Label(fuserroot, text="find").grid(row=0, column=0, columnspan=2)

            Label(fuserroot, text='ID').grid(row=1, column=0)
            Fident = Entry(fuserroot, bg='lightpink', width=30)
            Fident.grid(row=1, column=1)

            Label(fuserroot, text='Current pw').grid(row=2, column=0)
            Fcpwent = Entry(fuserroot, bg='lightpink', width=30)
            Fcpwent.grid(row=2, column=1)

            Label(fuserroot, text='New pw').grid(row=3, column=0)
            Fnpwent = Entry(fuserroot, bg='lightpink', width=30)
            Fnpwent.grid(row=3, column=1)

            Fpwbut = Button(fuserroot, text='find pw', command=findPW)
            Fpwbut.grid(row=4, column=0)

            Frpwbut = Button(fuserroot, text='replace pw', command=replacePW)
            Frpwbut.grid(row=4, column=1)

            Fstatent = Entry(fuserroot, bg='lightcoral', width=30, takefocus='false')
            Fstatent.grid(row=5, column=0, columnspan=2)

            fuserroot.mainloop()

        def Deleteuser():
            DeleteMessage = "\"I'll delete this (ID) account\""

            def Deleteuserinfo():
                DelID = DeIDent.get()
                DelPW = DePWent.get()
                DelMES = DeMesent.get()
                if DelID == 'admin':
                    DeIDent.delete(0, END)
                    DePWent.delete(0, END)
                    DeMesent.delete(0, END)
                    Dstaent.delete(0, END)
                    Dstaent.insert(0, 'You cannot delete admin ID')
                else:
                    try:
                        if user[DelID] == DelPW:
                            if DelMES == f"I'll delete this {DelID} account":
                                del (user[DelID])
                                with open('users.json', 'w') as Delaccount:
                                    json.dump(user, Delaccount)
                                DeIDent.delete(0, END)
                                DePWent.delete(0, END)
                                DeMesent.delete(0, END)
                                Dstaent.delete(0, END)
                                Dstaent.insert(0, "Delete succeed")
                            else:
                                Dstaent.delete(0, END)
                                DeMesent.delete(0, END)
                                Dstaent.insert(0, 'Message doesn\'t match')
                        else:
                            Dstaent.delete(0, END)
                            DePWent.delete(0, END)
                            Dstaent.insert(0, "Mismatch ID and Password")
                    except KeyError:
                        DeIDent.delete(0, END)
                        Dstaent.delete(0, END)
                        Dstaent.insert(0, "user ID is not exist")

            Deleteroot = Toplevel()
            Deleteroot.title('Delete user')
            Deleteroot.geometry('400x600')

            Label(Deleteroot, text="Delete").grid(row=0, column=0, columnspan=2)

            Label(Deleteroot, text="ID").grid(row=1, column=0)
            DeIDent = Entry(Deleteroot, bg='slategray', width=30)
            DeIDent.grid(row=1, column=1)

            Label(Deleteroot, text="Pw").grid(row=2, column=0)
            DePWent = Entry(Deleteroot, bg='slategray', width=30)
            DePWent.grid(row=2, column=1)

            Label(Deleteroot, text=DeleteMessage).grid(row=3, column=0, columnspan=2)
            DeMesent = Entry(Deleteroot, bg='slategray', width=30)
            DeMesent.grid(row=4, column=0, columnspan=2)
            DeMesent.insert(0, 'Please write the above sentence')

            Delbut = Button(Deleteroot, text="delete", command=Deleteuserinfo)
            Delbut.grid(row=5, column=0, columnspan=2)

            Dstaent = Entry(Deleteroot, bg='slategray', width=30, takefocus='false')
            Dstaent.grid(row=6, column=0, columnspan=2)

            Deleteroot.mainloop()

        with open('users.json', 'r') as f:
            user = json.load(f)
        print(user)

        self.name = Tk()
        self.name.title('my app')
        self.name.geometry('400x600')

        Label(self.name, text="Login").grid(row=0, column=0, columnspan=4)

        Label(self.name, text="ID").grid(row=1, column=0)
        IDent = Entry(self.name, bg="lightpink", width=30)
        IDent.grid(row=1, column=1, columnspan=3, sticky=W)

        Label(self.name, text="Password").grid(row=2, column=0)
        PWent = Entry(self.name, bg="lightpink", width=30)
        PWent.grid(row=2, column=1, columnspan=3, sticky=W)

        ubut = Button(self.name, text='submit', command=Userexist)
        ubut.grid(row=3, column=0)

        cbut = Button(self.name, text='create', command=Createuser)
        cbut.grid(row=3, column=1)

        fbut = Button(self.name, text='find', command=Finduser)
        fbut.grid(row=3, column=2)

        dbut = Button(self.name, text="delete", command=Deleteuser)
        dbut.grid(row=3, column=3)

        statent = Entry(self.name, bg='lightcoral', width=30, takefocus='false')
        statent.grid(row=4, column=0, columnspan=4)

        mmenu = Menu(self.name)
        smenu = Menu(mmenu)
        filemenu = Menu(smenu)
        funcmenu = Menu(smenu)

        mmenu.add_cascade(label="Menu", menu=smenu)

        smenu.add_cascade(label="file", menu=filemenu)
        filemenu.add_command(label="save", command=file_save)
        filemenu.add_command(label="load", command=file_load)

        smenu.add_cascade(label="canvas", menu=funcmenu)
        funcmenu.add_command(label="canvas move", command=canvas_move)
        funcmenu.add_command(label="second", command=func_second)

        smenu.add_separator()

        smenu.add_command(label="exit", command=Exit_method)

        self.name.config(menu=mmenu)

    def start(self):
        self.name.mainloop()


if __name__ == '__main__':
    m1 = Make_menu_interface('root')
    m1.make_interface()
    m1.start()
