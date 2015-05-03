import cv2
from plugin import Plugin
import logging
logger = logging.getLogger(__name__)
import sys
logger.warning("in Plugin file")
count = 0
class ClickDetect(Plugin):
  def __init__(self, g_pool):
    super(ClickDetect, self).__init__(g_pool)
    self.alive = True
    self.g_pool = g_pool
    self.order = .7
    logger.warning('Init funciton called')
  def on_click(self, pos, button,action):
    logger.warning('Click thing')
  def update(self, frame, events):
    global count
   
    cv2.imwrite("pic/pic" + str(count) + ".jpg", frame.img)
    text = open("pic/pic" + str(count) + ".txt", 'w')
    f = open("pic/current_count.txt", 'w')
    f.write(str(count))
    for g in events.get('gaze', []):
      text.write("x " + str(g['norm_pos'][0]) + " y " + str(g['norm_pos'][1]))

    count += 1
