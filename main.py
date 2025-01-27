import streamlit as st
import logging
from inputs import get_decisions, get_factors
from life_sim import initialize_weights, adjust_sliders, render_sliders, validate_weights, calculate_scores
from visualize import animate_bar_growth, plot_radar_chart
import random
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_weights():
    """Initialize weights in session state with random default values."""
    if "weights" not in st.session_state:
        random_weights = [random.uniform(0.2, 0.6) for _ in range(3)]
        total = sum(random_weights)
        st.session_state.weights = {
            "risk": random_weights[0] / total,
            "reward": random_weights[1] / total,
            "uncertainty": random_weights[2] / total,
        }

def toggle_view():
    """Manage input and output views with a toggle."""
    if "show_outputs" not in st.session_state:
        st.session_state.show_outputs = False
    return st.session_state.show_outputs

def get_factors_with_random_defaults(decisions):
    """Prompt user to input scores for each decision with random default values, but only on initial load."""
    if "factors" not in st.session_state:
        st.session_state.factors = {"risk": [], "reward": [], "uncertainty": []}
        for decision in decisions:
            st.session_state.factors["risk"].append(random.randint(1, 10))
            st.session_state.factors["reward"].append(random.randint(1, 10))
            st.session_state.factors["uncertainty"].append(random.randint(1, 10))

    factors = {"risk": [], "reward": [], "uncertainty": []}
    for i, decision in enumerate(decisions):
        st.subheader(f"Scores for {decision}")
        col1, col2, col3 = st.columns(3)
        with col1:
            factors["risk"].append(
                st.slider(f"Risk (1-10)", 1, 10, st.session_state.factors["risk"][i], key=f"risk_{decision}")
            )
        with col2:
            factors["reward"].append(
                st.slider(f"Reward (1-10)", 1, 10, st.session_state.factors["reward"][i], key=f"reward_{decision}")
            )
        with col3:
            factors["uncertainty"].append(
                st.slider(f"Uncertainty (1-10)", 1, 10, st.session_state.factors["uncertainty"][i], key=f"uncertainty_{decision}")
            )

    # Ensure session state is updated to keep values scaled correctly
    st.session_state.factors = factors
    return {key: values for key, values in factors.items()}

def export_results_to_csv(decisions, scores):
    """Export decision scores to a CSV file."""
    df = pd.DataFrame({"Decision": decisions, "Score": [round(score, 2) for score in scores]})
    csv = df.to_csv(index=False)
    st.download_button(label="Download Results as CSV", data=csv, file_name="decision_scores.csv", mime="text/csv")

def main_app():
    st.title("Life Decision Calculator")
    st.write("Input your decisions and factor scores for evaluation.")

    if toggle_view():
        # Outputs View
        st.subheader("Results")
        decisions = st.session_state.get("decisions", [])
        factors = st.session_state.get("factors", {})
        scores = st.session_state.get("scores", [])

        if decisions and factors and scores:
            st.subheader("Decision Scores")
            st.write(f"Scores: {dict(zip(decisions, [round(score, 2) for score in scores]))}")

            st.subheader("Bar Growth Animation")
            animate_bar_growth(decisions, scores)

            st.subheader("Radar Chart")
            plot_radar_chart(decisions, factors)

            # Export to CSV
            export_results_to_csv(decisions, scores)

        if st.button("Go Back to Inputs"):
            st.session_state.show_outputs = False

    else:
        # Inputs View
        decisions = get_decisions()
        if not decisions:
            return

        factors = get_factors_with_random_defaults(decisions)
        initialize_weights()
        render_sliders()

        if validate_weights():
            if st.button("Calculate Scores"):
                scores = calculate_scores(factors, st.session_state.weights)

                # Save data to session state
                st.session_state.decisions = decisions
                st.session_state.factors = {key: [val for val in values] for key, values in factors.items()}
                st.session_state.scores = scores
                st.session_state.show_outputs = True

if __name__ == "__main__":
    main_app()