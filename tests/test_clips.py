import os
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
CLIPS_DIR = REPO_ROOT / "clips"
CLIPS_FILES = [
    "knowledge_base.clp",
    "templates.clp",
    "sample_facts.clp",
]


def test_clips_files_exist():
    """Ensure the expected CLIPS files are present in the repository."""
    for fname in CLIPS_FILES:
        fpath = CLIPS_DIR / fname
        assert fpath.exists(), f"Missing CLIPS file: {fpath}"


def _has_clipspy():
    # Try to detect a usable CLIPS Python binding. Prefer the 'clips' module
    # from clipspy, but be tolerant if a different 'clips' package is installed.
    try:
        import clips
    except Exception:
        try:
            import clipspy as clips
        except Exception:
            return False

    # Ensure the module exposes an Environment-like class we can use
    return hasattr(clips, 'Environment') or hasattr(clips, 'Environment')


@pytest.mark.skipif(not _has_clipspy(), reason="clipspy is not installed; skipping runtime checks")
def test_load_and_run_with_clipspy():
    """Attempt to load the CLIPS files with clipspy and run the engine.

    This test will be skipped if `clipspy` (module name `clips`) is not installed.
    It verifies that loading the files and running the environment does not raise
    an exception and that the sample fact `user-profile` appears after running.
    """
    # Import a usable CLIPS binding. Try 'clips' first, then 'clipspy'. If the
    # module exists but doesn't provide an Environment class, skip the runtime
    # checks gracefully.
    try:
        import clips
    except Exception:
        import clipspy as clips

    if not hasattr(clips, 'Environment'):
        pytest.skip('Installed "clips" package does not expose Environment; skipping runtime checks')

    env = clips.Environment()

    # Load each CLP file into the environment
    for fname in CLIPS_FILES:
        path = str((CLIPS_DIR / fname).resolve())
        # env.load is the usual API; if unavailable this will raise and the test will fail
        env.load(path)

    # Reset and run the engine (the sample_facts.clp contains an assert of user-profile)
    env.reset()
    env.run()

    # Collect facts as strings and check for the user-profile fact
    facts = [str(f) for f in env.facts()]
    assert any("user-profile" in f or "user-profile" in f.lower() for f in facts), (
        "Expected 'user-profile' fact not found after running CLIPS files"
    )
