import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

st.set_page_config(page_title="Lissajous Generator", layout="wide")
st.title("🎨 Lissajous Figure Generator")

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
# Define default values for time and resolution
t_max_default = 4 * np.pi
num_points_default = 1000

# Temp placeholders to initialize time axis
t = np.linspace(0, t_max_default, num_points_default)

# ---------- SIGNAL PRESETS (initial, dummy) ----------
x = np.sin(2 * np.pi * 3 * t)
y = np.sin(2 * np.pi * 4 * t + np.pi / 2)

# ---------- PLOTS FIRST ROW ----------
plot_col1, plot_col2, plot_col3 = st.columns(3)

with plot_col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(t, x, color='royalblue')
    ax1.set_title("x(t) vs t")
    ax1.set_xlabel("t")
    ax1.set_ylabel("x(t)")
    ax1.grid(True)
    plot_x_placeholder = st.empty()
    plot_x_placeholder.pyplot(fig1)

with plot_col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(t, y, color='green')
    ax2.set_title("y(t) vs t")
    ax2.set_xlabel("t")
    ax2.set_ylabel("y(t)")
    ax2.grid(True)
    plot_y_placeholder = st.empty()
    plot_y_placeholder.pyplot(fig2)

with plot_col3:
    fig3, ax3 = plt.subplots()
    ax3.plot(x, y, color='crimson')
    ax3.set_title("Lissajous Figure: y(t) vs x(t)")
    ax3.set_xlabel("x(t)")
    ax3.set_ylabel("y(t)")
    ax3.axis("equal")
    ax3.grid(True)
    plot_lissajous_placeholder = st.empty()
    plot_lissajous_placeholder.pyplot(fig3)

# ---------- CONTROLS SECOND ROW ----------
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
    t_max = st.slider("Time Range", float(2 * np.pi), float(20 * np.pi), float(t_max_default))
    num_points = st.slider("Number of Points", 100, 5000, num_points_default)

# ---------- RECOMPUTE AND UPDATE PLOTS ----------
# New time array
t = np.linspace(0, t_max, num_points)

# Signals
x = waveform_function(x_wave, t, x_freq, x_amp, x_phase)
y = waveform_function(y_wave, t, y_freq, y_amp, y_phase)

# Redraw all three plots
with plot_col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(t, x, color='royalblue')
    ax1.set_title("x(t) vs t")
    ax1.set_xlabel("t")
    ax1.set_ylabel("x(t)")
    ax1.grid(True)
    plot_x_placeholder.pyplot(fig1)

with plot_col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(t, y, color='green')
    ax2.set_title("y(t) vs t")
    ax2.set_xlabel("t")
    ax2.set_ylabel("y(t)")
    ax2.grid(True)
    plot_y_placeholder.pyplot(fig2)

with plot_col3:
    fig3, ax3 = plt.subplots()
    ax3.plot(x, y, color='crimson')
    ax3.set_title("Lissajous Figure: y(t) vs x(t)")
    ax3.set_xlabel("x(t)")
    ax3.set_ylabel("y(t)")
    ax3.axis("equal")
    ax3.grid(True)
    plot_lissajous_placeholder.pyplot(fig3)
