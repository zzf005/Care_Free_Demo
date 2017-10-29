import tkinter as tk
import sys
import cv2
import imutils
import os
import subprocess
import time
time.sleep(1)


class GuessingGame:
        
    def __init__(self, master):

        self.master = master
        master.title("carefree and without worries")
        master.configure(background="#444444")

        thesisStatment = "a carefree-and-without-worries gaming experience"
        photo1 = tk.PhotoImage(file="3.gif")
        self.label1 = tk.Label(master, image=  photo1, height=450,width=800, text = thesisStatment, )
        self.label1.photo1 = photo1
        #vcmd = master.register(self.validate) # we have to wrap the command
        #self.entry = tk.Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        
        # command setting
        def var_states():
            print("male: %d,\n female: %d" % (var1.get(), var2.get()))
        
        
        #(1)MotionDetection Part
        #self.Mvar = tk.IntVar()
        self.MotionD_button = tk.Button(master, activebackground = 'green' ,text="Motion Detect", 
                                        borderwidth= 3,command= self.MotionD_command)#add command 
                                    
        '''                             
        def MotionD(self):
            print ("MotherMode is ", self.Mvar.get())
        self.MotionD_button.state = tk.Label(master, textvariable=self.Mvar).pack()
        '''
        
        #(2) Hear-Rate Parts
        #self.Hvar = tk.IntVar()
        self.heatRate_button = tk.Button(master,activebackground = 'green' ,text="Heart Rate",
                                         borderwidth= 3 ,command= self.heatRate_command)#add command
        
                                              
        #def heatRateState(self, event):
          #  print ("heatRateMode is ", self.Hvar.get())

        
            

        self.label1.grid(row=0, column=0, columnspan=3, sticky = tk.W + tk.E)
        #self.entry.grid(row=1, column=0, columnspan=2, sticky = tk.W + tk.E)
        self.MotionD_button.grid(row=2, column=0,sticky =tk.W + tk.E)
        self.heatRate_button.grid(row=2, column=1,sticky =tk.W + tk.E)
        
        #Show the state

        #camera preview

                
        #Quit
        self.quit = tk.Button(master, text='Quit', command= self.quit_command).grid(row=2,column=2, sticky=tk.E )
    
    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()
            
    def MotionD_command(self):
        #os.system('python motionDetection.py')
        p1 = subprocess.Popen(['python', 'motion_detection.py'],shell = True,stdout=subprocess.PIPE)
        
        
    def heatRate_command(self):
        #os.system('python get_pulse.py')
        p2 = subprocess.Popen(['python', 'get_pulse.py'],shell = True,stdout=subprocess.PIPE)
        
        
    def quit_command(self):
        cv2.destroyAllWindows()
        os._exit(0)
        
        


root = tk.Toplevel()
my_gui = GuessingGame(root)
cv2.destroyAllWindows()
root.mainloop()