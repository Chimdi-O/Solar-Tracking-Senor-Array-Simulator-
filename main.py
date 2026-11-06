import matplotlib.pyplot as plt
import numpy as np


class SensorArray(): 
    def __init__(self,sensor_num):
        self.sensor_positions = [ n*180/(sensor_num-1) for n in range(sensor_num)] 

    def track(self,sun_angle): 
        weighted_sum = 0
        sum_ = 0 

        for sensor_angle in self.sensor_positions: 
            weighted_sum += sensor_angle*self.sensor_response(sun_angle,sensor_angle)
            sum_ +=  self.sensor_response(sun_angle,sensor_angle)

        if sum_ == 0: 
            return np.nan
        return weighted_sum/sum_

   
    def sensor_response(self,sun_angle,sensor_angle):
        angle_diff = abs(sun_angle-sensor_angle)
        if angle_diff > 80: 
            return 0

        elif angle_diff > 50: 
            return angle_diff*-0.006667 + 0.5334

        elif angle_diff > 30: 
            return angle_diff*-0.0325 + 1.825

        else: 
            return angle_diff*-0.005 + 1 


class SimulationController(): 
    def __init__(self):  
        self.angle_step = 0.5
        self.angles = [0.5*n for n in range(361)]
        self.measurements = [] 
        
    def run(self,i): 
        self.measurements = []
        current_angle = 0   
        sensor_number = i

        sensor_array = SensorArray(sensor_number) 

        while current_angle <= 180: 
            self.measurements += [sensor_array.track(current_angle)]
            current_angle += self.angle_step

    def calc_max_error(self): 
        max_error = 0 

        for i in range(len(self.angles)): 
            error = abs(self.angles[i] - self.measurements[i])
            if error > max_error: 
                max_error = error 

        return max_error 




sensor_nums = [2,3,4,5,6,7,8,9,10]
errors = [] 

sim = SimulationController() 
plt.plot(sim.angles, sim.angles, "--", label = "Actual (ideal)")

for i in sensor_nums: 
    sim.run(i) 
    errors.append(sim.calc_max_error())
    plt.plot(sim.angles, sim.measurements, label = f"Measured {i}")

print("sensor num error (deg)")
for i in range(len(sensor_nums)): 
    print(f"{sensor_nums[i]}   {errors[i]}")

    
plt.legend() 
plt.xlabel("Sun angle (degrees)")
plt.ylabel("Estimated Sun Angle")
plt.grid()
plt.show()
