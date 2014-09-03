import urllib2
import subprocess
import threading
import Queue

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

def displayImage():
	displayProcess = subprocess.Popen(["display", "test.jpg"])

def getScore(imageNo):
	print 'getting score'
	parms="task=score&number=%d&data=0" % (imageNo)
	imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
	line = imageServer.readline()
	return line

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
global running
global history
global currentImage
global displayedImage
currentImage = 1
displayedImage = -1

running = True
inputQueue = Queue.Queue()

input_thread = threading.Thread(target=userInput)
input_thread.start()

while running == True:
	if not(inputQueue.empty()):
		task = inputQueue.get()
		
		if task == 'h':
			displayHistory()
		elif task[0] == 's':
			try:
				if float(task[2:]):
					scoreImage(imageNo, task[2:])
			except:
				print 'input must be a decimal number > 0'	
		elif task == 'p':
			currentImage = (currentImage - 1)%55
		elif task == 'n':
			currentImage = (currentImage + 1)%55
		elif task == 'q':
			running = False
	elif displayedImage != currentImage:
		getImage(currentImage)
		displayImage()
		displayedImage = currentImage
		
	
