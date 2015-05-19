"""

Initial code take from tutorial on zetcode.com:
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

test_mode = False

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()

    def initUI(self):
      #global test_mode
      if not test_mode:
        run_pupil()

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

      self.columnconfigure(0,pad=10, minsize=350, weight=1)
      self.columnconfigure(1,pad=10)

      self.rowconfigure(0,pad=10, minsize=500, weight=1)
      self.rowconfigure(1,pad=10, weight=1)

      self.pack()

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
        bt = Button(side_panel1, text="Confirm\nMatch", command=other)
        bt.pack(pady=10)
        bt = Button(side_panel1, text="Deny\nMatch", command=other)
        bt.pack(pady=10)

        return {"left_pic":pic1, "right_pic":pic2, "right_label":label2}

      #  make 3 panels
      panel_data = []
      panel_data.append( make_panel(upper_frame) )
      panel_data.append( make_panel(upper_frame) )
      panel_data.append( make_panel(upper_frame) )

      def capture():
        if not test_mode:
          pic_file, coord = take_snapshot()
          pic_file = os.path.abspath(pic_file)
        else:
          pic_file = sys.argv[1]
          if len(sys.argv) >= 4:
            coord = [float(sys.argv[2]), float(sys.argv[3])]
          else:
            coord = [0.5,0.5]

        #pupil player failed
        if len(coord) == 0:


        else:
          im=Image.open(pic_file)
          im.size # (width,height) tuple
          coord[0] = int(float(coord[0]) * im.size[0])
          coord[1] = int(float(coord[1]) * im.size[1])
          os.system("cp " + pic_file + " a.jpg")
          faces = facial_detection(pic_file, coord[0], coord[1])
          associated_matches = {}
          for face in faces:
            associated_matches[face['path']] = compare( face['path'], "../face_comparison/c1" )

          for index, face in enumerate(faces):
            face_matches = associated_matches[face['path']]
            best_match = face_matches[0]
            panel = panel_data[index]
            panel['right_label']['text'] = best_match['id']
            insert_img(self, best_match['match_path'], panel['right_pic'])
            insert_img(self, face['path'], panel['left_pic'])

      def key(event):
        # 'Enter' key triggers capture.
        if event.char == '\r':
          capture()

      # Bind to parent, so that the focus never leaves it. 
      self.parent.focus_set()
      self.parent.bind('<Key>', key)

      b2 = Button(self, text="Focus camera", command=other)
      b2.grid(row=1,column=0)
      cb = Button(self, text="Capture Gaze", command=capture)
      cb.grid(row=1,column=1)


      # Some weird hack to bring this window to the front as it is launched. 
      #  Won't work on windows.
      if os.name == "posix":
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

def exit_function():
  f = open("../pupil/pupil_src/capture/pic/quit.txt", 'w') 
  f.write("quit")
import atexit
atexit.register(exit_function)
def main():
  root = Tk()
  app = Example(root)
  root.mainloop()  

if __name__ == '__main__':
  if len(sys.argv) > 1:
    test_mode = True
  main()  

