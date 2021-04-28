import math as m  # The math module is imported in order to use the trig functions and pi
import numpy as np
import matplotlib.pyplot as plt

def projectile_motion(dt, u, h, x, theta):
    theta *= m.pi / 180  # Theta is converted to radians, as the math.sin and math.cos functions take angles in degrees

    u_y = u * m.sin(theta)  # The initial vertical and horizontal components of velocity are calculated
    u_x = u * m.cos(theta)

    r = np.array([[x], [h]])  # An array is defined to store the x and y coordinates of the projectile at any point in time
    r_dot = np.array([[u_x], [u_y]])  # Another array is defined to store the x and y components of the projectile's velocity at any point in time

    g = 9.8  # The gravitational constant is defined
    i = 0  # A counter variable is initialised

    while r_dot[1] >= 0:  # This loop will continue until the y component of the projectile's velocity is 0, i.e. until the projectile reaches the top of its trajectory
        x += u_x * dt  # The x position is updated for a timestep dt by adding dx, which is defined as dx = u_x * dt
        r[0] = x  # The x coordinate in the r array is also updated to reflect this

        h += u_y * dt  # Similar to the above, the current height and y coordinate in the r array are also updated
        r[1] = h

        u_y -= g * dt  # However, there is an acceleration in the y direction (g), so to account for this the vertical component of velocity is also updated every timestep
        r_dot[1] = u_y  # This change is also done to the vector storing the particle's velocity

        i += 1  # The counter variable is increased by one

    if abs(r_dot[1]) > dt / 2:  # This if statement checks if the currently stored y component of velocity (which should be as close as possible to 0) is greater than half of the timestep. If it is, this means that the closest the y component of velocity gets to 0 is a number greater than 0. If this is the case, all values are restored to the previous iteration by doing the opposite of the previously seen operations.
        x -= u_x * dt
        r[0] = x

        h -= (u_y + g * dt)
        r[1] = h

        u_y += g * dt
        r_dot[1] = u_y

        i -= 1

    t = 2 * i * dt  # The time taken for the projectile to reach apogee is i*dt, but using the symmetry of the parabola traced, the total flight time is found by simply multiplying this result by 2
    h_max = h  # The currently stored h value corresponds to the height when the vertical component of velocity is 0, so it would be the maximum height
    x_max = x * 2  # Once again, the symmetry of the path is used to find the maximum range as the apogee is reached when the projectile is halfway to its maximum horizontal range

    return t, h_max, x_max, i  # The required data is returned by the function

def plot_motion(dt, u, h, x, theta):
    t, h_max, x_max, i = projectile_motion(dt, u, h, x, theta)  # The time, apogee, maximum range and i are found by simply calling the previous function

    theta *= m.pi / 180  # Once again theta has to be converted to find the initial velocities in the x and y directions

    u_y = u * m.sin(theta)
    u_x = u * m.cos(theta)

    r_x = [x]  # Two separate list are defined to hold the x and y coordinates at any point, as well as one for the velocity in the y direction
    r_y = [h]
    v_y = [u_y]

    g = 9.8

    for j in range(1, i * 2):  # Since the number of iterations required is now known, a for loop is set up to append the x,y coordinates and v_y at every timestep between 0 and t
        x += u_x * dt
        r_x.append(x)

        h += u_y * dt
        r_y.append(h)

        u_y -= g * dt
        v_y.append(u_y)

    return r_x, r_y, v_y  # The function then returns all the array

dt = float(input("Please enter the timestep you woulds like to consider in s (using a smaller dt will give a better approximation): "))
u = float(input("Please enter the velocity of the projectile in m/s: "))
h = float(input("Please enter the starting height of the projectile in m: "))
x = float(input("Please enter the starting horizontal displacement in m (most of the time this will be 0): "))
theta = float(input("Please enter the angle of elevation of the projectile in degrees: "))


t, h_max, x_max, i = projectile_motion(dt, u, h, x, theta)

print("\nThe projectile's flight lasts for {0}s.\nDuring this time, it reaches a maximum height of {1}m.\nIts horizontal range is {2}m.".format(round(t, 2), round(h_max, 2), round(x_max, 2)))
print("The motion of the projectile over time is as shown.")

r_x, r_y, v_y = plot_motion(dt, u, h, x, theta)

plt.plot(r_x, r_y, color='red')  # The x position is plotted against the y coordinate
plt.xlabel("Horizantal displacement/m")  # And the axes are labelled
plt.ylabel("Height/m")

plt.show()