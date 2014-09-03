import urllib2
import subprocess
import threading
import Queue
import time

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
	
def timer(delay, killProcess):
	global stop
	counter = 0
	while not stop and counter < delay:
		time.sleep(0.5)
		counter +=0.5
	stop = False
	global currentImage
	currentImage = (currentImage + 1)%56
	#killProcess.finish.set()
"""	
class timerThread(threading.Thread):
	def __init__(self, delay, killProcess):
		threading.Thread.__init__(self)
		self.finish = threading.Event()
		self.delay = delay
		self.killProcess = killProcess
	def run(self):
		counter = 0
		while (counter < delay) and not(self.finish.set()):
			time.sleep(0.5)
			counter +=0.5
		killProcess.finish.set()
		global currentImage
		currentImage = (currentImage + 1)%56
"""		
	
class displayImageThread(threading.Thread):
	def __init__(self, imageNo):
		threading.Thread.__init__(self)
		self.finish = threading.Event()
		self.imageNo = imageNo
	def run(self):
		displayProcess = subprocess.Popen(["display", "test.jpg"])
		timerThread = threading.Thread(target = timer(getScore(self.imageNo), self))
		timerThread.start()
		displayProcess.kill()

def getScore(imageNo):
	print 'getting score'
	parms="task=score&number=%d&data=0" % (imageNo)
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	line = imageServer.readline()
	print line
	return float(line)

def scoreImage(imageNo, score):
	print 'updating score'
	parms="task=putscore&number=%d&data=%s" % (imageNo, score)
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	print imageServer.readline()
	
def displayHistory():
	if not(history.closed()):
		history.close()
	history.open('hist.txt', r)
	print history.read()
	history.close()

def updateHistory(text):
	if history.closed():
		history.open('hist.txt', a)
	history.write(text + '\n')
		
def userInput():
	global running
	while running:
		s = raw_input('>')
		inputQueue.put(s)

SERVER="http://ajhurst.org"
PROGRAM="~ajh/cgi-bin/imageServer.py"
global stop
global running
global history
global currentImage
global displayedImage
global disp
currentImage = 1
displayedImage = -1

stop = False
running = True
inputQueue = Queue.Queue()

userInputThread = threading.Thread(target=userInput)
userInputThread.start()

while running:
	if not(inputQueue.empty()):
		task = inputQueue.get()
		if task:
			if task == 'h':
				displayHistory()
			elif task[0] == 's':
				#try:
				if float(task[2:]):
					print task[2:]
					scoreImage(currentImage, task[2:])
				#except:
					#print 'input must be a decimal number > 0'	
			elif task == 'p':
				currentImage = (displayedImage - 1)%56
				#if displayedImage - currentImage != 1 :
					#currentImage = (currentImage - 1)%56
				stop = True
				#disp.finish.set()
			elif task == 'n':
				currentImage = (displayedImage + 1)%56
				#if currentImage-displayedImage ==2:
					#currentImage = (currentImage - 1)%56
				stop = True
				#disp.finish.set()
			elif task == 'q':
				running = False
				#disp.finish.set()
	elif displayedImage != currentImage:
		getImage(currentImage)
		disp = displayImageThread(currentImage)
		disp.start()
		displayedImage = currentImage
	
		
	
