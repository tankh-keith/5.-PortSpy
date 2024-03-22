#!/usr/bin/python3

#PREFACE: IMPORT MODULES
import time #to track time taken to finish scan
import socket #to create a virtual communication channel, to attempt reaching specific IPv4 address & its port numbers
import threading #to perform multi-threading and speed up the port scanning process
	#(note: python simulates multi-threading, but does not actually perform it)
from queue import Queue #Queue analogy: List of elements, each element deleted after being 'executed upon', shortening queue



#1. DEFINE USER INPUTS:
print("Welcome to PortSpy™ by Keith Tan!")
targetIP=input("Enter the target IP Address to scan:")
startport=int(input("Enter the lowest port number to scan:"))
endport=int(input("Enter the highest port number to scan:"))
numthreads=int(input("Enter the number of threads to use:"))



#2: DEFINE STORAGES:
queue=Queue() #create empty queue to prepare 'put'-ting in port numbers that user inputs
openports=[] #create empty list to store all open ports, as queue progresses



#3: DEFINE SCANNING OF SINGLE PORT (CHECK IF CONNECTION CAN BE ESTABLISHED - USING SOCKET):
def scanport(targetport): 
	try:
		# socket analogy: virtual communication channel
		# - 'socket.AF_INET' states to use IPv4 only
		# - 'socket.SOCK_STREAM' states to use TCP connection
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((targetIP, targetport)) #attempt to connect to specific IPv4 and port number
		return True #connection is successful (boolean outcome to be used for 'scanner' function)
	except:
		return False #connection is unsuccessful (boolean outcome to be used for 'scanner' function)



#4: 'PUT' PORT NUMBERS INTO QUEUE:
portlist=range(startport,endport)

def fillqueue(portlist):
	for el in portlist:
		queue.put(el) #FIFO: the port 'put' into queue first, will be scanned first
fillqueue(portlist)



#5: 'GET' PORT NUMBERS FROM QUEUE, 'scanport' EACH PORT NUMBER, PRINT PORT NUMBER IF OPEN:
def scanner():
	while not queue.empty(): #while there are elements (yet to be scanned) still in the queue...
		portnum=queue.get() #select the NEXT element from queue (a port number), and assign it to 'port' variable
		if scanport(portnum): #if the function 'scanport(targetport)' is true (aka if the port is OPEN)...
			print(f"Port {portnum} is OPEN.".format(portnum))
			openports.append(portnum) #add the newly-found OPEN port to the 'openports' list



#6: MULTI-THREAD 'scanner' FUNCTION TO SPEED UP SCANS:
threadlist=[]
for el in range(numthreads):
	thread = threading.Thread(target=scanner) #define new 'thread' variable, allow MULTIPLE 'scanner'-s at once
	threadlist.append(thread) #add each 'thread' into the list 'threadlist'



#7: START SCAN, TRACK SCAN TIME, END SCAN:
starttime=time.time() #record start time

for thread in threadlist:
	thread.start() #start the thread (which will execute multiple 'scanner' functions concurrently)
for thread in threadlist:
	thread.join() #wait for ALL threads to complete

endtime=time.time()
elapsed=endtime-starttime



#CONCLUDE: PRINT RESULTS:
print(f"Summary of OPEN Ports: {openports}") #print all OPEN ports
print(f"Scan time: {int(elapsed)} seconds")

