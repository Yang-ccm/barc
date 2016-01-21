from input_map import angle_2_servo, servo_2_angle
from numpy import sin, cos, pi

# simple test setting class
class TestSettings:
	def __init__(self, SPD = 95, L_turn = 5, R_turn = -5, dt = 10):
		# PWN signal values for motor
		self.speed 		= SPD
		self.neutral 	= 90
		self.stopped 	= False
		self.brake 		= 50
		self.dt_man 	= dt   	# duration of manuever

		# check valid speed
		if SPD < 90 or SPD > 130:
			self.speed = 95

		# check valid turns 
		# left is positive, right is negative
		if L_turn < 0 or L_turn > 30:
			L_turn = 5
		if R_turn > 0 or R_turn < -30:
			R_turn = -5

		# PWN signal values for servo
		self.L_turn 	= angle_2_servo(L_turn)		# left turn
		self.R_turn 	= angle_2_servo(R_turn)		# right turn
		self.Z_turn 	= 90 						# zero (no) turn


#############################################################
def CircularTest(test_opt, rate, t_i):
    oneSec 		= rate
    t_0         = 5*oneSec
    t_f         = t_0 + (test_opt.dt_man)*oneSec

    # do nothing initially
    if (t_i < t_0):
        motorCMD        = test_opt.neutral
        servoCMD         = test_opt.Z_turn

    # turn left and move
    elif (t_i >= t_0) and (t_i <= t_f):
        servoCMD     = test_opt.L_turn
        motorCMD    = test_opt.speed

    # set straight and stop
    else:
        servoCMD     	= test_opt.Z_turn
        motorCMD        = test_opt.neutral
        if not test_opt.stopped:
            motorCMD    	 = test_opt.brake
            test_opt.stopped = True

    return (motorCMD, servoCMD)


#############################################################
def Straight(test_opt, rate, t_i):
    # timing maneuvers
    oneSec      = rate
    dt          = 10*oneSec 
    t_0         = 5*oneSec
    t_f         = t_0 + dt

    # rest
    if t_i < t_0:
        servoCMD     = test_opt.Z_turn
        motorCMD    = test_opt.neutral

    # start moving
    elif (t_i >= t_0) and (t_i < t_f):
        servoCMD     = test_opt.Z_turn
        motorCMD    = test_opt.speed

    # set straight and stop
    else:
        servoCMD     	= test_opt.Z_turn
        motorCMD        = test_opt.neutral
        if not test_opt.stopped:
            motorCMD    	 = test_opt.brake
	

    return (motorCMD, servoCMD)

#############################################################
def SineSweep(test_opt, rate, t_i):
    # timing maneuvers
    oneSec      	= rate
    dt          	= 2.5*oneSec 
    t_0         	= 5*oneSec
    start_turning 	= 1*oneSec
    t_st         	= t_0+start_turning
    t_f         	= t_0 + dt +start_turning
    T           	= 1.2*oneSec

    # rest
    if t_i < t_0:
        servoCMD     = test_opt.Z_turn
        motorCMD    = test_opt.neutral
	
	# move forward
    elif  (t_i >= t_0) and (t_i < t_st):
        servoCMD     = test_opt.Z_turn
        motorCMD    = test_opt.speed

	# move in sine wave motion
    elif  (t_i >= t_st) and (t_i < t_f):
        servoCMD     = angle_2_servo(25*sin(2*pi*(t_i-t_0)/float(T)))
        motorCMD    = test_opt.speed

    # set straight and stop
    else:
        servoCMD     	= test_opt.Z_turn
        motorCMD        = test_opt.neutral
        if not test_opt.stopped:
            motorCMD    	 = test_opt.brake

    return (motorCMD, servoCMD)

#############################################################
def DoubleLaneChange(test_opt, rate, t_i):
    # timing maneuvers
    oneSec      = rate
    dt          = 3*oneSec 
    t_0         = 5*oneSec
    t_LT        = t_0 + dt
    t_RT        = t_LT + dt
    t_ZT        = t_RT + dt
    t_f         = t_ZT + dt

    # start moving
    if t_i < t_0:
        servoCMD     = test_opt.Z_turn
        motorCMD    = test_opt.speed

    # turn left
    elif (t_i >= t_0) and (t_i < t_LT):
        servoCMD     = test_opt.L_turn
        motorCMD    = test_opt.speed

    # turn right
    elif (t_i >= t_LT) and (t_i < t_RT):
        servoCMD     = test_opt.R_turn
        motorCMD    = test_opt.speed

    # go straight
    elif (t_i >= t_RT) and (t_i < t_ZT):
        servoCMD     = test_opt.Z_turn
        motorCMD    = test_opt.speed

    # set straight and stop
    else:
        servoCMD     	= test_opt.Z_turn
        motorCMD        = test_opt.neutral
        if not test_opt.stopped:
            motorCMD    	 = test_opt.brake

    return (motorCMD, servoCMD)
