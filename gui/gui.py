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

sys.path.insert(0, '..')
from face_comparison.compare import compare

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
      run_pupil()

      #  Defining a method for absolute positioning of an image
      def place_img(self, filename, x, y):
        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        lbl1 = Label(self, image=img)
        lbl1.image = img
        lbl1.place(x=x, y=y)

      self.parent.title("Student Name Recollection Helper")
      #self.pack(fill=BOTH, expand=1)

      style = Style()
      style.configure("TButton", padding=(0, 5, 0, 5), 
                      font='serif 10')
      style.configure("TFrame", background="#333")        
      #style.configure("TLabel", background="#333")        

      self.columnconfigure(0,pad=10, minsize=300, weight=1)
      self.columnconfigure(1,pad=10)

      self.rowconfigure(0,pad=10, minsize=500, weight=1)
      self.rowconfigure(1,pad=10, weight=1)

      self.pack()

      def capture():
        pic_file, coord = take_snapshot()
        pic_file = os.path.absPath(pic_file)
        matches = facial_detection(pic_file, coord)
        matchData = {}
        for match in matches:
          matchData[match] = compare( match[0], "c1" )
        # window dim: 500 x 300
        # xPos=yPos=50;
        # for target in matchData.keys():
        #   place_img(candidate, xPos, yPos)
        #   shift = -25;
        #   for targetMatch in matchData[target]:
        #     place_img(targetMatch[0], xPos - shift, yPos)
        #     shift += 25;
        #   xPos += 50

      def other():
        # external_method2()
        print "Not implemented"


      load = Label(self, text="Loading...", background="#eee")
      load.grid(row=0,column=0, columnspan=2)

      b2 = Button(self, text="Focus camera", command=other)
      b2.grid(row=1,column=0)
      cb = Button(self, text="Capture Gaze", command=capture)
      cb.grid(row=1,column=1)


      # some kind of hack to bring this window to the front as it is launched. Probably
      #  doesn't work on windows.
      if os.name == "posix":
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

def main():
    root = Tk()
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

