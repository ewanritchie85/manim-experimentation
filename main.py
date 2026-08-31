import sys

from manim import *

from scenes.manim_maths_showcase import MathsShowcase
from scenes.test_scene import TestScene

SCENES = {
    "test": TestScene,
    "maths": MathsShowcase,
    "math": MathsShowcase,
    "manim_maths_showcase": MathsShowcase,
    "manim-maths-showcase": MathsShowcase,
    "showcase": MathsShowcase,
    "mathsshowcase": MathsShowcase,
    "mathshowcase": MathsShowcase,
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
        for sub in ("test", "maths"):
            print(f"Rendering {sub} in subprocess...")
            subprocess.run([sys.executable, str(this), sub], check=True)
    elif target in SCENES:
        SCENES[target]().render()
    else:
        available = ", ".join(sorted(SCENES)) + ", all"
        print(f"Unknown scene '{target}'. Available: {available}")
        print("Usage: python main.py [test|maths|all]")
        print("  or:  manim -pql scenes/test_scene.py TestScene")
        print("  or:  manim -pql scenes/manim_maths_showcase.py MathsShowcase")
        sys.exit(1)
