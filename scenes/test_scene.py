from manim import *


class TestScene(Scene):
    """Concise tour of Manim's core features — each demo stays fully on-screen."""

    def construct(self):
        # Persistent header — leaves full safe area below for demos
        title = Text("Manim Feature Tour", weight=BOLD).scale(0.8)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.4)

        def header(text: str, color=GREY_A) -> Text:
            return Text(text, font_size=23, color=color).next_to(title, DOWN, buff=0.3)

        # ------------------------------------------------------------------
        # 1. Text & Write — Text objects are drawn stroke-by-stroke
        # ------------------------------------------------------------------
        c1 = header(
            "1. Text  —  Text() creates typography, Write() animates it", BLUE_B
        )
        demo1_a = Text("Hello,", font_size=44).shift(LEFT * 2.2 + DOWN * 0.3)
        demo1_b = Text(
            "Manim!", font_size=52, weight=BOLD, gradient=(BLUE, TEAL)
        ).next_to(demo1_a, RIGHT, buff=0.3)
        underline = Underline(demo1_b, color=TEAL, buff=0.12)

        self.play(FadeIn(c1, shift=UP * 0.15))
        self.play(Write(VGroup(demo1_a, demo1_b)))
        self.play(Create(underline))
        self.wait(0.7)
        self.play(FadeOut(c1), FadeOut(VGroup(demo1_a, demo1_b, underline)))
        self.wait(0.2)

        # ------------------------------------------------------------------
        # 2. Shapes & Create — geometric Mobjects
        # ------------------------------------------------------------------
        c2 = header("2. Shapes  —  Square / Circle / Triangle + Create()", RED_B)
        sq = Square(color=BLUE, fill_opacity=0.6, side_length=1.25)
        ci = Circle(color=RED, fill_opacity=0.6, radius=0.7)
        tr = Triangle(color=GREEN, fill_opacity=0.6).scale(0.85)
        arrow = Arrow(LEFT * 0.6, RIGHT * 0.6, buff=0, color=YELLOW, stroke_width=7)

        shapes = VGroup(sq, ci, tr, arrow).arrange(RIGHT, buff=0.6)
        shapes.move_to(ORIGIN).shift(DOWN * 0.35)
        if shapes.width > 12:
            shapes.scale(12 / shapes.width)

        labels = Text(
            "Create() traces each outline", font_size=20, color=GRAY_B
        ).next_to(shapes, DOWN, buff=0.45)

        self.play(FadeIn(c2, shift=UP * 0.15))
        self.play(Create(shapes, lag_ratio=0.25))
        self.play(FadeIn(labels, shift=UP * 0.1))
        self.wait(0.7)
        self.play(FadeOut(c2), FadeOut(shapes), FadeOut(labels))
        self.wait(0.2)

        # ------------------------------------------------------------------
        # 3. Animation & .animate — shift / rotate / scale / colour
        # ------------------------------------------------------------------
        c3 = header(
            "3. Animation  —  .animate moves, rotates, scales & recolours", GREEN
        )
        sq2 = Square(color=BLUE, fill_opacity=0.6, side_length=1.4).shift(
            LEFT * 2.5 + DOWN * 0.25
        )
        ci2 = Circle(color=RED, fill_opacity=0.6, radius=0.75).shift(DOWN * 0.25)
        tr2 = (
            Triangle(color=GREEN, fill_opacity=0.6)
            .scale(0.9)
            .shift(RIGHT * 2.5 + DOWN * 0.25)
        )
        trio = VGroup(sq2, ci2, tr2)
        hint = Text(
            ".animate.shift()  ·  .rotate()  ·  .scale()  ·  .set_fill()",
            font_size=18,
            color=GRAY_B,
        ).next_to(trio, DOWN, buff=0.5)

        self.play(FadeIn(c3, shift=UP * 0.15))
        self.play(FadeIn(trio, shift=UP * 0.15), FadeIn(hint, shift=UP * 0.1))
        self.wait(0.4)
        self.play(
            sq2.animate.shift(UP * 0.5).rotate(PI / 4),
            ci2.animate.scale(1.25).set_fill(YELLOW, opacity=0.8),
            tr2.animate.shift(UP * 0.5).set_fill(ORANGE, opacity=0.85),
            run_time=1.2,
        )
        self.wait(0.6)
        self.play(FadeOut(c3), FadeOut(trio), FadeOut(hint))
        self.wait(0.2)

        # ------------------------------------------------------------------
        # 4. VGroup — grouping objects for collective control
        # ------------------------------------------------------------------
        c4 = header("4. VGroup  —  group, arrange() & animate together", ORANGE)
        g_sq = Square(color=BLUE, fill_opacity=0.55, side_length=0.9)
        g_ci = Circle(color=RED, fill_opacity=0.55, radius=0.5)
        g_tr = Triangle(color=GREEN, fill_opacity=0.55).scale(0.6)
        grouped = VGroup(g_sq, g_ci, g_tr).arrange(RIGHT, buff=0.5)
        grouped.move_to(ORIGIN).shift(DOWN * 0.25)

        brace = Brace(grouped, DOWN, buff=0.18)
        brace_label = Text("one VGroup — one animation", font_size=20).next_to(
            brace, DOWN, buff=0.2
        )

        self.play(FadeIn(c4, shift=UP * 0.15))
        self.play(FadeIn(grouped, lag_ratio=0.15))
        self.play(GrowFromCenter(brace), FadeIn(brace_label, shift=UP * 0.1))
        self.wait(0.4)
        self.play(
            grouped.animate.shift(UP * 0.15).scale(1.15),
            brace.animate.shift(UP * 0.15).scale(1.15),
            brace_label.animate.shift(UP * 0.15).scale(1.05),
        )
        self.wait(0.5)
        self.play(FadeOut(c4), FadeOut(grouped), FadeOut(brace), FadeOut(brace_label))
        self.wait(0.2)

        # ------------------------------------------------------------------
        # 5. MathTex — LaTeX typesetting (previously clipped; now VGroup-scaled)
        # ------------------------------------------------------------------
        c5 = header("5. MathTex  —  LaTeX with MathTex() + Write()", PURPLE_B)
        # Each formula self-contained; stacked via VGroup so nothing leaves frame
        euler = MathTex(r"e^{i\pi} + 1 = 0", font_size=56)
        gauss = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}", font_size=40
        )
        basel = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}", font_size=40
        )

        euler_cap = Text("Euler's identity", font_size=16, color=GRAY_B).next_to(
            euler, UP, buff=0.12
        )
        gauss_cap = Text("Gaussian integral", font_size=16, color=GRAY_B).next_to(
            gauss, UP, buff=0.12
        )
        basel_cap = Text("Basel problem", font_size=16, color=GRAY_B).next_to(
            basel, UP, buff=0.12
        )

        g1 = VGroup(euler_cap, euler).arrange(DOWN, buff=0.1)
        g2 = VGroup(gauss_cap, gauss).arrange(DOWN, buff=0.1)
        g3 = VGroup(basel_cap, basel).arrange(DOWN, buff=0.1)
        formulas = VGroup(g1, g2, g3).arrange(DOWN, buff=0.45, aligned_edge=ORIGIN)
        if formulas.width > 11.5:
            formulas.scale(11.5 / formulas.width)
        if formulas.height > 4.8:
            formulas.scale(4.8 / formulas.height)
        formulas.move_to(ORIGIN).shift(DOWN * 0.3)

        self.play(FadeIn(c5, shift=UP * 0.15))
        self.play(Write(euler))
        self.play(FadeIn(euler_cap, shift=UP * 0.08))
        self.wait(0.3)
        self.play(FadeIn(g2, shift=UP * 0.12))
        self.wait(0.3)
        self.play(FadeIn(g3, shift=UP * 0.12))
        self.wait(0.7)
        # Final scale-to-fit demo: show all three were laid out as one safe VGroup
        self.play(Indicate(formulas, color=YELLOW, scale_factor=1.03))
        self.wait(0.4)
        self.play(FadeOut(c5), FadeOut(formulas))
        self.wait(0.2)

        # ------------------------------------------------------------------
        # 6. Axes & Graphs — coordinate systems and functions
        # ------------------------------------------------------------------
        c6 = header("6. Axes  —  Axes() + plot() for functions", TEAL)
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=7.2,
            y_length=3.2,
            axis_config={"color": GREY_B, "include_ticks": False},
            tips=False,
        ).scale(0.95)
        axes.move_to(ORIGIN).shift(DOWN * 0.45)
        if axes.height > 3.6:
            axes.scale(3.6 / axes.height)

        graph = axes.plot(
            lambda x: 0.9 * np.sin(2 * x), color=YELLOW, x_range=[-3.5, 3.5]
        )
        graph_label = MathTex(r"y = \sin(2x)", font_size=28, color=YELLOW).next_to(
            axes, UP, buff=0.2
        )

        self.play(FadeIn(c6, shift=UP * 0.15))
        self.play(Create(axes))
        self.play(Create(graph), FadeIn(graph_label, shift=DOWN * 0.1))
        self.wait(0.7)
        dot = Dot(color=RED).move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))
        self.play(
            dot.animate.move_to(axes.c2p(PI / 4, 0.9 * np.sin(PI / 2))), run_time=1.0
        )
        self.wait(0.4)
        self.play(FadeOut(c6), FadeOut(VGroup(axes, graph, graph_label, dot)))
        self.wait(0.2)

        # ------------------------------------------------------------------
        # Outro — all features at a glance
        # ------------------------------------------------------------------
        outro = Text("All features — one Scene, one construct()", font_size=28)
        outro.move_to(ORIGIN).shift(DOWN * 0.2)
        self.play(Write(outro))
        self.wait(0.8)
        self.play(outro.animate.scale(0.85).next_to(title, DOWN, buff=0.5))
        recap = Text(
            "Text  ·  Shapes  ·  Animation  ·  VGroup  ·  MathTex  ·  Axes",
            font_size=20,
            color=GRAY_B,
        ).next_to(outro, DOWN, buff=0.3)
        self.play(FadeIn(recap, shift=UP * 0.12))
        self.wait(1.0)
        self.play(FadeOut(VGroup(outro, recap)), FadeOut(title))
        self.wait(0.4)
