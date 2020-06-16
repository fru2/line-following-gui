from gpiozero import LineSensor
import RPi.GPIO as gpio
import socket
from time import sleep

#socket init
sock = socket.socket()
port = 2828         
sock.bind(('', port))
sock.listen(5)
c, addr = sock.accept() 
print(addr)

#GPIO inits -----------------------------------------------------------------------------------------------
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

#ir sensors
left_most_sensor = LineSensor(5)
left_sensor = LineSensor(6)
center_sensor = LineSensor(13)
right_sensor = LineSensor(19)
right_most_sensor = LineSensor(26)
near_sensor = LineSensor(16)



#left motor conf
ena = 17
left_motor_forward = 27
left_motor_backward = 22

gpio.setup(ena, gpio.OUT)
gpio.setup(left_motor_forward, gpio.OUT)
gpio.setup(left_motor_backward, gpio.OUT)

#right motor conf
enb = 18
right_motor_forward = 23
right_motor_backward = 24

gpio.setup(enb, gpio.OUT)
gpio.setup(right_motor_forward, gpio.OUT)
gpio.setup(right_motor_backward, gpio.OUT)

#speed conf
pwm1 = gpio.PWM(ena, 100)
left_motor_speed = 45 # %
pwm1.start(left_motor_speed)

pwm2 = gpio.PWM(enb, 100)
right_motor_speed = 45 # %
pwm2.start(right_motor_speed)

# ---------------------------------------------------------------------------------------------------------

#bot controls
def left_sharp_turn():
	gpio.output(left_motor_forward, 0)
	gpio.output(left_motor_backward, 1)
	gpio.output(right_motor_forward, 1)
	gpio.output(right_motor_backward, 0)
def left_turn():
	gpio.output(left_motor_forward, 0)
	gpio.output(left_motor_backward, 0)
	gpio.output(right_motor_forward, 1)
	gpio.output(right_motor_backward, 0)
def right_turn():
	gpio.output(left_motor_forward, 1)
	gpio.output(left_motor_backward, 0)
	gpio.output(right_motor_forward, 0)
	gpio.output(right_motor_backward, 0)
def right_sharp_turn():
	gpio.output(left_motor_forward, 1)
	gpio.output(left_motor_backward, 0)
	gpio.output(right_motor_forward, 0)
	gpio.output(right_motor_backward, 1)
def forward():
	gpio.output(left_motor_forward, 1)
	gpio.output(left_motor_backward, 0)
	gpio.output(right_motor_forward, 1)
	gpio.output(right_motor_backward, 1)
def uturn():
	gpio.output(left_motor_forward, 0)
	gpio.output(left_motor_backward, 1)
	gpio.output(right_motor_forward, 0)
	gpio.output(right_motor_backward, 1)
	sleep(1)
	right_sharp_turn()
def stop():
	gpio.output(left_motor_forward, 0)
	gpio.output(left_motor_backward, 0)
	gpio.output(right_motor_forward, 0)
	gpio.output(right_motor_backward, 0)
	
	
def follow_line():
	if (center_sensor == 0 and left_sensor == 1 and right_sensor == 1):
		forward()
	elif (left_sensor == 0 and center_sensor == 1 and right_sensor == 1):
		left()
		print('left')
	elif (right_sensor == 0 and center_sensor == 1 and left_sensor == 1):
		print('right')
		right()
	
		
	
def socket_send(string):
	send_this = str(string)
	s.send(send_this.encode('utf-8'))

directions_array = []
index = 1
    
while True:
	
	#is_cross_section = ((left_most_sensor.value == 0) and (left_sensor.value == 0) and (center_sensor.value == 0) and (right_sensor.value == 0) and (right_most_sensor.value == 0))
	
	#Socket communication	
	ir_sensor_reading = [left_most_sensor.value, left_sensor.value, center_sensor.value, right_sensor.value, right_most_sensor.value]
	c.send(str(ir_sensor_reading).encode('utf-8'))
	#Socket closed
	
	incoming = c.recv(1024)
	incoming_str = incoming.decode('utf-8')
	
	if incoming_str != "blank":
		directions = incoming_str
		replacable_str = "[]' "
		for i in replacable_str:
			directions = directions.replace(i, "")
		directions = directions.split(',') # Creates an array of incoming string splitted by comma
		directions_array = directions
	
	if len(directions_array) != 0:
		while directions_array[0] == "forward":
			is_cross_section = ((left_most_sensor.value == 0) and (left_sensor.value == 0) and (center_sensor.value == 0) and (right_sensor.value == 0) and (right_most_sensor.value == 0))
			print('forward')
			forward()
			if (is_cross_section):
				print('cross_section')
				if (directions_array[index] == "forward"):
					print('forward')
					forward()
				elif (directions_array[index] == "left"):
					print('left')
					left_sharp_turn()
				elif (directions_array[index] == "right"):
					print('right')
					right_sharp_turn()
				elif (directions_array[index] == "uturn"):
					print('uturn')
					uturn()
				elif (directions_array[index] == "stop"):
					print('stop')
					stop()
					index = 1
					directions_array = [] # set null so that it could not move again
					break
				index += 1
			follow_line()
	sleep(0.06)


	
