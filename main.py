import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

st.title("Lissajous Figure Plotter")

st.markdown("Enter two functions of time `t` for `x(t)` and `y(t)`.")

# Input functions
x_expr_str = st.text_input("x(t) =", value="sin(3*t)")
y_expr_str = st.text_input("y(t) =", value="sin(4*t + pi/2)")

# Time range and resolution
t_min = st.number_input("Start time", value=0.0)
t_max = st.number_input("End time", value=2*np.pi)
num_points = st.slider("Number of points", 100, 5000, 1000)

# Symbolic variable
t = sp.symbols('t')

try:
    # Parse and lambdify expressions
    x_expr = sp.sympify(x_expr_str)
    y_expr = sp.sympify(y_expr_str)

    x_func = sp.lambdify(t, x_expr, modules=["numpy"])
    y_func = sp.lambdify(t, y_expr, modules=["numpy"])

    # Evaluate
    t_vals = np.linspace(t_min, t_max, num_points)
    x_vals = x_func(t_vals)
    y_vals = y_func(t_vals)

    # Plot
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, color='blue')
    ax.set_title("Lissajous Figure")
    ax.set_xlabel("x(t)")
    ax.set_ylabel("y(t)")
    ax.axis("equal")
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error parsing expressions: {e}")

