#!/usr/bin/env python
# FIT2070 Lab 2 example6.py
import time, os
from threading import *
import threading
import Tkinter 
import urllib2, ImageTk, Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from decimal import *

#initialise events
EvDisplay = Event()
EvInput = Event()
EvSave = Event()
EvDisplayed = Event()

# define the key parameters
SERVER="http://ajhurst.org"
# the URL of the server address
PROGRAM="~ajh/cgi-bin/imageServer.py"

class Display(Thread):
	label = "Display"
	def __init__(self,label):
		Thread.__init__(self)
		self.label = label   
		self.running = True
      
   	def start(self):
   		Thread.start(self)
   		
	def run(self):
		while True:
			#wait for event to be called
			EvDisplay.wait()
			EvDisplay.clear()
			
			#display image here
			global label
			t = Thread(target=self.openWindow)
			score = process2.get_score()
			print score
			t.setDaemon(True)
			t.start()
			print "Something"
			#set event for user input
			EvDisplayed.set()
	
	
	
	def openWindow(self):
		w = Tkinter.Tk()
		im = Image.open('test.jpg')
		tkimg1 = ImageTk.PhotoImage(im)
		label =  Tkinter.Label(w, image=tkimg1)
		#print "Loaded"
		label.pack()
		#w.after(1000, self.update_image)
		w.mainloop()


class userInput(Thread):
	label = "UserInput"
	def __init__(self,label):
		Thread.__init__(self)
		self.label = label   
		self.running = True
      
   	def start(self):
   		Thread.start(self)
      
   	def run(self):
   		"""if os.path.isfile('test.jpg'):
   			print 'already'
   			th2 = threading.Thread(target=self.thread)
   			th2.start()
   			#add prev history 
   		else:"""	
	
		x = ''
		print 'new download'
		num = 24
		tassk = 'image'
		#dat='5.8'
		self.get_image(num)
		
		current = process3.getCurrent()
		history = process3.getHistory()
		
		while True:	
			EvDisplayed.wait()
			EvDisplayed.clear()
			x = raw_input('Enter q to quit: \n') #returns a string prompt
			h = []
			h.append(time.time())
			h.append(num)
			h.append(current)
			h.append(x)
			choice = x.split(" ")
			print "array length " 
			print len(choice)
			print choice
			if len(choice) == 1:
				if x == 'n':
					tassk = 'image'
					print tassk
					print "key n"
					num = self.next_image(num)
					self.get_image(num)
					print "key next"
					#t.display_image(num,tassk,dat)
					#tassk = 'score' #test
					#t.display_image(num,tassk,dat)
				elif x == 'p':
					tassk = 'image'
					print tassk
					print "key p"
					num = self.prev_image(num)
					self.get_image(num)
					print "key prev"
					#t.display_image(num,tassk,dat)
					#tassk = 'score'#test
					#t.display_image(num,tassk,dat)
					
				elif x == 'h':
					h.append("User displayed history.")
					st = '{:^21}'.format("Date/Time") + "|"  + '{:^6}'.format("CurImg") + "|" + '{:>7}'.format("Raw") + "|" + " Description"
					print st
                
               				for line in history:
               					st = '{:^21}'.format(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(line[0]))) + "|" + '{:^6}'.format(line[2]) + "|" + '{:>7}'.format(line[3]) + "|" + line[4] 
                    
                    			print st
                    			evDisplayed.set()
					
					
				elif x =='q':
					print "key q"
					h.append("User quits.")
					history.append(h)
					process3.setCurrent(current)
					process3.setHistory(history)
					#process3.setCurrent(x)
					
					self.running = False
					os._exit(1)
				else:
					print "Error: invalid character"
			elif len(choice) == 2:
				if choice[0] == 's':
					print "first is s"
					if self.is_number(choice[1]):
						sc = float(choice[1])
						if 0 <= sc <= 10.0:
							tassk = 'putscore'
							dat = choice[1]
							self.putscore(num, dat)
							#get putscore 
							
							#t.display_image(num,tassk,dat)
							#print "num =  %s, task = %s, data = %s \n"% (num,tassk,dat)
							#tassk = 'score' #test
							#t.display_image(num,tassk,dat)
							print sc
							print "is a valid range number"
							EvDisplayed.set()
						else:
							print "not in range"
					else:
						print "invalid third"
				else:
					print "invalid second"
			history.append(h)


					
		
	def next_image(self,current):
		return current + 1
	
	def prev_image(self,current):
		return current - 1

	def putscore(self, num, data):
		task='putscore'
		parms="task=%s&number=%d&data=%s" % (task,num,data)
		imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
		
		
	def is_number(self,s):
		try:
			float(s)
			return True
		except ValueError:
			return False

	def get_image(self, number):
		task = 'image'
		parms="task=%s&number=%d" % (task,number)
		imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
		bytes = imageServer.read()
		imageFName = 'test.jpg'
		imageFile = open(imageFName, 'wb')
		for b in bytes:
			imageFile.write(b)
		imageFile.close()
		
		task = 'score'
		parms="task=%s&number=%d" % (task,number)
		imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))
		line = imageServer.readline()
		self.score = float(line.strip())
		
		EvDisplay.set()
		
	def get_score(self):
		return self.score
        	
				
class History(Thread):
	label = "History"
	def __init__(self,label):
		Thread.__init__(self)
		self.label = label
		self.history = []
		self.current = 0
		self.running = True
      
   	def start(self):
   		Thread.start(self)
      
   	def run(self):  	   
   		print "history here"
   		
   	def storeHistory(self):
   		#historydata = [self.history, self.current]
   		#pickle.dump(historydata, open("history.data", "wb"))
   		file = open("newfile.txt", "wb")
   		file.write("")
   		file.close()
   		print "History data has been stored in file."
   		
   	def loadHistory(self):
   		try:
   			historydata = pickle.load(open("history.data", "rb"))
   			self.history = historydata[0]
   			self.current = historydata[1]
   			print "History data has been loaded from file"
		except:
			print "Could not load history data. Please create a new file"
			self.storeHistory()
   	
   	def getHistory(self):
   	 	 return self.history
   	 	 
    	def setHistory(self,new):
    		self.history = new
    		
	def getCurrent(self):
		return self.current
		
        def setCurrent(self,new):
        	self.current = new
   	 
if __name__ == '__main__':
	process1 = Display("Display")
	process2 = userInput("UserInput")
	process3 = History("History")

	process1.start()
	process2.start()
	process3.start()

	process1.join()
	process2.join()
	process3.join()
