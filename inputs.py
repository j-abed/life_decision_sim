import streamlit as st

def get_decisions():
    """Prompt user to input decision options."""
    decisions_input = st.text_input(
        "Enter decision options (comma-separated, up to 3):", 
        "Take New Job,Stay in Role,Third Option"
    )
    decisions = [decision.strip() for decision in decisions_input.split(",")][:3]
    return decisions

def get_factors(decisions):
    """Prompt user to input scores for each decision using sliders."""
    factors = {"risk": [], "reward": [], "uncertainty": []}
    for decision in decisions:
        st.subheader(f"Scores for {decision}")
        col1, col2, col3 = st.columns(3)
        with col1:
            factors["risk"].append(st.slider(f"Risk (1-10)", 1, 10, 5, key=f"risk_{decision}"))
        with col2:
            factors["reward"].append(st.slider(f"Reward (1-10)", 1, 10, 5, key=f"reward_{decision}"))
        with col3:
            factors["uncertainty"].append(st.slider(f"Uncertainty (1-10)", 1, 10, 5, key=f"uncertainty_{decision}"))
    return {key: [val * 10 for val in values] for key, values in factors.items()}
