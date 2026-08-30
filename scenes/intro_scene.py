from manim import *

class IntroScene(Scene):
    def construct(self):
        title = Text("Experiments with Manim").scale(1.2)
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
            triangle.animate.shift(UP)
        )
        self.wait(0.5)
        
        self.play(
            square.animate.rotate(PI/4),
            circle.animate.scale(1.5),
            triangle.animate.set_fill(YELLOW, opacity=0.9)
        )
        self.wait(0.5)
        
        group = VGroup(square, circle, triangle)
        self.play(FadeOut(group), FadeOut(title))
        self.wait(0.5)
        
        formula = Text("e^{iπ} + 1 = 0", font_size=72)
        self.play(Write(formula))
        self.wait(1)