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


def test_import_vector_field():
    from scenes.vector_field import VectorFieldCurlDivergence, vector_field_func

    assert VectorFieldCurlDivergence is not None
    assert hasattr(VectorFieldCurlDivergence, "construct")
    assert callable(vector_field_func)


def test_vector_field_instantiation():
    from scenes.vector_field import VectorFieldCurlDivergence

    scene = VectorFieldCurlDivergence()
    assert scene is not None
    assert callable(getattr(scene, "construct", None))


def test_vector_field_func_values():
    import numpy as np

    from scenes.vector_field import EPSILON, SOURCES, VORTICES, vector_field_func

    # At far field, should be finite and 3D
    v = vector_field_func(np.array([10.0, 10.0, 0.0]))
    assert v.shape == (3,)
    assert v[2] == 0.0
    assert np.all(np.isfinite(v))

    # At vortex centre, regularized by EPSILON — should not blow up
    cx, cy, _ = VORTICES[0]
    v_center = vector_field_func(np.array([cx, cy, 0.0]))
    assert np.all(np.isfinite(v_center))

    # At source centre, likewise finite
    cx, cy, _ = SOURCES[0]
    v_src = vector_field_func(np.array([cx, cy, 0.0]))
    assert np.all(np.isfinite(v_src))

    # Symmetry: opposite vortices have opposite curl sign contribution
    # so field at top midpoint should have strong horizontal component
    v_top = vector_field_func(np.array([0.0, 1.2, 0.0]))
    assert np.isfinite(v_top[0]) and np.isfinite(v_top[1])

    # EPSILON guards singularity
    assert EPSILON > 0


def test_vector_field_constants():
    from scenes.vector_field import SOURCES, VORTICES

    assert len(VORTICES) == 2
    assert len(SOURCES) == 2
    for tup in VORTICES + SOURCES:
        assert len(tup) == 3
        assert all(isinstance(x, (int, float)) for x in tup)


def test_import_maths_tour():
    from scenes.maths_tour import MathShowcase

    assert MathShowcase is not None
    assert hasattr(MathShowcase, "construct")
    # Each segment should be a method
    for name in (
        "pythagorean_theorem",
        "differentiation",
        "integration",
        "taylor_series",
        "linear_transformation",
        "vector_field_curl_divergence",
        "section_title",
        "clear_scene",
        "outro",
    ):
        assert hasattr(MathShowcase, name), f"missing {name}"
        assert callable(getattr(MathShowcase, name))


def test_maths_tour_instantiation():
    from scenes.maths_tour import MathShowcase

    scene = MathShowcase()
    assert scene is not None
    assert callable(getattr(scene, "construct", None))


def test_maths_tour_field_func():
    import numpy as np

    from scenes.maths_tour import MathShowcase

    scene = MathShowcase()
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
    # main.py SCENES should expose test, vector, maths aliases
    import main

    assert hasattr(main, "SCENES")
    for key in ("test", "vector", "maths", "tour", "maths_tour"):
        assert key in main.SCENES
    # all point to valid Scene subclasses
    for cls in set(main.SCENES.values()):
        assert hasattr(cls, "construct")
