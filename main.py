import sys

from manim import *

from scenes.maths_tour import MathShowcase
from scenes.test_scene import TestScene
from scenes.vector_field import VectorFieldCurlDivergence

SCENES = {
    "test": TestScene,
    "vector": VectorFieldCurlDivergence,
    # alias with full class name and file stem
    "vector-field": VectorFieldCurlDivergence,
    "vector_field": VectorFieldCurlDivergence,
    "curl": VectorFieldCurlDivergence,
    "maths": MathShowcase,
    "math": MathShowcase,
    "tour": MathShowcase,
    "maths_tour": MathShowcase,
    "maths-tour": MathShowcase,
    "showcase": MathShowcase,
    "mathshowcase": MathShowcase,
}

if __name__ == "__main__":
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if target == "all":
        # Rendering multiple Scenes sequentially in the same process corrupts
        # manim's global config / output filename (second scene would
        # overwrite the first's mp4). Delegate to subprocesses so each Scene
        # gets a clean interpreter.
        import subprocess
        from pathlib import Path

        this = Path(__file__).resolve()
        for sub in ("test", "vector", "maths"):
            print(f"Rendering {sub} in subprocess...")
            subprocess.run([sys.executable, str(this), sub], check=True)
    elif target in SCENES:
        SCENES[target]().render()
    else:
        available = ", ".join(sorted(SCENES)) + ", all"
        print(f"Unknown scene '{target}'. Available: {available}")
        print("Usage: python main.py [test|vector|maths|all]")
        print("  or:  manim -pql scenes/test_scene.py TestScene")
        print("  or:  manim -pql scenes/vector_field.py VectorFieldCurlDivergence")
        print("  or:  manim -pql scenes/maths_tour.py MathShowcase")
        sys.exit(1)
