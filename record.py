import threading
import tkinter as tk
import cv2
from collections import deque
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
e = threading.Event()
pr = None
pw = None
# -------begin capturing and saving video
def startrecording(e,queue,out,cap):

    while(cap.isOpened()):
        if e.is_set():
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            e.clear()
        ret, frame = cap.read()
        if ret==True:
            queue.append(frame)
        else:
            break
            
def startwriting(e,queue,out,cap):
    while not e.is_set():
        if queue:
            out.write(queue.popleft())

def startinitialising(e,cap):
    while not e.is_set():
        if queue:
            out.write(queue.popleft())
            
def start_recording_proc():
    queue = deque()
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))
    global pr
    pw = threading.Thread(target=startwriting, args=(e,queue,out,cap))
    pr = threading.Thread(target=startrecording, args=(e,queue,out,cap))
    pw.start()
    pr.start()

# -------end video capture and stop tk
def stoprecording():
    e.set()
    root.quit()
    root.destroy()

if __name__ == "__main__":

    # -------configure window
    root = tk.Tk()
    root.geometry("%dx%d+0+0" % (100, 100))
    startbutton=tk.Button(root,width=10,height=1,text='START',command=start_recording_proc)
    stopbutton=tk.Button(root,width=10,height=1,text='STOP', command=stoprecording)
    startbutton.pack()
    stopbutton.pack()

    # -------begin
    root.mainloop()
    for i in range(0,100):
        print(i)
    cv2.destroyAllWindows()
    
    
