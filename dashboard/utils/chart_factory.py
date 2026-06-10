"""
TATA Group 360 Analytics - Reusable Chart Factory
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from .constants import (
    TATA_PALETTE, CHART_TEMPLATE, CHART_FONT, CHART_BG,
    CHART_PAPER_BG, CHART_MARGIN, TATA_BLUE_LIGHT, TATA_GOLD, TATA_RED
)


def apply_layout(fig, title="", height=500, show_legend=True):
    """Apply consistent dark-theme layout to any Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="white"), x=0.02),
        template=CHART_TEMPLATE,
        font=CHART_FONT,
        plot_bgcolor=CHART_BG,
        paper_bgcolor=CHART_PAPER_BG,
        height=height,
        margin=CHART_MARGIN,
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0.3)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
    )
    return fig


def kpi_card_html(label, value, delta=None, icon=""):
    """Generate HTML for a KPI metric card."""
    delta_html = ""
    if delta:
        color = "#4CAF50" if delta.startswith("+") or delta.startswith("^") else "#F44336"
        delta_html = f'<div style="color:{color};font-size:14px;margin-top:4px">{delta}</div>'
    return f"""
    <div style="background:linear-gradient(135deg,rgba(30,136,229,0.15),rgba(0,188,212,0.08));
                border:1px solid rgba(30,136,229,0.25);border-radius:16px;padding:24px 20px;
                text-align:center;backdrop-filter:blur(10px);">
        <div style="font-size:28px;margin-bottom:6px">{icon}</div>
        <div style="font-size:32px;font-weight:800;color:white;letter-spacing:-1px">{value}</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:6px;text-transform:uppercase;
                    letter-spacing:1.5px">{label}</div>
        {delta_html}
    </div>
    """


def make_treemap(df, path_col, value_col, color_col=None, title=""):
    """Create a treemap chart."""
    fig = px.treemap(
        df, path=[path_col], values=value_col,
        color=value_col if color_col is None else color_col,
        color_continuous_scale="Blues",
    )
    return apply_layout(fig, title, height=550)


def make_line_chart(df, x, y_cols, labels=None, title="", colors=None):
    """Multi-line chart."""
    fig = go.Figure()
    if colors is None:
        colors = TATA_PALETTE
    if labels is None:
        labels = y_cols

    for i, (col, label) in enumerate(zip(y_cols, labels)):
        fig.add_trace(go.Scatter(
            x=df[x], y=df[col], name=label,
            line=dict(color=colors[i % len(colors)], width=2.5),
            mode="lines",
        ))
    return apply_layout(fig, title)


def make_bar_chart(df, x, y, color=None, barmode="group", title="", orientation="v",
                   color_sequence=None):
    """Bar chart with optional grouping."""
    fig = px.bar(
        df, x=x, y=y, color=color, barmode=barmode,
        orientation=orientation,
        color_discrete_sequence=color_sequence or TATA_PALETTE,
    )
    return apply_layout(fig, title, height=500)


def make_heatmap(corr_df, title=""):
    """Correlation heatmap."""
    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale="RdBu_r",
        zmin=-1, zmax=1,
        text=np.round(corr_df.values, 2),
        texttemplate="%{text}",
        textfont=dict(size=11),
    ))
    return apply_layout(fig, title, height=550)


def make_dual_axis(df, x, y1, y2, name1="", name2="", title=""):
    """Dual Y-axis chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y1], name=name1,
        line=dict(color=TATA_BLUE_LIGHT, width=3),
    ))
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y2], name=name2,
        yaxis="y2",
        line=dict(color=TATA_GOLD, width=3, dash="dot"),
    ))
    fig = apply_layout(fig, title, height=500)
    fig.update_layout(
        yaxis2=dict(
            overlaying="y", side="right",
            gridcolor="rgba(255,255,255,0.03)",
            zeroline=False,
        )
    )
    return fig


def make_bubble_chart(df, x, y, size, color, text_col=None, title=""):
    """Bubble chart."""
    fig = px.scatter(
        df, x=x, y=y, size=size, color=color,
        hover_name=text_col,
        color_discrete_sequence=TATA_PALETTE,
        size_max=60,
    )
    return apply_layout(fig, title, height=550)


def make_pie_donut(df, names, values, title="", hole=0.55):
    """Donut/pie chart."""
    colors = df["Color"].tolist() if "Color" in df.columns else TATA_PALETTE
    fig = go.Figure(data=[go.Pie(
        labels=df[names], values=df[values],
        hole=hole,
        marker=dict(colors=colors, line=dict(color="rgba(0,0,0,0.3)", width=2)),
        textinfo="label+percent",
        textfont=dict(size=12),
    )])
    return apply_layout(fig, title, height=500, show_legend=False)


def make_area_chart(df, x, y_cols, labels=None, title=""):
    """Stacked area chart."""
    fig = go.Figure()
    if labels is None:
        labels = y_cols
    for i, (col, label) in enumerate(zip(y_cols, labels)):
        fig.add_trace(go.Scatter(
            x=df[x], y=df[col], name=label,
            fill="tonexty" if i > 0 else "tozeroy",
            line=dict(color=TATA_PALETTE[i % len(TATA_PALETTE)], width=1),
            mode="lines",
        ))
    return apply_layout(fig, title, height=500)


def add_milestone_annotations(fig, milestones, y_pos=0.95):
    """Add vertical annotation lines for key milestone events."""
    for year, label in milestones:
        fig.add_vline(
            x=year, line_dash="dash",
            line_color="rgba(255,255,255,0.2)", line_width=1,
        )
        fig.add_annotation(
            x=year, y=y_pos, yref="paper",
            text=f"<b>{label}</b>", showarrow=False,
            font=dict(size=9, color="rgba(255,255,255,0.5)"),
            textangle=-90,
        )
    return fig
