import pytest

import nanorag
from nanorag.bootstrap import bootstrap

bootstrap(verbose=False, allow_install=False)


@pytest.fixture(scope="session")
def system():
    """One built system shared by the whole test session."""
    bundle, index, pipe = nanorag.quickstart(**nanorag.TUNED, verbose=False)
    return bundle, index, pipe
