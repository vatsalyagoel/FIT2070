import urllib2
import subprocess
import threading
import Queue
import time
import os
import platform

class logger():
    def __init__(self):
        self.logFile = 'history.txt'
        self.fileHandle = open(self.logFile, 'a')
        self.logFileLock = threading.Lock()
    def writeLine(self, logLine):
        self.logFileLock.acquire()
        output = "---------Start Current Log-----------\nTimestamp: "+self.timeStamp() + '\n' + str(logLine) + '\n' + "--------End Current Log--------\n"
        self.fileHandle.write(output)
        self.logFileLock.release()
        self.fileHandle.close()
    def timeStamp(self):
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        return stamp
def loggerTimeThread():
	global running
	global out
	counter = 0
	while running:
		timerThread = threading.Thread(target = logTimer(20))
		timerThread.start()
		log = logger()
		log.writeLine(out)
		out=""
def logTimer(delay):
	global stop
	counter = 0
	while running and counter < delay:
		time.sleep(0.5)
		counter +=0.5

def getImage(imageNo):
	print 'downloading image ' + str(imageNo)
	parms="task=image&number=%d&data=0" % (imageNo)
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	bytes=imageServer.read()
	imageFName='test.jpg'
	imageFile=open(imageFName,'wb')
	for b in bytes:
		imageFile.write(b)
	imageFile.close()
	
def displayTimer(delay):
	global stop
	counter = 0
	while not stop and counter < delay:
		time.sleep(0.5)
		counter +=0.5
	stop = False
	global nextImage
	nextImage = (nextImage + 1)%getMax()

	
class displayImageThread(threading.Thread):
	def __init__(self, imageNo):
		threading.Thread.__init__(self)
		self.finish = threading.Event()
		self.imageNo = imageNo
	def run(self):
		if platform.system()=='Linux':
			displayProcess = subprocess.Popen(["display", "test.jpg"])
		elif platform.system()=='Windows':
			displayProcess = subprocess.Popen("start test.jpg", shell=True)
		timerThread = threading.Thread(target = displayTimer(getScore(self.imageNo)))
		timerThread.start()
		displayProcess.kill()

def getScore(imageNo):
	print 'getting score'
	parms="task=score&number=%d&data=0" % (imageNo)
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	line = imageServer.readline()
	print line
	return float(line)
def returnScore(imageNo):
	parms="task=score&number=%d&data=0" % (imageNo)
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	line = imageServer.readline()
	return str(float(line))+"s"
def getMax():
	parms="task=maximum"
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	line = imageServer.readline()
	return int(line)

def scoreImage(imageNo, score):
	print 'updating score'
	parms="task=putscore&number=%d&data=%s" % (imageNo, score)
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	print imageServer.readline()
	
def displayHistory():
	history=open('history.txt', 'r')
	print history.read()
	history.close()
	
def userInput():
	global running
	while running:
		s = raw_input('>')
		inputQueue.put(s)

SERVER="http://ajhurst.org"
PROGRAM="~ajh/cgi-bin/imageServer.py"
global stop
global running
global nextImage
global displayedImage
global displayThread
global out

nextImage = 0
displayedImage = -1

stop = False
running = True

out = ""
inputQueue = Queue.Queue()

userInputThread = threading.Thread(target=userInput)
userInputThread.finish=threading.Event()
userInputThread.start()
logThread = threading.Thread(target=loggerTimeThread)
logThread.finish=threading.Event()
logThread.start()

print platform.system()

while running:
	if not(inputQueue.empty()):
		task = inputQueue.get()
		if task:
			if task == 'h':
				out += "Diplayed history\n"
				displayHistory()
			elif task[0] == 's':
				#try:
				if float(task[2:]):
					print task[2:]
					out += "Scored image "+str(nextImage)+" with value "+ task[2:]+"\n"
					scoreImage(nextImage, task[2:])
				#except:
					#print 'input must be a decimal number > 0'	
			elif task == 'p':
				nextImage = (nextImage - 1)%getMax()
				out += "Displayed previous image\n"
				stop = True
				displayThread.finish.set()
			elif task == 'n':
				out += "Displaying Next Image\n"
				if stop:
					nextImage = (nextImage + 1)%getMax()
				stop = True
				displayThread.finish.set()
			elif task == 'c':
				os.system('clear')
			elif task == 'q':
				out += "Saving Current State and Quitting"
				stop = True
				displayThread.finish.set()
				userInputThread.finish.set()
				logThread.finish.set()
				running = False
				print("press Enter/Return to Quit")
				print("Saving Current State and Quitting")
				break
	elif displayedImage != nextImage:
		getImage(nextImage)
		out +="Displaying image "+str(nextImage)+" for time "+str(returnScore(nextImage))+"\n"
		displayThread = displayImageThread(nextImage)
		displayThread.start()
		displayedImage = nextImage
		
	
