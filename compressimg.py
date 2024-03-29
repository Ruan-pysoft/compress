import sys, os
import PIL.Image as Image
from shutil import copyfile
from tkinter.filedialog import askdirectory
from tkinter import Tk, Label, Button, Entry, Frame
from datetime import datetime


INPUT = None
OUTPUT = None

def str2jpg(s):
	return '.'.join(s.split('.')[0:-1]) + '.jpg'

#INPUT = os.path.dirname(os.path.realpath(__file__)) + '\\input\\'
#OUTPUT = os.path.dirname(os.path.realpath(__file__)) + '\\output\\'

#Function to compress images
def compress():
    global INPUT #The Input folder
    global OUTPUT #The Outputfolder
    DONE_SOUND = 'done.mp3' #The sound to be played when the image is done being compressed

    log = f'\n{datetime.now().strftime("%d%m%Y %H:%M:%S")}:\n\n' #The log file

    '''if len(sys.argv) > 0:
        playsound = sys.argv[-1]
    else:
        playsound = 'True' '''

    playsound = 'False' #Wether or not the "done" sound should be played

    for r, d, f in os.walk(INPUT):
        for file in f:
            if '.png' in file.lower() or '.jpg' in file.lower():
                if r == INPUT:
                    size = os.path.getsize(os.path.join(INPUT, file))
                    try:
                        img = Image.open(os.path.join(INPUT, file))
                        img.save(os.path.join(OUTPUT, str2jpg(file)), optimize=True, quality=80)
                    except:
                        img = Image.open(os.path.join(INPUT, file)).convert('RGB')
                        img.save(os.path.join(OUTPUT, str2jpg(file)), optimize=True, quality=80)

                    new_size = os.path.getsize(os.path.join(OUTPUT, str2jpg(file)))
                    p = (((new_size/size) * 10000) // 1) / 100
                    print(f'Compressed image {file} from {size//1024}KB to {new_size//1024}KB, now {p}% origional size.')
                    log += f'Compressed image {file} from {size//1024}KB to {new_size//1024}KB, now {p}% origional size.\n'
                    if new_size > size:
                        print('Copied over origional file.')
                        log += 'Copied over origional file.\n'
                        copyfile(os.path.join(INPUT, file), os.path.join(OUTPUT, str2jpg(file)))

    if playsound.lower() != 'false':
        from playsound import playsound
        playsound(DONE_SOUND)
    with open('log.txt', 'a+') as f:
        f.write(log)

root = Tk()

root.title("Image Compression tool")

def def_in():
        global e1
        e1.delete(0, 'end')
        e1.insert(0, askdirectory())

def def_out():
        global e2
        e2.delete(0, 'end')
        e2.insert(0, askdirectory())

def cancel():
        root.destroy()
        sys.exit()

def run():
        global INPUT
        global OUTPUT
        #INPUT = os.path.dirname(os.path.realpath(e1.get()))
        #OUTPUT = os.path.dirname(os.path.realpath(e2.get()))
        INPUT = os.path.join(e1.get())
        OUTPUT = os.path.join(e2.get())
        compress()
	
content = Frame(root)
content.grid(column=0, row=0, sticky='EW')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
content.grid_columnconfigure(0,weight=1)
content.grid_columnconfigure(2,weight=1)

e1 = Entry(content)
e2 = Entry(content)
e1.insert(0, os.path.join('C:\\Users', os.getlogin(), 'Documents\\input'))
e2.insert(0, os.path.join('C:\\Users', os.getlogin(), 'Pictures'))
#e1.insert(0, os.path.dirname(os.path.realpath(__file__)) + '\\input\\')
#e2.insert(0, os.path.dirname(os.path.realpath(__file__)) + '\\output\\')

e1.grid(column=0, row=1, sticky='EW')

e2.grid(column=2, row=1, sticky='EW')

input_btn = Button(content, text="Select an input folder", bg="cyan", command=def_in)
input_btn.grid(column=0, row=0)

_lbl0 = Label(content, text="        ")
_lbl0.grid(column=1, row=0)

output_btn = Button(content, text="Select an output folder", bg="cyan", command=def_out)
output_btn.grid(column=2, row=0)

cancel_btn = Button(content, text="Exit", bg="red", command=cancel)
cancel_btn.grid(column=0, row=2)

run_btn = Button(content, text="Compress", bg="green", command=run)
run_btn.grid(column=2, row=2)

root.mainloop()
