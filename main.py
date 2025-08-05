import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
plt.rcParams.update({
    "axes.facecolor": "none",         # Transparent axes background
    "figure.facecolor": "none",       # Transparent figure background
    "axes.edgecolor": "white",        # White border
    "axes.labelcolor": "white",       # White x/y labels
    "xtick.color": "white",           # White x-axis tick labels
    "ytick.color": "white",           # White y-axis tick labels
    "grid.color": "none",            # White grid lines
    "text.color": "white",            # All other text (like titles)
    "axes.titlecolor": "white",       # Title color
})
plotcolor='dodgerblue'
st.set_page_config(page_title="Lissajous Generator", layout="wide")
st.title("Lissajous Figure Generator")

# ---------- Waveform Generator ----------
def waveform_function(name, t, freq, amp, phase):
    omega_t = 2 * np.pi * freq * t + phase
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
    else:
        return np.zeros_like(t)

# ---------- GLOBAL SETTINGS ----------
t_max_default = 4 * np.pi
num_points_default = 400

# ---------- CONTROLS ----------
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)

with ctrl_col1:
    st.subheader("🔵 x(t) Settings")
    x_wave = st.selectbox("Waveform", ["Sine", "Cosine", "Square", "Triangle", "Sawtooth"], key="x_wave")
    x_freq = st.slider("Frequency", 1, 20, 3, key="x_freq")
    x_amp = st.slider("Amplitude", 0.1, 5.0, 1.0, key="x_amp")
    x_phase = st.slider("Phase (radians)", 0.0, 2 * np.pi, 0.0, key="x_phase")

with ctrl_col2:
    st.subheader("🟢 y(t) Settings")
    y_wave = st.selectbox("Waveform", ["Sine", "Cosine", "Square", "Triangle", "Sawtooth"], key="y_wave")
    y_freq = st.slider("Frequency", 1, 20, 4, key="y_freq")
    y_amp = st.slider("Amplitude", 0.1, 5.0, 1.0, key="y_amp")
    y_phase = st.slider("Phase (radians)", 0.0, 2 * np.pi, np.pi / 2, key="y_phase")

with ctrl_col3:
    st.subheader("⚙️ Global Settings")
    t_max = st.slider("Time Range", float(1/2 * np.pi), float(20 * np.pi), float(t_max_default))
    num_points = st.slider("Number of Points", 100, 5000, num_points_default)

# ---------- COMPUTE SIGNALS ----------
t = np.linspace(0, t_max, num_points)
x = waveform_function(x_wave, t, x_freq, x_amp, x_phase)
y = waveform_function(y_wave, t, y_freq, y_amp, y_phase)

# ---------- PLOTS ----------
plot_col1, plot_col2, plot_col3 = st.columns(3)

with plot_col1:
    fig1, ax1 = plt.subplots()
    fig1.patch.set_alpha(0.0)        # Figure background
    ax1.plot(t, x, color=plotcolor)
    ax1.set_title("x(t) vs t")
    ax1.set_xlabel("t")
    ax1.set_ylabel("x(t)")
    ax1.grid(True)
    st.pyplot(fig1)

with plot_col2:
    fig2, ax2 = plt.subplots()
    fig2.patch.set_alpha(0.0)        # Figure background
    ax2.plot(t, y, color=plotcolor)
    ax2.set_title("y(t) vs t")
    ax2.set_xlabel("t")
    ax2.set_ylabel("y(t)")
    ax2.grid(True)
    st.pyplot(fig2)

with plot_col3:
    fig3, ax3 = plt.subplots()
    fig3.patch.set_alpha(0.0)        # Figure background
    ax3.plot(x, y, color=plotcolor)
    ax3.set_title("Lissajous Figure: y(t) vs x(t)")
    ax3.set_xlabel("x(t)")
    ax3.set_ylabel("y(t)")
    ax3.axis("equal")
    ax3.grid(True)
    st.pyplot(fig3)
