from PIL import Image
import urllib2
import subprocess
import time
import threading 
import thread
import Queue

def getImage(ImageNumber):  
    print 'downloading image'
    task='image'
    parms="task=%s&number=%d&data=%s" % (task,ImageNumber,data)
    imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
    bytes=imageServer.read()
    imageFName='test.jpg'
    imageFile=open(imageFName,'wb') # handle binary writes, esp. in Win32
    for b in bytes:
        imageFile.write(b)
    imageFile.close()
    
def getScore(ImageNumber):
    # print the return score (first line of file)
    task='score'
    parms="task=%s&number=%d&data=%s" % (task,ImageNumber,data)
    imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
    line = imageServer.readline()
    return line

def DisplayImage(ImageNumber):
    getImage(ImageNumber)
    displayProcess = subprocess.Popen(["display", "test.jpg"])
    delay = getScore(ImageNumber)
    print delay
    t = threading.Timer(float(getScore(ImageNumber)), NextImage,( ))
    t.start()
    thisImage = ImageNumber
    while(t.isAlive()):
        if thisImage != getCurrentImageNumber():
            displayProcess.kill()
            t.cancel()
        

    

def readInput():#gets textual input from the user, saves it to inputQueue
    while running:
        s = raw_input('>')
        inputQueue.put(s)
        
def NextImage():
    print 'next image'
    global currnetImage
    currnetImage = (currnetImage + 1) % 55
    
def PrevImage():
    print 'previous image'
    global currnetImage
    currnetImage = (currnetImage - 1) % 55
    
def getCurrentImageNumber():
    global currnetImage
    return currnetImage
    
threadLock = threading.Lock()
SERVER="http://ajhurst.org"
PROGRAM="~ajh/cgi-bin/imageServer.py"
data = 5.0
global currentImage
currnetImage = 1
DisplayImage(currnetImage)
displayedImage = 1



running = True
inputQueue = Queue.Queue()

input_thread = threading.Thread(target=readInput)
input_thread.start()



while running:
    if not(inputQueue.empty()):
        task = inputQueue.get()
        if task == 'h':#display history
            pass
        elif task == 'p':#previous image
            print 'previous'
            thread.start_new_thread(PrevImage,( ))
        elif task == 'n':#next image
            print 'next'
            thread.start_new_thread(NextImage,( ))
            
    elif displayedImage != currnetImage:
        displayedImage = currnetImage
        thread.start_new_thread(DisplayImage,(currnetImage, ))
