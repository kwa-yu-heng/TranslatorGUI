from tkinter import *
from tkinter.ttk import *
import customtkinter
from PIL import ImageTk,Image
from text_localization_en2zh_v3 import en2zh
import datetime
import platform
import cv2
try:
        import winsound
        type='windows'
except:
        import os
        type='other'
window = customtkinter.CTk()
window.title("Clock")
window.geometry('1366x768')
stopwatch_counter_num = 66600
stopwatch_running = False
timer_counter_num = 66600
timer_running = False

#en2zh initialisation
filename='final.jpg'
trans_filename='final_trans.jpg'

def clock():
        date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S/%p")
        date,time1 = date_time.split()
        time2,time3 = time1.split('/')
        hour,minutes,seconds =  time2.split(':')
        if int(hour) > 11 and int(hour) < 24:
                time = str(int(hour) - 12) + ':' + minutes + ':' + seconds + ' ' + time3
        else:
                time = time2 + ' ' + time3
        time_label.config(text = time)
        date_label.config(text= date)
        time_label.after(1000, clock)

#when activated, brings users to 1st tab
def go_to_camera(e):
        tabs_control.select(1)  ##change accordingly to go to camera tab if new tabs added####

#when activated, brings users to main tab
def go_to_clock(e):
        tabs_control.select(0)  ##change accordingly to go to camera tab if new tabs added####

#When activated, go to 2nd tab
def go_to_trans(e):
       tabs_control.select(2)

        


style = Style()
style.layout('TNotebook.Tab', []) # turn off tabs

tabs_control = Notebook(window,style="Tabless.TNotebook") #hiding tab bar
clock_tab = Frame(tabs_control)
clock_tab.pack(fill='both',expand=1)
tabs_control.add(clock_tab, text="Clock")

#alarm_tab = Frame(tabs_control)
#stopwatch_tab = Frame(tabs_control)
#timer_tab = Frame(tabs_control)

camera_tab = Frame(tabs_control)
#tabs_control.add(alarm_tab, text="Alarm")
#tabs_control.add(stopwatch_tab, text='Stopwatch')
#tabs_control.add(timer_tab, text='Timer')
tabs_control.add(camera_tab, text='Camera')
tabs_control.pack(expand = 1, fill ="both")

translated_tab = Frame(tabs_control)
tabs_control.add(translated_tab, text='Camera')
tabs_control.pack(expand = 1, fill ="both")


time_label = Label(clock_tab, font = 'calibri 120 bold', foreground = 'black')
time_label.pack(anchor='center')
date_label = Label(clock_tab, font = 'calibri 120 bold', foreground = 'black')
date_label.pack(anchor='s')


#creating camera button on bottom right corner
camera_icon=ImageTk.PhotoImage(Image.open("camera.png").resize((90,90),Image.Resampling.LANCZOS))
camera_button=Button(clock_tab, text="Camera",image=camera_icon)
camera_button.pack(anchor='se',pady=110)   ###change later to optimise it for lcd screen
camera_button.bind("<Button-1>",go_to_camera)

#back button in camera tab
back_icon=ImageTk.PhotoImage(Image.open("back.png").resize((100,100),Image.Resampling.LANCZOS))
back_button=Button(camera_tab, text="back",image=back_icon)
back_button.grid(row=0,column=0)   ###change later to optimise it for lcd screen
back_button.bind("<Button-1>",go_to_clock)
back_label = Label(camera_tab, font = 'calibri 20', foreground = 'black',text='Back')
back_label.grid(row=0,column=1)
camera_label = Label(camera_tab, font = 'calibri 20 bold', foreground = 'black',text='Camera')
camera_label.grid(row=0,column=2) ###is there a better way to centre camera icon?



###binds double click to go_to_camera function on clock tab#
#Even if you click on the labels############################
clock_tab.bind("<Double-Button-1>",go_to_camera)
time_label.bind("<Double-Button-1>",go_to_camera)
date_label.bind("<Double-Button-1>",go_to_camera)
########################################################

# Create a Label to capture the Video frames
vid_label =Label(camera_tab)
vid_label.grid(row=1, column=2)
cap= cv2.VideoCapture(0)        ######0 for main camera, 1 for webcam

# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   #imgtk = ImageTk.PhotoImage(image = img)
   imgtk = ImageTk.PhotoImage(img.resize((1366,766),Image.Resampling.LANCZOS))
   vid_label.imgtk = imgtk
   vid_label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   vid_label.after(20, show_frames)

#Define function to take picture
def take_picture(e):
    # Get the latest frame and convert into Image
    go_to_trans(e)
    cv2image= cap.read()[1]
    #img_pil = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    #imgtk = ImageTk.PhotoImage(image = img)
    #label.imgtk = imgtk
    #label.configure(image=imgtk)
    #image = np.array(img_pil)
    cv2.imwrite(filename,cv2image) #save written image   
    en2zh(filename,trans_filename)
    img2=ImageTk.PhotoImage(Image.open(trans_filename).resize((1366,766),Image.Resampling.LANCZOS))
    trans_label.configure(image=img2)
    trans_label.image=img2



#Create capture button 
camera_button=Button(camera_tab,text="Camera",image=camera_icon)
camera_button.grid(row=2, column=2)
camera_button.bind("<Button-1>",take_picture)


####Trasnlate tab------------##############
#back button in trans tab
#back_icon=ImageTk.PhotoImage(Image.open("back.png").resize((40,40),Image.Resampling.LANCZOS))
back_button=Button(translated_tab, text="back",image=back_icon)
back_button.grid(row=0,column=0)   ###change later to optimise it for lcd screen
back_button.bind("<Button-1>",go_to_camera)
back_label = Label(translated_tab, font = 'calibri 20', foreground = 'black',text='Back')
back_label.grid(row=0,column=1)
camera_label = Label(translated_tab, font = 'calibri 20 bold', foreground = 'black',text='Translation')
camera_label.grid(row=0,column=2) 

#add translated image into trans tab
img = ImageTk.PhotoImage(Image.open(filename))
# Create a Label Widget to display the text or Image
trans_label = Label(translated_tab, image = img)
trans_label.grid(row=1,column=2)


show_frames()


clock()
window.mainloop()