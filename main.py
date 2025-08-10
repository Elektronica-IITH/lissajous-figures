import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from st_social_media_links import SocialMediaIcons
import random

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Lissajous Generator", layout="wide")
st.logo("elektronica.png", size="large")

# ---------- SOCIAL LINKS ----------
social_media_links = [
    "https://www.linkedin.com/company/elektronica-iit-hyderabad/",
    "https://github.com/Elektronica-IITH",
    "https://www.instagram.com/elektronica_iith/",
]
social_media_icons = SocialMediaIcons(social_media_links)

# ---------- MATPLOTLIB SETTINGS ----------
plt.rcParams.update({
    "axes.facecolor": "none",
    "figure.facecolor": "none",
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "none",
    "text.color": "white",
    "axes.titlecolor": "white",
})

plotcolor = 'dodgerblue'

# ---------- TITLE & HEADER ----------
title_col, tip_col = st.columns([3, 1])

with title_col:
    st.title("Elektronica IITH")
    st.header("Lissajous Figure Generator")

with tip_col:
    if "tip_index" not in st.session_state:
        st.session_state.tip_index = 0

    tips = [
        "Lissajous figures are created by plotting two signals: x(t) vs y(t).",
        "Changing the frequency ratio changes the pattern complexity!",
        "Phase shifts create loops or rotations in the pattern.",
        "Try 'Square' or 'Sawtooth' waves for edgy, unique figures!",
        "See those ripples in x(t) and y(t) when you reduce number of points? Check out [Aliasing](https://en.wikipedia.org/wiki/Aliasing)"
    ]

    if st.button("🔁 Show Tip"):
        st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)

    st.info(tips[st.session_state.tip_index])

# ---------- WAVEFORM FUNCTION ----------
def waveform_function(name, t, freq, amp, phase, expr=None):
    omega_t = 2 * np.pi * freq * t + phase/180*np.pi
    if name == "Sine":
        return amp * np.sin(omega_t)
    elif name == "Cosine":
        return amp * np.cos(omega_t)
    elif name == "Square":
        return amp * signal.square(omega_t)
    elif name == "Triangle":
        return amp * signal.sawtooth(omega_t, width=0.5)
    elif name == "Sawtooth":
        return amp * signal.sawtooth(omega_t)
    elif name == "Arbitrary" and expr is not None:
        try:
            return eval(expr)
        except Exception as e:
            st.error(f"Invalid expression: {e}")
            return np.zeros_like(t)
    else:
        return np.zeros_like(t)

# ---------- GLOBAL SETTINGS ----------
t_max_default = 4 * np.pi
num_points_default = 1000

# ---------- CONTROLS ----------
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)

with ctrl_col1:
    st.subheader("🔵 x(t) Settings")
    x_wave = st.selectbox("Waveform", ["Sine", "Cosine", "Square", "Triangle", "Sawtooth", "Arbitrary"], index=0, key="x_wave")
    if x_wave == "Arbitrary":
        x_expr = st.text_input("Enter expression using 't' (e.g., np.sin(3*t))", key="x_expr")
    else:
        x_freq = st.slider("Frequency", 1, 20, 1, key="x_freq")
        x_amp = st.slider("Amplitude", 0.1, 5.0, 1.0, key="x_amp")
        x_phase = st.slider("Phase (in theta)", 0, 360, 0, key="x_phase")

with ctrl_col2:
    st.subheader("🟢 y(t) Settings")
    y_wave = st.selectbox("Waveform", ["Sine", "Cosine", "Square", "Triangle", "Sawtooth", "Arbitrary"], index=1, key="y_wave")
    if y_wave == "Arbitrary":
        y_expr = st.text_input("Enter expression using 't' (e.g., np.sin(4*t + np.pi/2))", key="y_expr")
    else:
        y_freq = st.slider("Frequency", 1, 20, 1, key="y_freq")
        y_amp = st.slider("Amplitude", 0.1, 5.0, 1.0, key="y_amp")
        y_phase = st.slider("Phase (in theta)", 0, 360, 0, key="y_phase")

with ctrl_col3:
    st.subheader("⚙️ Global Settings")
    t_max = st.slider("Time Range", float(1/2 * np.pi), float(20 * np.pi), float(t_max_default))
    num_points_density = st.slider("Number of Points per second", 100, 5000, num_points_default)
    show_quiz = st.checkbox("Show Quiz Overlay", value=True)
num_points=int(num_points_density*t_max)
# ---------- COMPUTE SIGNALS ----------
t = np.linspace(0, t_max, num_points)

if x_wave == "Arbitrary":
    x = waveform_function("Arbitrary", t, 0, 0, 0, expr=x_expr)
else:
    x = waveform_function(x_wave, t, x_freq, x_amp, x_phase)

if y_wave == "Arbitrary":
    y = waveform_function("Arbitrary", t, 0, 0, 0, expr=y_expr)
else:
    y = waveform_function(y_wave, t, y_freq, y_amp, y_phase)

# ---------- PLOTS ----------
plot_col1, plot_col2, plot_col3 = st.columns(3)

with plot_col1:
    fig1, ax1 = plt.subplots()
    fig1.patch.set_alpha(0.0)
    ax1.plot(t, x, color=plotcolor)
    ax1.set_title("x(t) vs t")
    ax1.set_xlabel("t")
    ax1.set_ylabel("x(t)")
    ax1.grid(True)
    st.pyplot(fig1)

with plot_col2:
    fig2, ax2 = plt.subplots()
    fig2.patch.set_alpha(0.0)
    ax2.plot(t, y, color=plotcolor)
    ax2.set_title("y(t) vs t")
    ax2.set_xlabel("t")
    ax2.set_ylabel("y(t)")
    ax2.grid(True)
    st.pyplot(fig2)
# Quiz question
quiz_x_wave="Triangle" 
quiz_y_wave="Triangle"
tq=t
quiz_x_freq=3
quiz_y_freq=2
quiz_x_amp=1
quiz_y_amp=1.5
quiz_x_phase=10
quiz_y_phase=0
with plot_col3:
    fig3, ax3 = plt.subplots()
    fig3.patch.set_alpha(0.0)

    # If quiz overlay enabled
    if show_quiz:
        tq = np.linspace(0, t_max, num_points)
        qx = waveform_function(quiz_x_wave, tq, quiz_x_freq, quiz_x_amp, quiz_x_phase)
        qy = waveform_function(quiz_y_wave, tq, quiz_y_freq, quiz_y_amp, quiz_y_phase)
        ax3.plot(qx, qy, color="gray", alpha=0.3, label="Quiz Figure")

    # User-tunable figure
    ax3.plot(x, y, color=plotcolor, label="Your Figure")
    
    ax3.set_title("Lissajous Figure: y(t) vs x(t)")
    ax3.set_xlabel("x(t)")
    ax3.set_ylabel("y(t)")
    ax3.axis("equal")
    ax3.grid(True)
    ax3.legend()
    st.pyplot(fig3)# ---------- SOCIAL MEDIA ----------
social_media_icons.render()

