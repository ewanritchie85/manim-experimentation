"""
Manim capabilities showcase — a concise run-through of classic maths concepts.

Structure: one Scene (MathsShowcase) whose construct() calls a sequence of
self-contained segment methods, each demonstrating both a classic maths idea
and a different corner of Manim's toolkit:

    1. Pythagorean theorem      -> Transform, shape construction, area proof
    2. Differentiation          -> secant-to-tangent limit + ValueTracker sweep
    3. Integration               -> Axes.get_riemann_rectangles, area convergence
    4. Taylor series            -> function graphing, successive approximations
    5. Linear transformation    -> ApplyMatrix on a NumberPlane + basis vectors
    6. Vector field, curl & div -> ArrowVectorField + StreamLines (reused)

Each segment clears the scene before the next starts, so it plays as one
continuous "tour" video. To render a single segment on its own while
developing, comment out the other calls in MathsShowcase.construct().

Render examples:
    manim -pql scenes/manim_maths_showcase.py MathsShowcase
    manim -pql scenes/manim_maths_showcase.py MathsShowcase --format=mp4
"""

import math

import numpy as np
from manim import *

# Module-level field for ArrowVectorField/StreamLines — plain function so
# manim's deepcopy (Copy -> Create) doesn't try to pickle the Scene's lock
_MATHS_VORTICES = [(-2.0, 1.0, 3.0), (2.0, 1.0, -3.0)]
_MATHS_SOURCES = [(-2.0, -1.4, 3.0), (2.0, -1.4, -3.0)]
_MATHS_EPSILON = 0.3


def _maths_field_func(point):
    x, y, _ = point
    vx, vy = 0.0, 0.0
    for cx, cy, k in _MATHS_VORTICES:
        r2 = (x - cx) ** 2 + (y - cy) ** 2 + _MATHS_EPSILON
        vx += -k * (y - cy) / r2
        vy += k * (x - cx) / r2
    for cx, cy, k in _MATHS_SOURCES:
        r2 = (x - cx) ** 2 + (y - cy) ** 2 + _MATHS_EPSILON
        vx += k * (x - cx) / r2
        vy += k * (y - cy) / r2
    return np.array([vx, vy, 0.0])


class MathsShowcase(Scene):
    def construct(self):
        self.section_title("An overview of classic maths concepts, in Manim")
        self.pythagorean_theorem()
        self.differentiation()
        self.integration()
        self.taylor_series()
        self.linear_transformation()
        self.vector_field_curl_divergence()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def top_left_stack(self, *mobjects, buff=0.25, corner_buff=0.4):
        """Arrange mobjects in a vertical stack, left-aligned, anchored to
        the top-left corner, with consistent spacing. Returns the VGroup so
        callers can .play(Write(...)) on it or update individual children."""
        group = VGroup(*mobjects).arrange(DOWN, aligned_edge=LEFT, buff=buff)
        group.to_corner(UL, buff=corner_buff)
        return group

    def section_title(self, text, subtitle=None, wait=1.5, use_math_subtitle=False):
        """Full-screen title card between segments.

        subtitle may be:
          - None
          - a plain string (rendered with Text, or MathTex if use_math_subtitle=True)
          - a Mobject (e.g. MathTex(r"a^2 + b^2 = c^2")) already constructed —
            it will be positioned below the title.
        """
        title = Text(text, font_size=40)
        group = VGroup(title)
        sub = None
        if subtitle is not None:
            if isinstance(subtitle, Mobject):
                sub = subtitle
                # Ensure consistent positioning below title; caller can pre-style colour/size
                sub.next_to(title, DOWN, buff=0.4)
            elif use_math_subtitle:
                sub = MathTex(subtitle, font_size=30, color=GRAY_B)
                sub.next_to(title, DOWN, buff=0.4)
            else:
                sub = Text(subtitle, font_size=24, color=GRAY_B)
                sub.next_to(title, DOWN, buff=0.4)
            group.add(sub)
        self.play(Write(title))
        if sub is not None:
            self.play(FadeIn(sub))
        self.wait(wait)
        self.play(FadeOut(group))

    def clear_scene(self):
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ------------------------------------------------------------------
    # 1. Pythagorean theorem
    # ------------------------------------------------------------------

    def pythagorean_theorem(self):
        self.section_title(
            "1. The Pythagorean Theorem",
            MathTex(r"a^2 + b^2 = c^2", font_size=32, color=GRAY_B),
        )

        a, b = 2.0, 1.5
        c = np.hypot(a, b)

        triangle = Polygon(
            ORIGIN,
            RIGHT * a,
            RIGHT * a + UP * b,
            color=WHITE,
            stroke_width=3,
        ).shift(LEFT * 2 + DOWN * 0.5)

        labels = VGroup(
            MathTex("a").next_to(triangle, DOWN, buff=0.15),
            MathTex("b").next_to(triangle, RIGHT, buff=0.15),
            MathTex("c").move_to(
                triangle.get_vertices()[0:3:2].mean(axis=0) + UP * 0.3 + LEFT * 0.3
            ),
        )

        self.play(Create(triangle))
        self.play(Write(labels))
        self.wait(0.5)

        # Squares built on each side, area-proportional to a^2, b^2, c^2
        sq_a = Square(side_length=a, color=BLUE, fill_opacity=0.4)
        sq_a.next_to(triangle, DOWN, buff=0).align_to(triangle, LEFT)

        sq_b = Square(side_length=b, color=GREEN, fill_opacity=0.4)
        sq_b.next_to(triangle, RIGHT, buff=0).align_to(triangle, UP)

        # Square on hypotenuse: one full edge flush against the hypotenuse,
        # extending outward away from the triangle interior (classic diagram).
        sq_c = Square(side_length=c, color=RED, fill_opacity=0.4)
        verts = triangle.get_vertices()
        P0 = verts[0]
        P2 = verts[2]
        hyp_mid = (P0 + P2) / 2
        h_vec = P2 - P0
        c_len = np.linalg.norm(h_vec)
        # outward normal (perpendicular to hypotenuse, pointing away from interior)
        interior_pt = verts[1]
        to_interior = interior_pt - hyp_mid
        n1 = np.array([-h_vec[1], h_vec[0], 0]) / c_len
        n_out = n1 if np.dot(n1[:2], to_interior[:2]) < 0 else -n1
        theta = np.arctan2(h_vec[1], h_vec[0])
        sq_c.rotate(theta)
        c_center = hyp_mid + n_out * (c / 2)
        sq_c.move_to(c_center)

        self.play(FadeIn(sq_a), FadeIn(sq_b), FadeIn(sq_c))
        self.wait(0.5)

        equation = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=44)
        equation.to_edge(DOWN)
        equation[0].set_color(BLUE)
        equation[2].set_color(GREEN)
        equation[4].set_color(RED)
        self.play(Write(equation))
        self.wait(2)

        self.clear_scene()

    # ------------------------------------------------------------------
    # 2. Differentiation: limit definition, then the tangent sweep
    # ------------------------------------------------------------------

    def differentiation(self):
        self.section_title(
            "2. Differentiation", "the derivative as a limit of secant slopes"
        )

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=5,
        ).shift(RIGHT * 0.8 + DOWN * 0.3)
        f = lambda x: 0.4 * x**2
        df = lambda x: 0.8 * x  # dy/dx

        graph = axes.plot(f, color=BLUE)
        # Top-left anchored layout: graph_label and formulae share UL stack, clear of axes
        graph_label = MathTex("f(x) = 0.4x^2", font_size=28)
        limit_formula = MathTex(
            r"\frac{dy}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            font_size=30,
        )
        header = self.top_left_stack(graph_label, limit_formula)
        self.play(Create(axes), Create(graph), Write(header))

        # --- 2a. Secant line shrinking to the tangent (the limit itself) ---
        x0 = -1.5
        h_tracker = ValueTracker(2.0)

        fixed_point = Dot(axes.c2p(x0, f(x0)), color=YELLOW)
        moving_point = always_redraw(
            lambda: Dot(
                axes.c2p(x0 + h_tracker.get_value(), f(x0 + h_tracker.get_value())),
                color=ORANGE,
            )
        )

        def secant_line():
            h = h_tracker.get_value()
            slope = (f(x0 + h) - f(x0)) / h
            x_left, x_right = x0 - 1.0, x0 + max(h, 0) + 1.0
            p1 = axes.c2p(x_left, f(x0) + slope * (x_left - x0))
            p2 = axes.c2p(x_right, f(x0) + slope * (x_right - x0))
            return Line(p1, p2, color=RED)

        secant = always_redraw(secant_line)

        # Fixed anchor below limit_formula, left-aligned, not dynamic arrange
        secant_slope_label = always_redraw(
            lambda: MathTex(
                r"\frac{\Delta y}{\Delta x} = "
                f"{(f(x0 + h_tracker.get_value()) - f(x0)) / h_tracker.get_value():.2f}",
                font_size=28,
            )
            .next_to(limit_formula, DOWN, buff=0.25)
            .align_to(limit_formula, LEFT)
        )

        self.play(
            FadeIn(fixed_point),
            FadeIn(moving_point),
            Create(secant),
            FadeIn(secant_slope_label),
        )
        self.wait(0.5)
        self.play(h_tracker.animate.set_value(0.02), run_time=4, rate_func=smooth)
        self.wait(1)

        self.play(
            FadeOut(moving_point),
            FadeOut(secant),
            FadeOut(secant_slope_label),
            FadeOut(limit_formula),
        )

        # --- 2b. Sweep the tangent point across the whole curve ---
        x_tracker = ValueTracker(-2.5)

        dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_tracker.get_value(), f(x_tracker.get_value())), color=YELLOW
            )
        )

        def tangent_line():
            x0 = x_tracker.get_value()
            slope = df(x0)
            y0 = f(x0)
            x_left, x_right = x0 - 1.2, x0 + 1.2
            p1 = axes.c2p(x_left, y0 + slope * (x_left - x0))
            p2 = axes.c2p(x_right, y0 + slope * (x_right - x0))
            return Line(p1, p2, color=ORANGE)

        line = always_redraw(tangent_line)

        # Eyeline stays consistent: slope_label where limit_formula was (below graph_label, UL)
        slope_label = always_redraw(
            lambda: MathTex(
                rf"\frac{{dy}}{{dx}}\bigg|_{{x={x_tracker.get_value():.1f}}} = {df(x_tracker.get_value()):.1f}",
                font_size=28,
            )
            .next_to(graph_label, DOWN, buff=0.25)
            .align_to(graph_label, LEFT)
        )

        self.play(FadeOut(fixed_point), FadeIn(dot), Create(line), FadeIn(slope_label))
        self.wait(0.5)
        self.play(x_tracker.animate.set_value(2.5), run_time=4, rate_func=smooth)
        self.wait(1)

        self.clear_scene()

    # ------------------------------------------------------------------
    # 3. Integration: Riemann sums converging to the area under a curve
    # ------------------------------------------------------------------

    def integration(self):
        self.section_title("3. Integration", "Riemann sums and the area under a curve")

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=5,
        ).shift(RIGHT * 0.9 + DOWN * 0.3)
        f = lambda x: 0.5 * x**2 + 1
        F = lambda x: x**3 / 6 + x  # antiderivative, for the exact value

        graph = axes.plot(f, x_range=[0, 4], color=BLUE)
        graph_label = MathTex("f(x) = 0.5x^2 + 1", font_size=28)
        integral_formula = MathTex(
            r"\int_0^4 f(x)\,dx \approx \sum_{i} f(x_i)\,\Delta x",
            font_size=30,
        )
        n_label = MathTex("n = 4", font_size=28)
        header = self.top_left_stack(graph_label, integral_formula, n_label)
        self.play(Create(axes), Create(graph), Write(header))

        # Riemann rectangles getting finer: 4 -> 8 -> 16 -> 32
        n_values = [4, 8, 16, 32]
        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 4],
            dx=4 / n_values[0],
            color=(BLUE, GREEN),
            fill_opacity=0.6,
            stroke_width=1,
        )
        self.play(FadeIn(rects))
        self.wait(0.5)

        for n in n_values[1:]:
            new_rects = axes.get_riemann_rectangles(
                graph,
                x_range=[0, 4],
                dx=4 / n,
                color=(BLUE, GREEN),
                fill_opacity=0.6,
                stroke_width=0.5,
            )
            new_label = MathTex(f"n = {n}", font_size=28).next_to(
                integral_formula, DOWN, buff=0.25
            ).align_to(integral_formula, LEFT)
            self.play(
                Transform(rects, new_rects),
                Transform(n_label, new_label),
                run_time=1.2,
            )
            self.wait(0.3)

        self.wait(0.5)

        # Swap the rectangles for the exact shaded area and show the FTC result
        # Place ftc_formula in same top-left stack, below n_label, consistent with det_label placement
        area = axes.get_area(graph, x_range=[0, 4], color=GREEN, opacity=0.5)
        exact_value = F(4) - F(0)
        ftc_formula = MathTex(
            r"\int_0^4 f(x)\,dx = F(4) - F(0) = " + f"{exact_value:.2f}",
            font_size=28,
        ).next_to(n_label, DOWN, buff=0.25).align_to(n_label, LEFT)

        self.play(FadeOut(rects), FadeIn(area))
        self.play(Write(ftc_formula))
        self.wait(2)

        self.clear_scene()

    # ------------------------------------------------------------------
    # 4. Taylor series approximation
    # ------------------------------------------------------------------

    def taylor_series(self):
        self.section_title("4. Taylor Series", "polynomials approximating sin(x)")

        axes = Axes(
            x_range=[-PI * 1.5, PI * 1.5, PI / 2],
            y_range=[-2, 2, 1],
            x_length=9,
            y_length=5,
        ).scale(0.92)
        axes.shift(RIGHT * 0.7 + DOWN * 0.3)
        sine_graph = axes.plot(np.sin, color=BLUE)
        self.play(Create(axes), Create(sine_graph))

        # Top-left stack for sin label + P_n labels (consistent with other sections)
        sin_label = MathTex(r"\sin(x)", color=BLUE, font_size=30)
        base_header = self.top_left_stack(sin_label)
        self.play(Write(base_header))
        self.wait(0.5)

        def taylor_sin(x, n_terms):
            total = 0.0
            for n in range(n_terms):
                power = 2 * n + 1
                total += ((-1) ** n) * (x**power) / math.factorial(power)
            return total

        colors = [YELLOW, GREEN, RED, PURPLE]
        current_approx = None

        for i, n_terms in enumerate([1, 2, 3, 5]):
            approx_graph = axes.plot(
                lambda x, n=n_terms: taylor_sin(x, n),
                color=colors[i],
                x_range=[-PI * 1.5, PI * 1.5],
            )
            approx_label = MathTex(
                f"P_{{{2 * n_terms - 1}}}(x)", color=colors[i], font_size=26
            )
            # Stack below sin_label in top-left corner, fixed offsets so no overlap
            approx_label.next_to(
                sin_label, DOWN, buff=0.25 + i * 0.42
            ).align_to(sin_label, LEFT)

            if current_approx is None:
                self.play(Create(approx_graph), Write(approx_label))
            else:
                self.play(
                    Transform(current_approx, approx_graph),
                    Write(approx_label),
                )
            if current_approx is None:
                current_approx = approx_graph
            self.wait(0.8)

        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 5. Linear transformation (matrix acting on the plane)
    # ------------------------------------------------------------------

    def linear_transformation(self):
        self.section_title(
            "5. Linear Transformations",
            "a matrix stretches, rotates, and shears the plane",
        )

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1])
        self.play(Create(plane))

        i_hat = Arrow(ORIGIN, plane.c2p(1, 0), buff=0, color=GREEN)
        j_hat = Arrow(ORIGIN, plane.c2p(0, 1), buff=0, color=RED)
        basis = VGroup(i_hat, j_hat)

        unit_square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=YELLOW,
            fill_opacity=0.25,
            stroke_width=2,
        )

        self.play(Create(unit_square), GrowArrow(i_hat), GrowArrow(j_hat))
        self.wait(0.5)

        matrix_tex = Matrix([[2, 1], [0, 1.5]]).to_corner(UL)
        matrix_tex.set_column_colors(GREEN, RED)
        self.play(Write(matrix_tex))

        matrix = [[2, 1], [0, 1.5]]
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det_label = MathTex(f"\\det = {det:.1f}").next_to(matrix_tex, DOWN)

        self.play(
            ApplyMatrix(matrix, plane),
            ApplyMatrix(matrix, unit_square),
            ApplyMatrix(matrix, basis),
            run_time=3,
        )
        self.play(Write(det_label))
        self.wait(2)

        self.clear_scene()

    # ------------------------------------------------------------------
    # 6. Vector field with curl & divergence (reused from the earlier scene)
    # ------------------------------------------------------------------

    VORTICES = _MATHS_VORTICES
    SOURCES = _MATHS_SOURCES
    EPSILON = _MATHS_EPSILON

    def field_func(self, point):
        # Instance wrapper for tests — delegates to module func
        return _maths_field_func(point)

    def vector_field_curl_divergence(self):
        self.section_title(
            "6. Vector Fields: Curl & Divergence",
            "superposition of vortices and point sources",
        )

        formula = MathTex(
            r"\vec{F}(x,y) = \sum_{i} k_i\,"
            r"\frac{-(y-y_i)\hat{\imath}+(x-x_i)\hat{\jmath}}{r_i^2+\varepsilon}",
            r"\;+\;\sum_{j} m_j\,"
            r"\frac{(x-x_j)\hat{\imath}+(y-y_j)\hat{\jmath}}{r_j^2+\varepsilon}",
            font_size=32,
        ).to_edge(UP)
        self.play(Write(formula))
        self.wait(1.5)
        self.play(formula.animate.scale(0.55).to_corner(UL))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GRAY_D, "stroke_width": 1.5},
        )
        self.play(Create(axes))

        field = ArrowVectorField(
            _maths_field_func,
            x_range=[-4, 4, 0.5],
            y_range=[-3, 3, 0.5],
            length_func=lambda norm: 0.25 * sigmoid(norm),
            color_scheme=lambda p: np.linalg.norm(_maths_field_func(p)),
            colors=[BLUE_E, BLUE, GREEN, YELLOW, RED],
        )
        self.play(Create(field), run_time=2.5)

        def marker(cx, cy, label_text, color):
            dot = Dot(axes.c2p(cx, cy), color=color)
            ring = Circle(radius=0.5, color=color, stroke_width=3).move_to(
                axes.c2p(cx, cy)
            )
            label = Text(label_text, font_size=18, color=color).next_to(
                ring, UP, buff=0.1
            )
            return VGroup(dot, ring, label)

        markers = VGroup(
            marker(*self.VORTICES[0][:2], "curl > 0", TEAL),
            marker(*self.VORTICES[1][:2], "curl < 0", PURPLE),
            marker(*self.SOURCES[0][:2], "div > 0", ORANGE),
            marker(*self.SOURCES[1][:2], "div < 0", RED_C),
        )
        self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in markers], lag_ratio=0.3))
        self.wait(1)

        stream = StreamLines(
            _maths_field_func,
            x_range=[-4, 4, 0.5],
            y_range=[-3, 3, 0.5],
            stroke_width=2,
            max_anchors_per_line=25,
            padding=0.5,
        )
        self.add(stream)
        stream.start_animation(warm_up=True, flow_speed=1.2)
        self.wait(5)
        stream.end_animation()

        self.wait(1)
        self.clear_scene()
