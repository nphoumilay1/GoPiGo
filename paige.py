import time
from math import atan2, pi
from easygopigo3 import EasyGoPiGo3
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit

class Robot:
    def __init__(self):
        self.gpg = EasyGoPiGo3()
        self.imu = InertialMeasurementUnit(bus="GPG3_AD1")
        self.my_servo_portSERVO1 = self.gpg.init_servo('SERVO1')
        self.my_servo_portSERVO2 = self.gpg.init_servo('SERVO2')
        self.my_distance_sensor = self.gpg.init_distance_sensor('I2C')
        self.MAGNETIC_DECLINATION = -5.31
        time.sleep(0.1)
        self.setDefaultSettings()

    def setDefaultSettings(self):
        self.my_servo_portSERVO1.rotate_servo(200)  # Assuming 90 is the center position
        self.my_servo_portSERVO2.rotate_servo(200)  # Assuming 90 is the center position
        self.gpg.set_speed(500)

    def driveUntilObstacle(self):
        while self.my_distance_sensor.read_inches() >= 5:
            self.gpg.forward()
            time.sleep(1)
        self.gpg.stop()
        # No need to set speed here again if it hasn't changed since setDefaultSettings
        while self.my_distance_sensor.read_inches() < 5:
            self.gpg.turn_degrees(90)
            time.sleep(1)
            self.gpg.stop()
            time.sleep(1)
            self.gpg.forward()
            time.sleep(1)
            self.gpg.turn_degrees(-90)
            self.find_north()

    def safe_north_point(self):
        try:
            x, y, z = self.imu.read_magnetometer()
        except Exception as e:
            print(f"Error reading magnetometer: {e}")
            x, y, z = 0, 0, 0

        heading = -atan2(x, -z) * 180 / pi
        if heading < 0:
            heading += 360
        elif heading > 360:
            heading -= 360
        heading += self.MAGNETIC_DECLINATION
        return heading

    def find_north(self):
        heading = self.safe_north_point()
        while heading < -5 or heading > 5:
            if heading < 0:
                self.gpg.turn_degrees(5)
            else:
                self.gpg.turn_degrees(-5)
            heading = self.safe_north_point()
        robot.driveUntilObstacle()
                

# Usage
robot = Robot()
robot.setDefaultSettings()
robot.driveUntilObstacle()
robot.safe_north_point()
robot.find_north()
