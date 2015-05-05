"""

Based on tutorial on zetcode.com:
zetcode.com/gui/tkinter/layout/

"""

from PIL import Image, ImageTk
from Tkinter import Tk, W,E, Label, BOTH, RIGHT, RAISED
from ttk import Frame, Style, Button
from ttk import Entry

from test_script import external_method1, external_method2


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()

    def callback():
      print "hello"
        
    def capture_message(self):
      self.create_text(self.winfo_width()/2, self.winfo_height()/2, 
                      text="GAZE CAPTURED", fill="white")

    def initUI(self):
      
        self.parent.title("Student Name Recollection Helper")
        #self.pack(fill=BOTH, expand=1)

        style = Style()
        style.configure("TButton", padding=(0, 5, 0, 5), 
                        font='serif 10')
        style.configure("TFrame", background="#333")        

        self.columnconfigure(0,pad=10, minsize=300)
        self.columnconfigure(1,pad=10)
        #self.columnconfigure(2,pad=10)
        #self.columnconfigure(3,pad=10)

        self.rowconfigure(0,pad=10, minsize=500)
        self.rowconfigure(1,pad=10)
        #self.rowconfigure(2,pad=3)
        #self.rowconfigure(3,pad=3)
        #self.rowconfigure(4,pad=3)

        def capture():
          external_method1()
        def other():
          external_method2()

        frame = Frame(self, relief=RAISED, borderwidth=20)
        frame.grid(row=0, column=0)
        #frame.pack()

        cls = Button(self, text="Capture Gaze", command=capture)
        cls.grid(row=1, column=0)
        bck = Button(self, text="Focus Camera", command=other)
        bck.grid(row=1, column=1)

        
        self.pack()

#
#        entry = Entry(self)
#        entry.grid(row = 0, columnspan=4, sticky = W+E)
#        
#        #style.configure("TButton", font='serif 10')        
#
#        frame = Frame(self, relief=RAISED, borderwidth=1)
#        frame.grid(row=0, column=0)
#            #fill=BOTH, expand=1)
#
#        #frame2 = Frame(self, relief=RAISED, borderwidth=15)
#        #frame2.pack(fill=BOTH, expand=1)
#
#
#        cb = Button(self, text="Capture Gaze", command=capture)
#        cb.grid(row=1,column=0)
#        #cb.pack(side=RIGHT, padx=5,pady=5)
#        b2 = Button(self, text="Other button", command=other)
#        cb.grid(row=1,column=1)
#        #b2.pack(side=RIGHT, padx=5,pady=5)
              

def main():
    root = Tk()
    #root.geometry("500x500+200+200")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

