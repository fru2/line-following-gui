import tkinter
import socket
from time import sleep

host = '192.168.43.3'  # Raspi address
port = 2828
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))


top = tkinter.Tk()

C = tkinter.Canvas(top, bg="white", height=550, width=800)

# rectangle
rect = 50, 50, 500, 500
rect_path = C.create_rectangle(rect, width="2")

# lines
column_1 = 200, 50, 200, 500
column_2 = 350, 50, 350, 500
row_1 = 50, 200, 500, 200
row_2 = 50, 350, 500, 350

column_1_path = C.create_line(column_1, width="2")
column_2_path = C.create_line(column_2, width="2")
row_1_path = C.create_line(row_1, width="2")
row_2_path = C.create_line(row_2, width="2")

# points
point_1_0 = 45, 45, 55, 55
point_2_0 = 195, 45, 205, 55
point_3_0 = 345, 45, 355, 55
point_4_0 = 495, 45, 505, 55

point_1_1 = 45, 195, 55, 205
point_2_1 = 195, 195, 205, 205
point_3_1 = 345, 195, 355, 205
point_4_1 = 495, 195, 505, 205

point_1_2 = 45, 345, 55, 355
point_2_2 = 195, 345, 205, 355
point_3_2 = 345, 345, 355, 355
point_4_2 = 495, 345, 505, 355

point_1_3 = 45, 495, 55, 505
point_2_3 = 195, 495, 205, 505
point_3_3 = 345, 495, 355, 505
point_4_3 = 495, 495, 505, 505

point_1_0_path = C.create_oval(point_1_0, fill="white")
point_2_0_path = C.create_oval(point_2_0, fill="white")
point_3_0_path = C.create_oval(point_3_0, fill="white")
point_4_0_path = C.create_oval(point_4_0, fill="white")

point_1_1_path = C.create_oval(point_1_1, fill="white")
point_2_1_path = C.create_oval(point_2_1, fill="white")
point_3_1_path = C.create_oval(point_3_1, fill="white")
point_4_1_path = C.create_oval(point_4_1, fill="white")

point_1_2_path = C.create_oval(point_1_2, fill="white")
point_2_2_path = C.create_oval(point_2_2, fill="white")
point_3_2_path = C.create_oval(point_3_2, fill="white")
point_4_2_path = C.create_oval(point_4_2, fill="white")

point_1_3_path = C.create_oval(point_1_3, fill="white")
point_2_3_path = C.create_oval(point_2_3, fill="white")
point_3_3_path = C.create_oval(point_3_3, fill="white")
point_4_3_path = C.create_oval(point_4_3, fill="white")

# text
text_coord_0 = 575, 65
bot_orientation = C.create_text(text_coord_0, text="Bot orientation: " + str("northward"), anchor="sw")
text_coord_1 = 575, 95
ir_sensor_reading = C.create_text(text_coord_1, text="Ir sensors reading: " + str([0, 0, 0, 0]), anchor="sw")
text_coord_2 = 575, 125
bot_motion = C.create_text(text_coord_2, text="Bot motion: " + str("Stop"), anchor="sw")


def close_socket():
    sock.close()


def send_str_socket(string):
    command = string
    sock.send(str(command).encode('utf-8'))


def receive_str_socket():
    return sock.recv(1024)


index = 0

while True:
    # txt = input("input text: ")
    incoming = receive_str_socket()

    if index == 128:
        send_str_socket(['forward', 'stop'])
    else:
        send_str_socket("blank")  # write a condition in socket server to ignore blank while accepting other string

    print(incoming.decode('utf-8') + str(index))
    # ir_sensor_reading = C.create_text(text_coord_1, text="Ir sensors reading: " + incoming.decode('utf-8'), anchor="sw")
    C.itemconfig(ir_sensor_reading, text="Ir sensors reading: " + incoming.decode('utf-8'))
    # if txt == "quit":
    #     close_socket()
    #     break
    top.update()
    C.pack()
    top.mainloop(1)
    index += 1
    sleep(0.06)
