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
import tkMessageBox
from ttk import Frame, Style, Button
from ttk import Entry

from gui_helper import take_snapshot, run_pupil


sys.path.insert(0, '..')
from face_comparison.compare import compare
from face_detection.face import facial_detection

COUNT = 0
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
      def insert_img(self, filename, frame, pic_path, label):
        global COUNT
        sizeY = frame.winfo_height()
        sizeX = frame.winfo_width()
        img = Image.open(filename)
        img = img.resize((sizeY, sizeX), Image.ANTIALIAS)
        print "pic_pat " + pic_path
        print "label " + label
        frame.setvar('pic', pic_path)
        frame.setvar('label', label)
        COUNT = COUNT + 1
        # Subtract 8 for various borders in the frame.
        img = img.resize((sizeX-8, sizeY-8), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        lbl1 = Label(frame, image=img)
        lbl1.image = img
        
        lbl1.bind('<Button-1>', save_image)
        lbl1.place(x=frame.winfo_x(), y=frame.winfo_y())

      self.parent.title("Student Name Recollection Helper")
      #self.pack(fill=BOTH, expand=1)

      style = Style()
      style.configure("TButton", padding=(0, 5, 0, 5), 
                      font='serif 10')
      style.configure("TFrame", background="#333")        
      #style.configure("TLabel", background="#333")        

      self.columnconfigure(0,pad=10, minsize=650, weight=1)
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
      def save_image(event):
        print "save_image!!!"
        folder = "../face_comparison/c1/" + event.widget.getvar('label')
        os.system("ls " + folder + " | wc -l > output.txt")
        f = open("output.txt", 'r')
        file_number = f.readline()
        os.system("cp " + event.widget.getvar('pic') + "../face_comparison/c1/" + folder + file_number +".jpg")

      def make_panel(panel_frame):
        ### Panel 1
        p1 = Frame(upper_frame, relief=RAISED, borderwidth =1)
        p1.pack(side = TOP, fill = BOTH, expand=1)

        pic_frame1 = Frame(p1, relief=RAISED, borderwidth =1)
        pic_frame1.pack(side = LEFT, fill = BOTH, expand=1,padx=15, pady=4)
        pic1 = Frame(pic_frame1, relief=RAISED, borderwidth =1)
        pic1.pack(side = TOP, fill = BOTH, expand=1)
        label1 = Label(pic_frame1, relief=RAISED, borderwidth =1, 
            text ="Captured face", width = 15)
        label1.pack(side = BOTTOM, fill = BOTH)

        match_pictures = []
        match_labels = []
        for i in range(3):
          pic_frame = Frame(p1, relief=RAISED, borderwidth =1)
          pic_frame.pack(side = LEFT, fill = BOTH, expand=1,padx=15, pady=4)
          pic = Frame(pic_frame, relief=RAISED, borderwidth =1)
          pic.pack(side = TOP, fill = BOTH, expand=1)
          pic.bind('<Button-1>', save_image)
          match_pictures.append(pic)
          label = Label(pic_frame, relief=RAISED, borderwidth =1, 
              text = "Match %d"%(i+1), width=15)
          label.pack(side = BOTTOM, fill = BOTH)
          match_labels.append(label)

        #  TODO -- delete this? I think we won't use it.
        side_panel1 = Frame(p1, relief=RAISED, borderwidth =1)
        side_panel1.pack(side = RIGHT, fill = BOTH, expand=1)
        bt = Button(side_panel1, text="Confirm\nMatch", command=other)
        bt.pack(pady=10)
        bt = Button(side_panel1, text="Deny\nMatch", command=other)
        bt.pack(pady=10)

        return {"left_pic":pic1, "match_pics":match_pictures, 
                                "match_labels":match_labels}

      #  make 3 panels
      panel_data = []
      panel_data.append( make_panel(upper_frame) )
      panel_data.append( make_panel(upper_frame) )
      panel_data.append( make_panel(upper_frame) )

      def capture():
        coord = []
        if not test_mode:
          pic_file, coord = take_snapshot()
          pic_file = os.path.abspath(pic_file)
        else:
          pic_file = sys.argv[1]
          if len(sys.argv) >= 4:
            coord = [float(sys.argv[2]), float(sys.argv[3])]
          else:
            coord = [0.5,0.5]

        if len(coord) == 0:
          tkMessageBox.showwarning("Error",
                "Pupil player failed to capture gaze.")

        else:
          im=Image.open(pic_file)
          im.size # (width,height) tuple
          coord[0] = int(float(coord[0]) * im.size[0])
          coord[1] = int(float(coord[1]) * im.size[1])
          os.system("cp " + pic_file + " a.jpg")
          faces = facial_detection(pic_file, coord[0], coord[1])
          associated_matches = {}
          if len(faces) == 0:
            tkMessageBox.showwarning("Error",
                "No faces were found.")

          for face in faces:
            associated_matches[face['path']] = compare( face['path'], 
                  "../face_comparison/c1" )
          for index, face in enumerate(faces):
            face_matches = associated_matches[face['path']]
            panel = panel_data[index]
            insert_img(self, face['path'], panel['left_pic'], face['path'], "")
            for j, match in enumerate(face_matches):
              panel['match_labels'][j]['text'] = match['id'].replace('_',' ')
              insert_img(self, match['match_path'], panel['match_pics'][j], face['path'], match['id'])

      def key(event):
        # 'Enter' key triggers capture.
        if event.char == '\r':
          capture()

      # Bind to parent, so that the focus never leaves it. 
      self.parent.focus_set()
      self.parent.bind('<Key>', key)

      ent_msg = Label(self, text="Press Enter to capture gaze.", background="#eee")
      ent_msg.grid(row=1,column=0)
      b2 = Button(self, text="Focus camera", command=other)
      b2.grid(row=1,column=1)

      # Some weird hack to bring this window to the front as it is launched. 
      #  Won't work on windows.
      if os.name == "posix":
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

def exit_function():
  print "I'm in the exit function"
  f = open("../pupil/pupil_src/capture/pic/quit.txt", 'w') 
  f.write("quit")
import atexit
atexit.register(exit_function)
def main():
  root = Tk()
  app = Example(root)
  root.mainloop()  

def removeQuit(): 
  os.system("rm ../pupil/pupil_src/capture/pic/quit.txt")
  os.system("touch ../pupil/pupil_src/capture/pic/quit.txt")
if __name__ == '__main__':
  if len(sys.argv) > 1:
    test_mode = True
  removeQuit()#need to make sure quit file is gone!
  main()  

