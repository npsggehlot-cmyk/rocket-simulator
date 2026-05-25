I built this to make rocketry more accessible and easier for people trying to get into it around the world. Enter your rocket's specs and simulate a complete flight with real aerospace physics — no engineering degree required.
What it does:

Newton's Second Law of Motion (F=ma) for all force calculations
Variable mass simulation as propellant burns
RK4 numerical integration for an accurate trajectory
Aerodynamic drag with variable drag coefficient based on Mach number
International Standard Atmosphere model - air density changes with altitude
Mach number tracking with variable speed of sound
Barrowman equations for rocket stability analysis
Monte Carlo simulation - 1000 flights to quantify uncertainty

Live Demo: https://rocket-simulator-njpmtcd9jvuoprfyojsegh.streamlit.app/
Run locally:
git clone [your repo]
pip install -r requirements.txt
streamlit run app.py
Built by Naivedhya Gehlot - Lambert High School, rising sophomore
