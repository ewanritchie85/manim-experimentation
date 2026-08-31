"""
Vector field with regions of curl and divergence — Manim Community scene.

The field is built as a superposition of:
  - two point vortices (pure rotation -> nonzero curl, zero divergence)
  - a point source and a point sink (pure radial flow -> nonzero divergence, zero curl)

This lets the scene visually separate "curl regions" from "divergence regions"
instead of using one field where both effects are tangled together everywhere.
"""

import numpy as np
from manim import *

# ---- Field parameters -------------------------------------------------

# Vortices: (center_x, center_y, strength). Positive strength = counter-
# clockwise rotation (curl > 0); negative strength = clockwise (curl < 0).
VORTICES = [
    (-2.0, 1.2, 3.0),
    (2.0, 1.2, -3.0),
]

# Sources/sinks: (center_x, center_y, strength). Positive strength = source
# (divergence > 0, flow points outward); negative strength = sink
# (divergence < 0, flow points inward).
SOURCES = [
    (-2.0, -1.4, 3.0),
    (2.0, -1.4, -3.0),
]

EPSILON = 0.3  # regularization so nothing blows up at the centers


def vector_field_func(point):
    x, y, _ = point
    vx, vy = 0.0, 0.0

    for cx, cy, k in VORTICES:
        r2 = (x - cx) ** 2 + (y - cy) ** 2 + EPSILON
        vx += -k * (y - cy) / r2
        vy += k * (x - cx) / r2

    for cx, cy, k in SOURCES:
        r2 = (x - cx) ** 2 + (y - cy) ** 2 + EPSILON
        vx += k * (x - cx) / r2
        vy += k * (y - cy) / r2

    return np.array([vx, vy, 0.0])


class VectorFieldCurlDivergence(Scene):
    def construct(self):
        # ---- 1. Title -----------------------------------------------
        title = Text("A Vector Field with Curl and Divergence", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---- 2. Formula -----------------------------------------------
        formula = MathTex(
            r"\vec{F}(x,y) = \sum_{i=1}^{2} k_i\,"
            r"\frac{-(y-y_i)\,\hat{\imath} + (x-x_i)\,\hat{\jmath}}{r_i^2+\varepsilon}",
            r"\;+\;",
            r"\sum_{j=1}^{2} m_j\,"
            r"\frac{(x-x_j)\,\hat{\imath} + (y-y_j)\,\hat{\jmath}}{r_j^2+\varepsilon}",
            font_size=34,
        )
        formula.next_to(title, DOWN, buff=0.6)

        subcaption = Text(
            "vortex terms (curl)          +          source/sink terms (divergence)",
            font_size=22,
            color=GRAY_B,
        )
        subcaption.next_to(formula, DOWN, buff=0.3)

        self.play(Write(formula))
        self.play(FadeIn(subcaption))
        self.wait(2)

        # Shrink formula and tuck it into the corner so the field has room
        self.play(
            FadeOut(subcaption),
            formula.animate.scale(0.55).to_corner(UL),
            title.animate.scale(0.6).to_corner(UR),
        )

        # ---- 3. Axes + vector field -------------------------------------
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GRAY_D, "stroke_width": 1.5},
        )
        self.play(Create(axes))

        field = ArrowVectorField(
            vector_field_func,
            x_range=[-4, 4, 0.5],
            y_range=[-3, 3, 0.5],
            length_func=lambda norm: 0.25 * sigmoid(norm),
            color_scheme=lambda p: np.linalg.norm(vector_field_func(p)),
            colors=[BLUE_E, BLUE, GREEN, YELLOW, RED],
        )
        self.play(Create(field), run_time=2.5)
        self.wait(1)

        # ---- 4. Highlight the regions ------------------------------------
        def marker(cx, cy, label_text, color):
            dot = Dot(axes.c2p(cx, cy), color=color)
            ring = Circle(radius=0.55, color=color, stroke_width=3).move_to(
                axes.c2p(cx, cy)
            )
            label = Text(label_text, font_size=20, color=color)
            label.next_to(ring, UP, buff=0.1)
            return VGroup(dot, ring, label)

        curl_pos = marker(*VORTICES[0][:2], "curl > 0 (CCW)", TEAL)
        curl_neg = marker(*VORTICES[1][:2], "curl < 0 (CW)", PURPLE)
        div_pos = marker(*SOURCES[0][:2], "div > 0 (source)", ORANGE)
        div_neg = marker(*SOURCES[1][:2], "div < 0 (sink)", RED_C)

        self.play(
            LaggedStart(
                *[FadeIn(m, scale=0.8) for m in (curl_pos, curl_neg, div_pos, div_neg)],
                lag_ratio=0.3,
            )
        )
        self.wait(1.5)

        # ---- 5. Stream lines to make the flow direction obvious -----------
        stream = StreamLines(
            vector_field_func,
            x_range=[-4, 4, 0.5],
            y_range=[-3, 3, 0.5],
            stroke_width=2,
            max_anchors_per_line=25,
            padding=0.5,
        )
        self.add(stream)
        stream.start_animation(warm_up=True, flow_speed=1.2)
        self.wait(6)
        stream.end_animation()

        self.wait(1)
        self.play(
            *[FadeOut(m) for m in self.mobjects],
        )
