"""

Based on tutorial on zetcode.com:
zetcode.com/gui/tkinter/layout/

"""
import os
import time

import sys

from PIL import Image, ImageTk
from Tkinter import Tk, N,S,W,E, Label, BOTH, RIGHT, RAISED, LEFT
from Tkinter import TOP, BOTTOM
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

    def initUI(self):
      #run_pupil()

      #  Defining a method for absolute positioning of an image
      def place_img(self, filename, x, y):
        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        lbl1 = Label(self, image=img)
        lbl1.image = img
        lbl1.place(x=x, y=y)

      #  Defining a method for framewise positioning of an image
      # @params
      #   frame   the frame to attach filename to
      def insert_img(self, filename, frame):
        sizeY = frame.winfo_height()
        sizeX = frame.winfo_width()
        img = Image.open(filename)
        img = img.resize((sizeY, sizeX), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        lbl1 = Label(frame, image=img)
        lbl1.image = img
        lbl1.place(x=frame.winfo_x(), y=frame.winfo_y())

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
        pic_file = os.path.abspath(pic_file)
        im=Image.open(pic_file)
        im.size # (width,height) tuple
        coord[1] = int(float(coord[1]) * im.size[0])
        coord[3] = int(float(coord[3]) * im.size[1])
        print coord
        os.system("cp " + pic_file + " a.jpg")
        matches = facial_detection(pic_file, coord[1], coord[3])
        matchData = {}
        print "matches"
        print matches
        for match in matches:
          matchData[match] = compare( match[0], "../face_comparison/c1" )
        # window dim: 500 x 300
        xPos=yPos=50;
        for target in matchData.keys():
          place_img(candidate, xPos, yPos)
          shift = -25;
          for targetMatch in matchData[target]:
            place_img(targetMatch[0], xPos - shift, yPos)
            shift += 25;
          xPos += 50

      def other():
        # external_method2()
        print "Not implemented"

      # Top box
      upper_frame = Frame(self, relief=RAISED )
      upper_frame.grid(row = 0, column = 0, columnspan=2, sticky=N+E+S+W)

      # Creates a panel in the frame passed in, and returns a list of frame objects
      #  that need to be accessed in the panel
      def make_panel(panel_frame):
        ### Panel 1
        p1 = Frame(upper_frame, relief=RAISED, borderwidth =1)
        p1.pack(side = TOP, fill = BOTH, expand=1)

        pic_frame1 = Frame(p1, relief=RAISED, borderwidth =1)
        pic_frame1.pack(side = LEFT, fill = BOTH, expand=1,padx=15, pady=4)
        pic1 = Frame(pic_frame1, relief=RAISED, borderwidth =1)
        pic1.pack(side = TOP, fill = BOTH, expand=1)
        label1 = Label(pic_frame1, relief=RAISED, borderwidth =1, text = "Captured face")
        label1.pack(side = BOTTOM, fill = BOTH)

        pic_frame2 = Frame(p1, relief=RAISED, borderwidth =1)
        pic_frame2.pack(side = LEFT, fill = BOTH, expand=1,padx=15, pady=4)
        pic2 = Frame(pic_frame2, relief=RAISED, borderwidth =1)
        pic2.pack(side = TOP, fill = BOTH, expand=1)
        label2 = Label(pic_frame2, relief=RAISED, borderwidth =1, text = "Best match")
        label2.pack(side = BOTTOM, fill = BOTH)

        side_panel1 = Frame(p1, relief=RAISED, borderwidth =1)
        side_panel1.pack(side = RIGHT, fill = BOTH, expand=1)

        return [pic1, pic2]

      #  make 3 panels

      (p1_1, p1_2) = make_panel(upper_frame)
      (p2_1, p2_2) = make_panel(upper_frame)
      (p3_1, p3_2) = make_panel(upper_frame)

      #  TODO -- replace my fake capture method with this one
      #def capture():
      #  pic_file, coord = take_snapshot()
      #  pic_file = os.path.abspath(pic_file)
      #  im=Image.open(pic_file)
      #  im.size # (width,height) tuple
      #  coord[1] = int(float(coord[1]) * im.size[0])
      #  coord[3] = int(float(coord[3]) * im.size[1])
      #  print coord
      #  os.system("cp " + pic_file + " a.jpg")
      #  matches = facial_detection(pic_file, coord[1], coord[3])
      #  matchData = {}
      #  for match in matches:
      #    matchData[match] = compare( match[0], "../face_comparison/c1" )
      #  # window dim: 500 x 300
      #  xPos=yPos=50;
      #  for target in matchData.keys():
      #    place_img(candidate, xPos, yPos)
      #    shift = -25;
      #    for targetMatch in matchData[target]:
      #      place_img(targetMatch[0], xPos - shift, yPos)
      #      shift += 25;
      #    xPos += 50

      def capture():
        insert_img(self, "img1.jpg",p1_1)
        insert_img(self, "img2.jpg",p2_1)
        insert_img(self, "img3.jpg",p3_1)
        insert_img(self, "img1.jpg",p2_2)
        insert_img(self, "img2.jpg",p3_2)
        insert_img(self, "img3.jpg",p1_2)
        

      b2 = Button(self, text="Focus camera", command=other)
      b2.grid(row=1,column=0)
      cb = Button(self, text="Capture Gaze", command=capture)
      cb.grid(row=1,column=1)


      # Some kind of hack to bring this window to the front as it is launched. 
      #  Won't work on windows.
      if os.name == "posix":
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

def main():
    root = Tk()
    app = Example(root)
    root.mainloop()  

if __name__ == '__main__':
    main()  

