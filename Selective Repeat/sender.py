import threading
from threading import *
import socket
import time

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.bind(('localhost', 10000))

sender.listen()
print("Server is listening...")

def selective_repeat(receiver):
    total_frames = int(receiver.recv(1024).decode('ascii'))
    print("\nThe receiver has requested for {} frames".format(total_frames))
    
    window_size = int(receiver.recv(1024).decode('ascii'))
    print("\nThe window size is {}".format(window_size))

    error = int(receiver.recv(1024).decode('ascii'))    
    
    if (error):
        nth_error = int(receiver.recv(1024).decode('ascii'))
        current_frame = 1
        total_frames_sent = 1
        all_received = False
        
        # Initializing the status of the frames
        frame_status = [False for i in range(total_frames+1)]
        frame_status[0] = True

        while False in frame_status:
            if current_frame > total_frames:
                for i in range(1,total_frames+1):
                    if frame_status[i] == False:
                        current_frame = i
                        break
            else:
                    
                if current_frame<=window_size:
                    print("\nSending frame no. {}".format(current_frame))

                    # Generating a scenario where every nth frame is not delivered
                    if total_frames_sent%nth_error!=0:
                        receiver.send(str(current_frame).encode('ascii'))
                        
                        print("Waiting for an acknowledgement...")
                        time.sleep(2)
                        ack = int(receiver.recv(1024).decode('ascii'))
                        
                        if ack!=-1:
                            print("Acknowledgement received for frame no. {}".format(ack))
                            if current_frame==total_frames:
                                all_received = True
                        else:
                            print("Received a negative acknowledgement!")

                        frame_status[current_frame] = True

                    current_frame+=1
                    total_frames_sent+=1
                    
                else:
                    
                    if frame_status[current_frame-window_size]:
                        print("\nSending frame no. {}".format(current_frame))

                        # Generating a scenario where every nth frame is not delivered
                        if total_frames_sent%nth_error!=0:
                            receiver.send(str(current_frame).encode('ascii'))
                            print("Waiting for an acknowledgement...")
                            time.sleep(2)
                            ack = int(receiver.recv(1024).decode('ascii'))
                            
                            if ack!=-1:
                                print("Acknowledgement received for frame no. {}".format(ack))
                                if current_frame==total_frames:
                                    all_received = True
                            else:
                                print("Received a negative acknowledgement!")

                            frame_status[current_frame] = True
                        
                        current_frame += 1
                        total_frames_sent += 1
                    
                    else:
                    
                        print("\nSending frame no. {}".format(current_frame-window_size))

                        # Generating a scenario where every nth frame is not delivered
                        if total_frames_sent%nth_error!=0:
                            receiver.send(str(current_frame-window_size).encode('ascii'))
                            print("Waiting for an acknowledgement...")
                            time.sleep(2)
                            ack = int(receiver.recv(1024).decode('ascii'))
                            
                            if ack!=-1:
                                print("Acknowledgement received for frame no. {}".format(ack))
                            else:
                                print("Received a negative acknowledgement!")
                            frame_status[current_frame - window_size] = True
                        
                        total_frames_sent+=1

    else:
        for i in range(total_frames):
            print("\nSending frame no. {}".format(i + 1))
            receiver.send(str(i + 1).encode('ascii'))
            print("Waiting for an acknowledgement...")
            time.sleep(2)
            try:
                print('Acknowldegment received for frame no. {}'.format(receiver.recv(1024).decode('ascii')))
            except:
                print("Acknowldegement has not been received!")

listening = True
while listening:
    receiver, address = sender.accept()
    print("Receiver "+str(address)+" connected!")

    t = threading.Thread(target=selective_repeat, args=[receiver])
    listening = t.start()
