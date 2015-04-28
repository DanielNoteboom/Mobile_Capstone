
from plugin import Plugin
import logging
logger = logging.getLogger(__name__)



class ClickDetect(Plugin):
  def __init__(self, g_pool):
    super(ClickDetect, self).__init__(g_pool)
    self.alive = True
    self.g_pool = g_pool
    self.order = .7
    logger.warning('Init funciton called')
  def on_click(self, pos, button, action):
    logger.warning('Click thing')
  def update(self,frame,events):
  	print type(frame)
  	print frame
  	logger.warning("In update click")
