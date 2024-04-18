#%%
import matplotlib.pyplot as plt
import numpy as np


class PIDController1D:
    def __init__(self, p_gain, i_gain, d_gain, target):
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain
        self.target = target

        self.position = 0.0
        self.error = self.target - self.position
        self.error_integral = 0.0
        self.error_derivative = 0.0

    def update(self, dt):
        # Calculate the error
        error = self.target - self.position
        print(f"Error: {error}")
        # Calculate the integral of the error
        self.error_integral += error * dt
        print(f"Error integral: {self.error_integral}")
        # Calculate the derivative of the error
        self.error_derivative = (error - self.error) / dt
        print(f"Error derivative: {self.error_derivative}")

        # Update the error
        self.error = error

        # Calculate the control output using a PID controller
        output = self.p_gain * self.error + self.i_gain * self.error_integral + self.d_gain * self.error_derivative

        # Update the position
        self.position += output * dt

# Define the PID gains and the target
p_gain = 0.1
i_gain = 0.01
d_gain = 0.1
target = 1.0

# Create the PID controller
pid_controller = PIDController1D(p_gain, i_gain, d_gain, target)

# Run the PID controller and store the results
dt = 0.01
end_time = 50
time = np.arange(0, end_time, dt)
position = np.empty_like(time)

for i in range(len(time)):
    position[i] = pid_controller.position
    pid_controller.update(dt)

# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(time, position, label='Position')
plt.plot(time, np.full_like(time, target), 'r--', label='Target')
plt.xlabel('Time')
plt.ylabel('Position')
plt.legend()
plt.grid(True)
plt.show()

# %%
