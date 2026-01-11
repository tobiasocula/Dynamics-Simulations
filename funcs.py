
import numpy as np
from scipy.integrate import solve_ivp
import scipy.integrate as integrate
from scipy.optimize import brentq
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

def system_solve(func, mu=0.001, x0=0.0, dt=0.01, Tmax=30.0, x_to=None):

    def df(x, h=1e-7):
        return (func(x + h) - func(x - h)) / (2*h)

    def T(t):
        d = df(t)
        denom = np.sqrt(1 + d**2)
        return np.array([1 / denom, d / denom])

    def rhs(state): # state is a tuple (s, v)
        s, v = state
        x_pos = S_inv_interp(s)
        g_tan = np.dot(np.array([0.0, -9.81]), T(x_pos))

        # # Static friction: don't move if gravity too weak
        # mu_s = 0.01  # Static > kinetic
        # if abs(g_tan) < mu_s * 9.81 and abs(v) < 0.001:
        #     return np.array([0.0, 0.0])  # stuck
        
        friction = mu * 9.81 * np.sign(v) + 0.1 * abs(v) * v

        return np.array([v, g_tan - friction])
    
    if x_to is None:
        x_to = x0 + 9.81 * Tmax * Tmax

    xvalues = np.linspace(x0, x_to, 1000)
    dfvalues = np.vectorize(df)(xvalues)
    integrand = np.sqrt(1 + dfvalues * dfvalues)
    svalues = cumulative_trapezoid(integrand, xvalues, initial=0)

    S_inv_interp = interp1d(svalues, xvalues, kind='linear', fill_value='extrapolate')

    state = [0.0, 0.0]

    n_steps = int(Tmax / dt)

    # store result
    # store features: s, v at every timestamp
    result = np.empty((2, n_steps))

    for i in range(n_steps):

        # RK4 step
        k1 = rhs(state)
        k2 = rhs(state + 0.5*dt*k1)
        k3 = rhs(state + 0.5*dt*k2)
        k4 = rhs(state + dt*k3)
        state = state + dt*(k1 + 2*k2 + 2*k3 + k4)/6

        result[:, i] = state
    
    xvalues = S_inv_interp(result[0, :]) # (n_points)
    yvalues = np.vectorize(func)(xvalues) # (n_points)
    slopes = np.vectorize(df)(xvalues) # (n_points)

    return np.stack([
        result[0, :], # s(t) values
        result[1, :], # v(t) values
        xvalues, # x(t) values
        yvalues, # y(t) values
        slopes # slope values (from slope of curve)
        ])

def system_solve_3(func, x0, y0, vx0, vy0, vz0,
                   mu=0.001, Tmax=30, dt=0.1):

    def df_x(x, y, h=1e-7):
        return (func(x + h, y) - func(x - h, y)) / (2*h)
    
    def df_y(x, y, h=1e-7):
        return (func(x, y + h) - func(x, y - h)) / (2*h)
    
    def rhs(state):
        x, y, vx, vy, vz = state

        fx = df_x(x, y)
        fy = df_y(x, y)
        D = 1 + fx*fx + fy*fy

        v_norm = np.sqrt(vx*vx + vy*vy + vz*vz)

        g = 9.81

        ax = -g * fx / D - mu * v_norm * vx
        ay = -g * fy / D - mu * v_norm * vy
        az = -g + g / D - mu * v_norm * vz

        return np.array([vx, vy, ax, ay, az])

    state = np.array([x0, y0, vx0, vy0, vz0])

    n_steps = int(Tmax / dt)

    # store result
    # store features: x, y, vx, vy, vz at every timestamp
    result = np.empty((5, n_steps))

    for i in range(n_steps):

        # RK4 step
        k1 = rhs(state)
        k2 = rhs(state + 0.5*dt*k1)
        k3 = rhs(state + 0.5*dt*k2)
        k4 = rhs(state + dt*k3)
        state = state + dt*(k1 + 2*k2 + 2*k3 + k4)/6

        # projection
        x, y, vx, vy, vz = state

        fx = df_x(x, y)
        fy = df_y(x, y)
        n = np.array([-fx, -fy, 1.0])
        n /= np.linalg.norm(n)

        v = np.array([vx, vy, vz])
        v -= np.dot(v, n) * n

        state = np.array([x, y, v[0], v[1], v[2]])

        result[:, i] = state

    return result