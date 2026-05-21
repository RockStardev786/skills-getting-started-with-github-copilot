import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


def create_test_client():
    return TestClient(app_module.app)


def reset_activities(original_activities):
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))


@pytest.fixture(scope="function")
def test_client():
    original_activities = copy.deepcopy(app_module.activities)
    client = create_test_client()

    try:
        yield client
    finally:
        reset_activities(original_activities)
