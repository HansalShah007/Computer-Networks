import socket
import time

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect(('localhost', 10000))

frames = input('Enter the number of frames to be requested: ')
window_size = input('Enter the size of the window: ')
error = input('Type of scenario (Error-1,Non-error-0): ')

receiver.send(frames.encode('ascii'))
time.sleep(1)
receiver.send(window_size.encode('ascii'))
time.sleep(1)
receiver.send(error.encode('ascii'))

if int(error) == 0:
    for i in range(int(frames)):
        frame = receiver.recv(1024).decode('ascii')
        print("\nFrame no. {} received.".format(frame))

        print("Sending an acknowledgement...")
        receiver.send(frame.encode('ascii'))

else:
    nth_error = input("The error case will be generated for every nth frame. Enter the value of n: ")
    time.sleep(0.5)
    receiver.send(str(nth_error).encode('ascii'))

    frame_status = [False for _ in range(int(frames))]
    nacks = []
    expecting = 1

    while False in frame_status:
        frame = int(receiver.recv(1024).decode('ascii'))
        print("\nFrame no. {} received.".format(frame))
        if frame == expecting:
            print("Sending an acknowledgement...")
            receiver.send(str(frame).encode('ascii'))
            frame_status[int(frame) - 1] = True
            expecting += 1

        elif int(frame) in nacks:
            print("Sending an acknowledgement...")
            receiver.send(str(frame).encode('ascii'))
            frame_status[int(frame) - 1] = True
            nacks.remove(int(frame))

        else:
            print("Accepting frame no. {}".format(frame))
            frame_status[int(frame) - 1] = True

            print("Did not receive frame no. {}".format(expecting))
            print("Sending a negative acknowledgement...")
            nacks.append(expecting)
            receiver.send(str(-1).encode('ascii'))
            expecting = int(frame) + 1
