import streamlit as st
import pandas as pd
import numpy as np
import time # <- We'll need this later as well
from wf_sim import Population

st.title('Simple Wright-Fisher Simulation of Genetic Drift')


# Initialize the chart with the initial allele frequency of the derived
# allele. `line_chart` expects a list, so we must wrap `p.f` in square
# brackets to pass a list
generations = st.sidebar.slider("Generations", 1, 100, 50, 1)
N_var = st.sidebar.slider("Population size", 1, 100, 10, 1)
f_var = st.sidebar.slider("Initial allele frequency", 0.0, 1.0, 0.2, 0.1)

# Create a new Population
# As a reminder these are the default values for population size (N)
# and initial derived allele frequency (f).
#   N=10, f=0.2
p = Population(N=N_var, f=f_var)

chart = st.line_chart([p.f])
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# Initially we'll run a loop 50 times
for i in range(1, generations):
    # Step 1 wf generation
    p.step(ngens=1)
    # Calculate the current derived allele frequency
    freq = np.sum(p.pop)/len(p.pop)
    # Update the chart to add the current allele frequency
    chart.add_rows([freq])
    # stop plotting if f = 1 or f = 0
    if freq == 0 or freq == 1:
        status_text.text(f"Simulation ended after {i} generations")
        break
    else:
        # reports progress in sidebar
        prog = round(i/generations, 2)
        progress_bar.progress(prog)
        status_text.text(f"{prog*100}% complete")
        
    # sleep for a small amount of time so you can watch the animation
    time.sleep(0.05)

#progress_bar.empty()

# Add a button to rerun the simulation
st.button("Rerun")

