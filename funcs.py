
import numpy as np
from scipy.integrate import solve_ivp
import scipy.integrate as integrate
from scipy.optimize import brentq



def system_solve(func, maxdist=10, N_points=100, Tmax=100, mu=0.001, s0=0, v0=0):

    def df(x, h=1e-7):
        return (func(x + h) - func(x - h)) / (2*h)

    def T(t):
        d = df(t)
        denom = np.sqrt(1 + d**2)
        return np.array([1 / denom, d / denom])

    def rhs(t, y):
        s, v = y
        x_pos = S_inv(s)
        g_tan = np.dot(np.array([0.0, -9.81]), T(x_pos))

        #Static friction: don't move if gravity too weak
        mu_s = 0.01  # Static > kinetic
        if abs(g_tan) < mu_s * 9.81 and abs(v) < 0.001:
            return np.array([0.0, 0.0])  # stuck
        
        friction = mu * 9.81 * np.sign(v) + 0.1 * abs(v) * v

        return np.array([v, g_tan - friction])

    def S(u):
        val, _ = integrate.quad(lambda x: np.sqrt(1.0 + df(x)**2), 0.0, u)
        return val
    
    def S_inv(arcl):

        F = lambda m: S(m) - arcl
        return brentq(F, 0, maxdist)

    y0 = [s0, v0]

    longsolve = solve_ivp(rhs, [0, Tmax], [0,0], dense_output=True)
    # s.sol is a 2 x (n_times) array: first row is s, second is v
    # s.t is a (n_times) array (corresp. timestamps)

    t_sample = np.linspace(0, Tmax, 1000)
    s_sample = longsolve.sol(t_sample)[0]  # s at each t_stamp
    T_final = np.interp(maxdist, s_sample, t_sample)

    t_eval = np.linspace(0, T_final, N_points)
    sol = solve_ivp(rhs, np.array([0, T_final]), y0, t_eval=t_eval, method='LSODA')

    s_inv_vect = np.vectorize(S_inv)
    f_vect = np.vectorize(func)
    f_vect_deriv = np.vectorize(df)
    
    intermed = s_inv_vect(sol.y[0, :]) # (n_points)
    f_last = f_vect(intermed) # (n_points)
    slopes = f_vect_deriv(intermed) # (n_points)

    # testing code for error estimation (used in debugging etc)

    # s_test = np.linspace(0, maxdist, 20)
    # x_test = s_inv_vect(s_test)
    # s_recovered = np.array([S(xx) for xx in x_test])
    # error = np.max(np.abs(s_recovered - s_test))
    # print("S_inv error:", error)  # Should be <1e-8

    return np.stack([
        sol.t, # time values
        sol.y[0], # s(t) values
        sol.y[1], # v(t) values
        intermed, # x(t) values (first component)
        f_last, # x(t) values (second component)
        slopes # slope values (from slope of curve)
        ])