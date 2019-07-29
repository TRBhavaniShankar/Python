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

q1_lock = threading.Semaphore(1)
q2_lock = threading.Semaphore(1)
q3_lock = threading.Semaphore(1)

pickup1 = threading.Semaphore(1)
pickup2 = threading.Semaphore(1)
pickup3 = threading.Semaphore(1)

counter = threading.Lock()
busy1 = False
busy2 = False
busy3 = False

queue_1 = 0
queue_2 = 0
queue_3 = 0
done = 0
counterNonServed = 0

nonservedThread = []
servedThreadTime = []
totalThreadTime = []

def driveThru(myTime):
	
	#delcaring all the global variables inside the function
    global queue_1, queue_2, queue_3
    global totalThreadTime, servedThreadTime
    global done, nonservedThread, counter, counterNonServed
    global lock, pickup1, pickup2,pickup3
    global q1_lock,q2_lock,q2_lock
    global busy1,busy2,busy3
    name = threading.current_thread().getName()

    while True:
        startTime = time.time()
		#inital lock to join the queue, with 20 mins delay
        if lock.acquire(True,(20*scale)):
			#check queue size
            if((queue_1 == 0 and not busy1) or (queue_1 == 1 and (queue_2!=0 or queue_3!=0))):
				#lock to enter queue 1(update the queue value)
                if q1_lock.acquire(False):
                    queue_1 +=1
                    q1_lock.release()
					#lock to enter the check out counter in queue 1
                    if pickup1.acquire(True,999999):
                        #lock to move on to the check out counter(decrement the value of queue as
						#job moves on to checkout)
                        if q1_lock.acquire(False):
                            queue_1 -= 1
                            busy1 = True
                            q1_lock.release()
                            lock.release()
                            servingDuration = time.time()
							#get served in checkout
                            time.sleep(random.uniform(300 * scale, 600 * scale))
                            busy1 = False
                            pickup1.release()
							#lock to count how many customers got served	
                            if counter.acquire():
                                done += 1
                                servedTime = time.time() - servingDuration
                                servedThreadTime.append(servedTime)
                                logging.warning(name + " I billed my items!! Thank you")
                                counter.release()
                                break
			#check queue size
            elif ((queue_2 ==0 and (queue_1==1 or (queue_1==0 and busy1)) and not busy2) or (queue_2 ==0 and queue_1==2 and not busy2)
                  or (queue_2 == 1 and queue_1 == 2 and queue_3!=0)):
				#lock to enter queue 2(update the queue value)  
                if q2_lock.acquire(False):
                    queue_2 += 1
                    q2_lock.release()
					#lock to enter the check out counter in queue 2
                    if pickup2.acquire(True, 999999):
						#lock to move on to the check out counter(decrement the value of queue as
						#job moves on to checkout)
                        if q2_lock.acquire(False):
                            queue_2 -= 1
                            busy2 = True
                            q2_lock.release()
                            lock.release()
                            servingDuration = time.time()
							#get served at checkout
                            time.sleep(random.uniform(300 * scale, 600 * scale))
                            busy2 = False
                            pickup2.release()
							#lock to count the number of customers served
                            if counter.acquire():
                                done += 1
                                servedTime = time.time() - servingDuration
                                servedThreadTime.append(servedTime)
                                logging.warning(name + " I billed my items!! Thank you")
                                counter.release()
                                break
			#check queue size
            elif ((queue_3 ==0 and ((queue_2 !=0 and queue_1!=0) or ((queue_2 ==0 and busy2 and queue_1==0  and busy1))))
                  or (queue_3 ==1 and (queue_1==2 and queue_2==2))):
				#lock to enter queue 3(update the queue value)
                if q3_lock.acquire(False):
                    queue_3 += 1
                    q3_lock.release()
					#lock to enter the check out counter in queue 3
                    if pickup3.acquire(True, 999999):
						#lock to move on to the check out counter(decrement the value of queue as
						#job moves on to checkout)
                        if q3_lock.acquire(False):
                            queue_3 -= 1
                            busy3 = True
                            q3_lock.release()

                            lock.release()
                            servingDuration = time.time()
							#get served at checkout
                            time.sleep(random.uniform(300 * scale, 600 * scale))
                            busy3 = False
                            pickup3.release()
							#lock to count the number of customers served
                            if counter.acquire():
                                done += 1
                                servedTime = time.time() - servingDuration
                                servedThreadTime.append(servedTime)
                                logging.warning(name + " I billed my items!! Thank you ")
                                counter.release()
                                break
        else:
            time.sleep(600*scale)
			#inital lock to join the queue, with 40 mins delay
            if lock.acquire(True, (40 * scale)):
				#check queue size
                if ((queue_1 == 0 and not busy1) or (queue_1 == 1 and (queue_2 != 0 or queue_3 != 0))):
                    # lock to enter queue 1(update the queue value)
                    if q1_lock.acquire(False):
                        queue_1 += 1
                        q1_lock.release()
						#lock to enter the check out counter in queue 1
                        if pickup1.acquire(True, 999999):
							#lock to move on to the check out counter(decrement the value of queue as
							#job moves on to checkout)
                            if q1_lock.acquire(False):
                                queue_1 -= 1
                                busy1 = True
                                q1_lock.release()
                                lock.release()
                                servingDuration = time.time()
								#get served at checkout
                                time.sleep(random.uniform(300 * scale, 600 * scale))
                                busy1 = False
                                pickup1.release()
								#lock to count the number of customers served
                                if counter.acquire():
                                    done += 1
                                    servedTime = time.time() - servingDuration
                                    servedThreadTime.append(servedTime)
                                    logging.warning(name + " I billed my items!! Thank you ")
                                    counter.release()
                                    break
				#check queue size
                elif ((queue_2 == 0 and (queue_1 == 1 or (queue_1 == 0 and busy1)) and not busy2) or (
                        queue_2 == 0 and queue_1 == 2 and not busy2)
                      or (queue_2 == 1 and queue_1 == 2 and queue_3 != 0)):
					#lock to enter queue 1(update the queue value)
                    if q2_lock.acquire(False):
                        queue_2 += 1
                        q2_lock.release()
						#lock to enter the check out counter in queue 2
                        if pickup2.acquire(True, 999999):
							#lock to move on to the check out counter(decrement the value of queue as
							#job moves on to checkout)
                            if q2_lock.acquire(False):
                                queue_2 -= 1
                                busy2 = True
                                q2_lock.release()
                                lock.release()
                                servingDuration = time.time()
								#get served at checkout
                                time.sleep(random.uniform(300 * scale, 600 * scale))
                                busy2 = False
                                pickup2.release()
								#lock to count the number of customers served
                                if counter.acquire():
                                    done += 1
                                    servedTime = time.time() - servingDuration
                                    servedThreadTime.append(servedTime)
                                    logging.warning(name + " I billed my items!! Thank you")
                                    counter.release()
                                    break
				#check queue size
                elif ((queue_3 == 0 and (
                        (queue_2 != 0 and queue_1 != 0) or ((queue_2 == 0 and busy2 and queue_1 == 0 and busy1))))
                      or (queue_3 == 1 and (queue_1 == 2 and queue_2 == 2))):
					#lock to enter queue 1(update the queue value)
                    if q3_lock.acquire(False):
                        queue_3 += 1
                        q3_lock.release()
						#lock to enter the check out counter in queue 3
                        if pickup3.acquire(True, 999999):
							#lock to move on to the check out counter(decrement the value of queue as
							#job moves on to checkout)
                            if q3_lock.acquire(False):
                                queue_3 -= 1
                                busy3 = True
                                q3_lock.release()

                                lock.release()
                                servingDuration = time.time()
								#get served at checkout
                                time.sleep(random.uniform(300 * scale, 600 * scale))
                                busy3 = False
                                pickup3.release()
								#lock to count the number of customers served
                                if counter.acquire():
                                    done += 1
                                    servedTime = time.time() - servingDuration
                                    servedThreadTime.append(servedTime)
                                    logging.warning(name + " I billed my items!! Thank you ")
                                    counter.release()
                                    break
            else:
				#customers who are not served
                no_ServedTime = time.time() - startTime
                nonservedThread.append(no_ServedTime)
                print(name," I waited for very long and did not get served, Im leaving,bye ")
                break

    sys.exit()

threads = []
#creating jobs(customers)
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
