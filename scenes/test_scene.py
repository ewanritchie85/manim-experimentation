from manim import *


class TestScene(Scene):
    def construct(self):
        title = Text("Experimenting with Manim").scale(1.2)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        square = Square(color=BLUE, fill_opacity=0.7)
        circle = Circle(color=RED, fill_opacity=0.7).next_to(square, RIGHT, buff=1)
        triangle = Triangle(color=GREEN, fill_opacity=0.7).next_to(square, LEFT, buff=1)

        self.play(Create(square), Create(circle), Create(triangle))
        self.wait(0.5)

        self.play(
            square.animate.shift(UP),
            circle.animate.shift(DOWN),
            triangle.animate.shift(UP),
        )
        self.wait(0.5)

        self.play(
            square.animate.rotate(PI / 4),
            circle.animate.scale(1.5),
            triangle.animate.set_fill(YELLOW, opacity=0.9),
        )
        self.wait(0.5)

        group = VGroup(square, circle, triangle)
        self.play(FadeOut(group), FadeOut(title))
        self.wait(0.5)

        formula = MathTex(r"e^{i\pi} + 1 = 0", font_size=72)
        self.play(Write(formula))
        self.wait(1)

        # More LaTeX examples
        integrals = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
            font_size=60
        ).next_to(formula, DOWN, buff=1)
        self.play(Write(integrals))
        self.wait(1)

        sum_formula = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
            font_size=60
        ).next_to(integrals, DOWN, buff=0.8)
        self.play(Write(sum_formula))
        self.wait(1)

        self.play(FadeOut(formula), FadeOut(integrals), FadeOut(sum_formula))
        self.wait(0.5)
