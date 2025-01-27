import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def plot_radar_chart(decisions, factors):
    """Plot a radar chart to visualize factor trade-offs."""
    labels = list(factors.keys())
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    for decision in decisions:
        values = [factors[key][decisions.index(decision)] for key in labels]
        values += values[:1]
        ax.plot(angles, values, label=decision, linewidth=2, linestyle='solid')
        ax.fill(angles, values, alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    ax.yaxis.set_tick_params(labelsize=10)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    plt.title("Factor Trade-offs Across Decisions", fontsize=14, fontweight='bold')
    st.pyplot(fig)

def animate_bar_growth(decisions, scores):
    """Animate bar growth for decision scores."""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=decisions, y=[0] * len(scores), marker_color='skyblue'))
    frames = [
        go.Frame(
            data=[
                go.Bar(x=decisions, y=[score * (frame / 100) for score in scores])
            ],
            name=str(frame),
        )
        for frame in range(1, 101)
    ]
    fig.frames = frames
    fig.update_layout(
        title="Decision Scores (Animated)",
        xaxis=dict(title="Decisions"),
        yaxis=dict(title="Scores", range=[0, max(scores) + 10]),
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[None, {"frame": {"duration": 50, "redraw": True}}],
                    ),
                    dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0}}]),
                ],
            )
        ],
    )
    st.plotly_chart(fig)
