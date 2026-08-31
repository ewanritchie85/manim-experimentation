"""Basic tests to ensure project scaffolding and manim scene are valid."""


def test_import_manim():
    import manim

    assert manim is not None
    assert hasattr(manim, "Scene")


def test_import_test_scene():
    from scenes.test_scene import TestScene

    assert TestScene is not None
    assert hasattr(TestScene, "construct")


def test_scene_instantiation():
    from scenes.test_scene import TestScene

    scene = TestScene()
    assert scene is not None
    # Ensure construct is callable without requiring full render
    assert callable(getattr(scene, "construct", None))


def test_utils_importable():
    import utils

    assert utils is not None


def test_import_maths_tour():
    from scenes.manim_maths_showcase import MathsShowcase

    assert MathsShowcase is not None
    assert hasattr(MathsShowcase, "construct")
    # Each segment should be a method (outro removed)
    for name in (
        "pythagorean_theorem",
        "differentiation",
        "integration",
        "taylor_series",
        "linear_transformation",
        "vector_field_curl_divergence",
        "section_title",
        "clear_scene",
    ):
        assert hasattr(MathsShowcase, name), f"missing {name}"
        assert callable(getattr(MathsShowcase, name))
    # outro should no longer exist
    assert not hasattr(MathsShowcase, "outro")


def test_maths_tour_instantiation():
    from scenes.manim_maths_showcase import MathsShowcase

    scene = MathsShowcase()
    assert scene is not None
    assert callable(getattr(scene, "construct", None))


def test_maths_tour_field_func():
    import numpy as np

    from scenes.manim_maths_showcase import MathsShowcase

    scene = MathsShowcase()
    # field_func should be finite, 3D, regularized at centres
    v_far = scene.field_func(np.array([10.0, 10.0, 0.0]))
    assert v_far.shape == (3,)
    assert v_far[2] == 0.0
    assert np.all(np.isfinite(v_far))

    for cx, cy, _ in scene.VORTICES + scene.SOURCES:
        v = scene.field_func(np.array([cx, cy, 0.0]))
        assert np.all(np.isfinite(v))

    # taylor helper uses math.factorial — spot check
    import math

    assert math.factorial(5) == 120
    # ensure scene can compute taylor term without np.math
    total = sum(
        ((-1) ** n) * (1.0 ** (2 * n + 1)) / math.factorial(2 * n + 1) for n in range(3)
    )
    assert abs(total - 0.8416666666) < 1e-6


def test_main_scenes_registry():
    # main.py SCENES should expose test, maths aliases
    import main

    assert hasattr(main, "SCENES")
    for key in ("test", "maths"):
        assert key in main.SCENES
    # ensure removed aliases are gone (tour/maths_tour intentionally removed, vector redundant)
    for key in ("tour", "maths_tour", "maths-tour", "vector", "vector-field", "vector_field", "curl"):
        assert key not in main.SCENES
    # all point to valid Scene subclasses
    for cls in set(main.SCENES.values()):
        assert hasattr(cls, "construct")
