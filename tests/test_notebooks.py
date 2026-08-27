"""Execute every notebook end to end. This is the promise the README makes."""
import pathlib
import time

import pytest

NOTEBOOKS = sorted((pathlib.Path(__file__).parent.parent / "notebooks").glob("*.ipynb"))


@pytest.mark.notebooks
@pytest.mark.slow
@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.stem)
def test_notebook_runs_clean(path):
    nbformat = pytest.importorskip("nbformat")
    from nbclient import NotebookClient

    nb = nbformat.read(path, as_version=4)
    t0 = time.perf_counter()
    NotebookClient(nb, timeout=900, kernel_name="python3",
                   resources={"metadata": {"path": str(path.parent)}},
                   allow_errors=True).execute()
    elapsed = time.perf_counter() - t0

    errors = [
        "".join(o["traceback"])[-1500:]
        for cell in nb.cells for o in cell.get("outputs", [])
        if o.get("output_type") == "error"
    ]
    assert not errors, f"{path.name} raised {len(errors)} error(s):\n" + "\n---\n".join(errors)
    assert elapsed < 600, f"{path.name} took {elapsed:.0f}s — too slow for a teaching notebook"


@pytest.mark.notebooks
@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.stem)
def test_notebook_outputs_are_stripped(path):
    """Committed notebooks carry no outputs: clean diffs, small repo, honest reviews."""
    import json

    nb = json.load(open(path))
    stray = [i for i, c in enumerate(nb["cells"]) if c.get("outputs")]
    assert not stray, f"{path.name} has outputs in cells {stray}. Run `make strip`."
