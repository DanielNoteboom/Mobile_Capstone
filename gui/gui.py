"""

Based on tutorial on zetcode.com:
zetcode.com/gui/tkinter/layout/

"""
import os
import time



from PIL import Image, ImageTk
from Tkinter import Tk, W,E, Label, BOTH, RIGHT, RAISED
from ttk import Frame, Style, Button
from ttk import Entry

from gui_helper import take_snapshot, run_pupil, facial_detection



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

    def launch_pupil():
      newpid = os.fork()
      if newpid ==0:
        os.execv("../pupil/run_capture", ['foo'])
      else:
        print "Loading... please wait"  

    def initUI(self):
      run_pupil()


      self.parent.title("Student Name Recollection Helper")
      #self.pack(fill=BOTH, expand=1)

      style = Style()
      style.configure("TButton", padding=(0, 5, 0, 5), 
                      font='serif 10')
      style.configure("TFrame", background="#333")        

      self.columnconfigure(0,pad=10, minsize=300, weight=1)
      self.columnconfigure(1,pad=10)
      #self.columnconfigure(2,pad=10)
      #self.columnconfigure(3,pad=10)

      self.rowconfigure(0,pad=10, minsize=500, weight=1)
      self.rowconfigure(1,pad=10, weight=1)
      #self.rowconfigure(2,pad=3)
      #self.rowconfigure(3,pad=3)
      #self.rowconfigure(4,pad=3)

      self.pack()

      def capture():
        pic_file, coord = take_snapshot()
        facial_detection(pic_file, coord)


      def other():
        external_method2()

      #frame = Frame(self, relief=RAISED, borderwidth=20)
      #frame.grid(row=0, column=0)

      
      b2 = Button(self, text="Loading", command=other)
      b2.grid(row=0,column=0)
      #frame.pack()

      #f2 = Frame(frame, relief=RAISED, borderwidth=10)
      #f2.pack(fill=BOTH, expand=1)
      ##f3 = Frame(frame, relief=RAISED, borderwidth=10)
      #f3.pack(fill=BOTH, expand=1)

      #cls = Button(f2, text="Cls")
      ##cls.pack(fill=BOTH, expand=1)
      #bck = Button(f3, text="Back")
      ##bck.grid(fill=BOTH, expand=1)



      #cb.pack(side=RIGHT, padx=5,pady=5)
      b2 = Button(self, text="Focus camera", command=other)
      b2.grid(row=1,column=0)
      cb = Button(self, text="Capture Gaze", command=capture)
      cb.grid(row=1,column=1)
      #b2.pack(side=RIGHT, padx=5,pady=5)
            

def main():
    root = Tk()
    #root.geometry("500x500+200+200")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

