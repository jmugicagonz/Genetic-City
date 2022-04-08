import threading
import time

'''
This function will print 5 lines in a loop and sleeps for 1 second after
printing a line.
'''
def threadFunc():
   for i in range(5):
       print('Hello from new Thread ')
       time.sleep(1)

# Create a Thread with a function without any arguments
th = threading.Thread(target=threadFunc)

# Start the thread
th.start()

# Print some messages on console
for i in range(5):
   print('Hi from Main Thread')
   time.sleep(1)
# Wait for thread to finish
th.join()