import streamlit as st
import math

def initialize_weights():
    """Initialize weights in session state."""
    if "weights" not in st.session_state:
        st.session_state.weights = {"risk": 0.3, "reward": 0.5, "uncertainty": 0.2}

def adjust_sliders():
    """Adjust sliders dynamically to ensure weights sum to 1."""
    total_weight = sum(st.session_state.weights.values())
    if total_weight > 1.0:
        excess = total_weight - 1.0
        keys = list(st.session_state.weights.keys())
        for key in keys:
            if st.session_state.weights[key] > 0:
                st.session_state.weights[key] -= excess * (st.session_state.weights[key] / total_weight)
                st.session_state.weights[key] = max(0, st.session_state.weights[key])

def render_sliders():
    """Render sliders for weights with dynamic adjustment."""
    st.markdown("---")
    st.subheader("Decision Weights")

    st.session_state.weights["risk"] = st.slider(
        "Risk Weight",
        0.0,
        1.0,
        st.session_state.weights["risk"],
        step=0.01,
        key="risk_weight",
        on_change=adjust_sliders,
    )
    st.session_state.weights["reward"] = st.slider(
        "Reward Weight",
        0.0,
        1.0,
        st.session_state.weights["reward"],
        step=0.01,
        key="reward_weight",
        on_change=adjust_sliders,
    )
    st.session_state.weights["uncertainty"] = st.slider(
        "Uncertainty Weight",
        0.0,
        1.0,
        st.session_state.weights["uncertainty"],
        step=0.01,
        key="uncertainty_weight",
        on_change=adjust_sliders,
    )

def validate_weights():
    """Ensure weights sum to approximately 1."""
    total_weight = sum(st.session_state.weights.values())
    if total_weight > 1.0:
        st.error("Weights must not exceed 1. Adjust the sliders accordingly.")
        return False
    if not (0.99 <= total_weight <= 1.01):
        st.error("Weights must sum to approximately 1. Adjust the sliders accordingly.")
        return False
    st.success("Weights are valid!")
    return True

def calculate_scores(factors, weights):
    entropy = calculate_entropy(factors)
    num_decisions = len(next(iter(factors.values())))
    scores = []
    for i in range(num_decisions):
        score = sum(entropy[key] * weights[key] * factors[key][i] for key in weights)
        scores.append(score)
    return scores


def calculate_entropy(factors):
    """Calculate entropy for each factor."""
    entropy = {}
    for key, values in factors.items():
        probabilities = [val / sum(values) for val in values]
        entropy[key] = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

