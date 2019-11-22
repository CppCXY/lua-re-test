#!/usr/bin/env python3

"""Basic regular expression demonstration facility (Perl style syntax)."""

from tkinter import *
import re
import subprocess
class ReDemo:

    def __init__(self, master):
        self.master = master

        self.promptdisplay = Label(self.master, anchor=W,
                text="Enter a lua-style regular expression:")
        self.promptdisplay.pack(side=TOP, fill=X)

        self.regexdisplay = Entry(self.master)
        self.regexdisplay.pack(fill=X)
        self.regexdisplay.focus_set()

        self.labeldisplay = Label(self.master, anchor=W,
                text="Enter a string to match:")
        self.labeldisplay.pack(fill=X)
        self.showframe = Frame(master)
        self.showframe.pack(fill=X, anchor=W)

        self.showvar = StringVar(master)
        self.showvar.set("first")


        self.stringdisplay = Text(self.master, width=60, height=4)
        self.stringdisplay.pack(fill=BOTH, expand=1)
        self.stringdisplay.tag_configure("hit", background="yellow")

        self.grouplabel = Label(self.master, text="Groups:", anchor=W)
        self.grouplabel.pack(fill=X)

        self.grouplist = Listbox(self.master)
        self.grouplist.pack(expand=1, fill=BOTH)

        self.regexdisplay.bind('<Key>', self.recompile)
        self.stringdisplay.bind('<Key>', self.reevaluate)

        self.compiled = None
        self.recompile()

        btags = self.regexdisplay.bindtags()
        self.regexdisplay.bindtags(btags[1:] + btags[:1])

        btags = self.stringdisplay.bindtags()
        self.stringdisplay.bindtags(btags[1:] + btags[:1])


    def genLuaCode(self,rep,text):
        return """
        local t={{string.find([[{0}]],[[({1})]])}}
        for i,v in ipairs(t) do 
            if i>2 then
             print((i-2).." : "..v)
            end
        end 
        """.format(text,rep)

    def recompile(self, event=None):
        try:
            self.compiled=self.regexdisplay.get()
        except re.error as msg:
            self.compiled = None
        self.reevaluate()

    def reevaluate(self, event=None):
        self.grouplist.delete(0, END)
        if self.compiled=="" or self.compiled is None:
            return
        text = self.stringdisplay.get("1.0", END)
        if text=="" or text is None:
            return
        try:
            luacode=self.genLuaCode(self.compiled,text)
            comp=subprocess.run(["lua","-e",luacode],stdout=subprocess.PIPE)
            res=str(comp.stdout.decode("utf8")).split("\n")
            #self.grouplist.insert(END, res)
            for s in res:
                self.grouplist.insert(END, s)
        except:
            pass
        
        


# Main function, run when invoked as a stand-alone Python program.

def main():
    root = Tk()
    root.title("lua regular test")
    demo = ReDemo(root)
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()

if __name__ == '__main__':
    main()
