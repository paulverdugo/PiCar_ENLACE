# picar servo-install
import keyboard
from Imports.back_wheels import Back_Wheels
from Imports.front_wheels import Front_Wheels
from Imports.camera import Camera

from time import sleep

cam = Camera()
back_wheels= Back_Wheels()
front_wheels=Front_Wheels()
run=True
w=100 # forward speed (1-100)
s=70 # backward speed (1-100)
cam.to_position(90,120)
while run==True:
    try:
        """
        # if no key pressed, controlled by tracker
        if not keyboard.is_pressed("up"or"down"or"left"or"right"or"w"or"a"or"s"or"d"):
            # print("no key pressed")

            scan_count = 0
            while True:
                x = 0             # x initial in the middle
                y = 0             # y initial in the middle
                h = 0             # ball radius initial to 0(no balls if r < ball_size)

                for _ in range(10):
                    (tmp_x,tmp_y),height = tracker()
                    if h > BALL_SIZE_MIN:
                        x = tmp_x
                        y = tmp_y
                        h = height
                        break

                print(x, y, h)

                # scan:
                if r < BALL_SIZE_MIN:
                    bw.stop()
                    if scan_enable:
                        #bw.stop()
                        pan_angle = SCAN_POS[scan_count][0]
                        tilt_angle = SCAN_POS[scan_count][1]
                        if pan_tilt_enable:
                            pan_servo.write(pan_angle)
                            tilt_servo.write(tilt_angle)
                        scan_count += 1
                        if scan_count >= len(SCAN_POS):
                            scan_count = 0
                    else:
                        sleep(0.1)
            
                elif r < BALL_SIZE_MAX:
                    if follow_mode == 0:
                        if abs(x - CENTER_X) > MIDDLE_TOLERANT:
                            if x < CENTER_X:                              # Ball is on left
                                pan_angle += CAMERA_STEP
                                #print("Left   ", )
                                if pan_angle > PAN_ANGLE_MAX:
                                    pan_angle = PAN_ANGLE_MAX
                            else:                                         # Ball is on right
                                pan_angle -= CAMERA_STEP
                                #print("Right  ",)
                                if pan_angle < PAN_ANGLE_MIN:
                                    pan_angle = PAN_ANGLE_MIN
                        if abs(y - CENTER_Y) > MIDDLE_TOLERANT:
                            if y < CENTER_Y :                             # Ball is on top
                                tilt_angle += CAMERA_STEP
                                #print("Top    " )
                                if tilt_angle > TILT_ANGLE_MAX:
                                    tilt_angle = TILT_ANGLE_MAX
                            else:                                         # Ball is on bottom
                                tilt_angle -= CAMERA_STEP
                                #print("Bottom ")
                                if tilt_angle < TILT_ANGLE_MIN:
                                    tilt_angle = TILT_ANGLE_MIN
                    else:
                        delta_x = CENTER_X - x
                        delta_y = CENTER_Y - y
                        #print("x = %s, delta_x = %s" % (x, delta_x))
                        #print("y = %s, delta_y = %s" % (y, delta_y))
                        delta_pan = int(float(CAMERA_X_ANGLE) / SCREEN_WIDTH * delta_x)
                        #print("delta_pan = %s" % delta_pan)
                        pan_angle += delta_pan
                        delta_tilt = int(float(CAMERA_Y_ANGLE) / SCREEN_HIGHT * delta_y)
                        #print("delta_tilt = %s" % delta_tilt)
                        tilt_angle += delta_tilt

                        if pan_angle > PAN_ANGLE_MAX:
                            pan_angle = PAN_ANGLE_MAX
                        elif pan_angle < PAN_ANGLE_MIN:
                            pan_angle = PAN_ANGLE_MIN
                        if tilt_angle > TILT_ANGLE_MAX:
                            tilt_angle = TILT_ANGLE_MAX
                        elif tilt_angle < TILT_ANGLE_MIN:
                            tilt_angle = TILT_ANGLE_MIN
            
                    if pan_tilt_enable:
                        pan_servo.write(pan_angle)
                        tilt_servo.write(tilt_angle)
                    sleep(0.01)
                    fw_angle = 180 - pan_angle
                    if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
                        fw_angle = ((180 - fw_angle) - 90)/2 + 90
                        if front_wheels_enable:
                            fw.turn(fw_angle)
                        if rear_wheels_enable:
                            bw.speed = motor_speed
                            bw.backward()
                    else:
                        if front_wheels_enable:
                            fw.turn(fw_angle)
                        if rear_wheels_enable:
                            bw.speed = motor_speed
                            bw.forward()
        """
        if keyboard.is_pressed("up"):
            cam.turn_up()
        if keyboard.is_pressed("down"):
            cam.turn_down()
        if keyboard.is_pressed("left"):
            cam.turn_left()
        if keyboard.is_pressed("right"):
            cam.turn_right()
            
        if keyboard.is_pressed("w"):
            back_wheels.forward()
            back_wheels.speed = w
        elif keyboard.is_pressed("s"):
            back_wheels.backward()
            back_wheels.speed = s
        else: back_wheels.stop()
        
        if keyboard.is_pressed("a"):
            front_wheels.turn_left()
        elif keyboard.is_pressed("d"):
            front_wheels.turn_right()
        else: front_wheels.turn_straight()
        
    except KeyboardInterrupt:
        cam.to_position(90,120)
        back_wheels.stop()
        front_wheels.turn_straight()
        run=False