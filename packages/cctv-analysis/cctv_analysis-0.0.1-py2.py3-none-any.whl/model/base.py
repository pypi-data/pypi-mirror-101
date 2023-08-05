import abc 
#import cv2  
  
class BaseModel(abc.ABC):
  
  @abc.abstractmethod
  def analyze_frame(self,frame):
    pass
  def analyze_video(self,video_path):
    pass



