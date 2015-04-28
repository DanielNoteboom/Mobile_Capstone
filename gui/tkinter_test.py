"""

Based on tutorial on zetcode.com:
zetcode.com/gui/tkinter/layout/

"""

from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH, RIGHT, RAISED
from ttk import Frame, Style, Button


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
        self.pack(fill=BOTH, expand=1)
        
        style = Style()
        style.configure("TFrame", background="#333")        
        #style.configure("TButton", font='serif 10')        

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=1)


        def capture():
          print "hello"

        cb = Button(self, text="Capture Gaze", command=capture)
        cb.pack(side=RIGHT, padx=5,pady=5)
              

def main():
    root = Tk()
    root.geometry("500x500+200+200")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

