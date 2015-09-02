from scipy.integrate import ode

def f(t, y, *args, **kwargs):
    if 1.0 <= t or t <= 0.0:
        return 0.0
    return t**2

r = ode(f).set_integrator('dopri5')
r.set_initial_value(0.0, -10.0)
t1 = 10
dt = 1
while r.successful() and r.t < t1:
    r.integrate(r.t+dt)
    print("%g %g" % (r.t, r.y))
