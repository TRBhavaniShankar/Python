import time
import random
import threading
import logging
import sys
logging.basicConfig(format='%(asctime)s %(message)s')

#global variables
scale = 0.0001
total = 0
start = time.time()

lock = threading.Semaphore(6)
pickup = threading.Semaphore(1)
queueLock = threading.Semaphore(1)
counter = threading.Lock()

queue_1 = 0
queue_2 = 0
done = 0
counterNonServed = 0

nonservedThread = []
servedThreadTime = []
totalThreadTime = []

def driveThru(myTime):

	#delcaring all the global variables inside the function
    global queue_1, queueLock, queue_2
    global totalThreadTime, servedThreadTime
    global done, nonservedThread, counter, counterNonServed
    global lock, pickup
    name = threading.current_thread().getName()

    while True:
        startTime = time.time()
		#inital lock to join the queue, with 20 mins delay
        if lock.acquire(True,(20*scale)):
			#check queue size
            if((queue_1 == 0 and queue_2 == 0) or (queue_1 == 0 and queue_2 == 1) or (queue_1 == 0 and queue_2 == 2) or
                (queue_1 == 0 and queue_2 == 3) or (queue_1 == 1 and queue_2 == 1) or (queue_1 == 1 and queue_2 == 2) or
                (queue_1 == 1 and queue_2 == 3) or (queue_1 == 2 and queue_2 == 2) or (queue_1 == 2 and queue_2 == 3)):
                #lock to enter queue 1(update the queue value)
                if queueLock.acquire(False):
                    queue_1 +=1
                    queueLock.release()
					#lock to enter the pick up station
                    if pickup.acquire(True,999999):
						#lock to move on to the pick up counter (to decrement the value on the queue 1)
                        if queueLock.acquire(False):
                            queue_1 -= 1
                            queueLock.release()
                            lock.release()
                            servingDuration = time.time()
							#getting served in the pickup station
                            time.sleep(random.uniform(300 * scale, 600 * scale))
                            pickup.release()
							#count the number of customers served
                            if counter.acquire():
                                done += 1
                                servedTime = time.time() - servingDuration
                                servedThreadTime.append(servedTime)
                                logging.warning(name+" I got the order, Thank you! Bye ")
                                counter.release()
                                break
			#check queue size
            elif ((queue_1 == 3 and queue_2 == 0) or (queue_1 == 2 and queue_2 == 0) or (queue_1 == 1 and queue_2 == 0) or (queue_1 == 3 and queue_2 == 1) or
                  (queue_1 == 2 and queue_2 == 1) or (queue_1 == 3 and queue_2 == 2)):
				#lock to enter queue 2(update the queue value)
                if queueLock.acquire(False):
                    queue_2 += 1
                    queueLock.release()
					#lock to enter the pick up station
                    if pickup.acquire(True, 999999):
						#lock to move on to the pick up counter(to decrement the value on the queue 2)
                        if queueLock.acquire(False):
                            queue_2 -= 1
                            queueLock.release()

                            lock.release()
                            servingDuration = time.time()
							#getting served in the pickup station
                            time.sleep(random.uniform(300 * scale, 600 * scale))
                            pickup.release()
							#count the number of customers served
                            if counter.acquire():
                                done += 1
                                servedTime = time.time() - servingDuration
                                servedThreadTime.append(servedTime)
                                logging.warning(name + " I got the order, Thank you! Bye ")
                                counter.release()
                                break
        else:
            time.sleep(600*scale)
			#inital lock to join the queue, with 40 mins delay
            if lock.acquire(True, (40*scale)):
				#check queue size
                if ((queue_1 == 0 and queue_2 == 0) or (queue_1 == 0 and queue_2 == 1) or (
                        queue_1 == 0 and queue_2 == 2) or
                        (queue_1 == 0 and queue_2 == 3) or (queue_1 == 1 and queue_2 == 1) or (
                                queue_1 == 1 and queue_2 == 2) or
                        (queue_1 == 1 and queue_2 == 3) or (queue_1 == 2 and queue_2 == 2) or (
                                queue_1 == 2 and queue_2 == 3)):
					#lock to enter queue 1(update the queue value)
                    if queueLock.acquire(False):
                        queue_1 += 1
                        queueLock.release()
						#lock to enter the pick up station
                        if pickup.acquire(True, 999999):
							#lock to move on to the pick up counter(to decrement the value on the queue 1)
                            if queueLock.acquire(False):
                                queue_1 -= 1
                                queueLock.release()

                                lock.release()
                                servingDuration = time.time()
								#getting served in the pickup station
                                time.sleep(random.uniform(300 * scale, 600 * scale))
                                pickup.release()
								#count the number of customers served
                                if counter.acquire():
                                    done += 1
                                    servedTime = time.time() - servingDuration
                                    servedThreadTime.append(servedTime)
                                    logging.warning(name+" I got the order, Thank you! Bye ")
                                    counter.release()
                                    break
				#check queue size
                elif ((queue_1 == 3 and queue_2 == 0) or (queue_1 == 2 and queue_2 == 0) or (
                        queue_1 == 1 and queue_2 == 0) or (queue_1 == 3 and queue_2 == 1) or
                      (queue_1 == 2 and queue_2 == 1) or (queue_1 == 3 and queue_2 == 2)):
					#lock to enter queue 1(update the queue value)
                    if queueLock.acquire(False):
                        queue_2 += 1
                        queueLock.release()
						#lock to enter the pick up station
                        if pickup.acquire(True, 999999):
							#lock to move on to the pick up counter(to decrement the value on the queue 2)
                            if queueLock.acquire(False):
                                queue_2 -= 1
                                queueLock.release()

                                lock.release()
                                servingDuration = time.time()
								#getting served in the pickup station
                                time.sleep(random.uniform(300 * scale, 600 * scale))
                                pickup.release()
								#count the number of customers served
                                if counter.acquire():
                                    done += 1
                                    servedTime = time.time() - servingDuration
                                    servedThreadTime.append(servedTime)
                                    logging.warning(name+" I got the order, Thank you! Bye ")
                                    counter.release()
                                    break
            else:
				#count number of customers not served
                no_ServedTime = time.time() - startTime
                nonservedThread.append(no_ServedTime)
                print(name," I waited for very long and did not get served, Im leaving ")
                break

    sys.exit()

threads = []
#create threads
while (total < (14400*scale)):
    time.sleep(random.uniform(50*scale,100*scale))
    myTime = time.time()
    total = myTime - start
    t = threading.Thread(target=driveThru, args = [myTime])
    threads.append(t)
    t.start()

#wait until all the threads finishes
for t in threads:
    t.join()

print("*****************Stats of coustomers*****************")
print(" The total number of customers that arrived : ",len(threads))
print(" The total number of customers served : ",done)
print(" The total number of customers who were forced to leave without being served : ",len(nonservedThread))
avgServedThreadTime = 0
for sThread in servedThreadTime:
    avgServedThreadTime += (sThread*10000)
print(" The average amount of time taken to serve each customer : ",avgServedThreadTime/done,"secs")
