import pytest

import fde_rag
from fde_rag.bootstrap import bootstrap

bootstrap(verbose=False, allow_install=False)


@pytest.fixture(scope="session")
def system():
    """One built system shared by the whole test session."""
    bundle, index, pipe = fde_rag.quickstart(**fde_rag.TUNED, verbose=False)
    return bundle, index, pipe
