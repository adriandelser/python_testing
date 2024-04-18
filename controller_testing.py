import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

class PIDController:
    def __init__(self, Kp, Ki, Kd, min_output, max_output):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.min_output = min_output
        self.max_output = max_output
        self.cumulative_error = 0
        self.previous_error = 0

    def update(self, error, dt):
    
        # Proportional term
        P = self.Kp * error

        # Integral term
        self.cumulative_error += error * dt
        I = self.Ki * self.cumulative_error

        # Derivative term
        error_rate = (error - self.previous_error) / dt
        D = self.Kd * error_rate

        # Compute the control signal
        control = P + I + D

        # Clamp the output
        control = max(self.min_output, min(control, self.max_output))

        # Update previous error
        self.previous_error = error

        return control

def update_drone_state(x, vx, y, vy, ax, ay, dt):
    # Update position
    x_new = x + vx * dt + 0.5 * ax * dt**2
    y_new = y + vy * dt + 0.5 * ay * dt**2

    # Update velocity
    vx_new = vx + ax * dt
    vy_new = vy + ay * dt

    return x_new, vx_new, y_new, vy_new


# Define a function to update the plot based on the PID gains
def update_plot(Kp, Ki, Kd):
    pid_x = PIDController(Kp, Ki, Kd, min_accel, max_accel)
    pid_y = PIDController(Kp, Ki, Kd, min_accel, max_accel)

    x, vx, y, vy = 0, 0, 0, 0
    all_x, all_y = [x], [y]
    acc_x, acc_y = [0], [0]
    v_x, v_y = [0], [0]
    times = [0]

    for t in range(int(simulation_time / dt)):
        error_x = x_desired - x
        error_y = y_desired - y

        ax = pid_x.update(error_x, dt)
        ay = pid_y.update(error_y, dt)

        x, vx, y, vy = update_drone_state(x, vx, y, vy, ax, ay, dt)
        all_x.append(x)
        all_y.append(y)
        acc_x.append(ax)
        acc_y.append(ay)
        v_x.append(vx)
        v_y.append(vy)
        times.append(t * dt)

    plt.plot(times, all_x)
    plt.title("Drone Path")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.grid()
    plt.show()

# Simulation parameters
dt = 0.01
simulation_time = 30
min_accel, max_accel = -2.0, 2.0
x_desired, y_desired = 10, 10

# Create sliders for PID gains
Kp_slider = widgets.FloatSlider(value=0.5, min=0.1, max=2.0, step=0.1, description='Kp:')
Ki_slider = widgets.FloatSlider(value=0.1, min=0.01, max=0.5, step=0.01, description='Ki:')
Kd_slider = widgets.FloatSlider(value=2.0, min=0.5, max=5.0, step=0.1, description='Kd:')

# Create an interactive widget to update the plot
widgets.interactive(update_plot, Kp=Kp_slider, Ki=Ki_slider, Kd=Kd_slider)

# # Simulation parameters
# dt = 0.01  # Time step
# simulation_time = 30  # Total simulation time in seconds

# # PID parameters and limits
# Kp, Ki, Kd = 0.5, 0.1, 2
# min_accel, max_accel = -2.0, 2.0  # Acceleration limits

# # Initialize PID controllers
# pid_x = PIDController(Kp, Ki, Kd, min_accel, max_accel)
# pid_y = PIDController(Kp, Ki, Kd, min_accel, max_accel)

# # Initial drone state
# x, vx, y, vy = 0, 0, 0, 0

# # Desired position (setpoint)
# x_desired, y_desired = 10, 10

# all_x, all_y = [x], [y]
# acc_x, acc_y = [0], [0]
# v_x, v_y = [0], [0]
# times=[0]
# # Simulation loop
# for t in range(int(simulation_time / dt)):
#     error_x = x_desired - x
#     error_y = y_desired - y

#     ax = pid_x.update(error_x, dt)
#     ay = pid_y.update(error_y, dt)

#     x, vx, y, vy = update_drone_state(x, vx, y, vy, ax, ay, dt)
#     all_x.append(x)
#     all_y.append(y)
#     acc_x.append(ax)
#     acc_y.append(ay)
#     v_x.append(vx)
#     v_y.append(vy)
#     times.append(t*dt)

#     # Optional: Print or log the current state
#     # print(f"Time: {t*dt}, X: {x}, Y: {y}, Vx: {vx}, Vy: {vy}")

# # End of simulation
# # plt.plot(acc_x, acc_y)
# # plt.plot(all_x, all_y)
# # plt.plot(times, v_x)
# plt.plot(times,all_x)
# # plt.plot(x_desired, y_desired, 'ro')
# plt.title("Drone Path")
# plt.xlabel("X Position (m)")
# plt.ylabel("Y Position (m)")
# plt.grid()
# plt.show()