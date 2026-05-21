from src import app as app_module


def test_root_redirects_to_static_index(test_client):
    # Arrange
    url = "/"

    # Act
    response = test_client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(test_client):
    # Arrange
    url = "/activities"

    # Act
    response = test_client.get(url)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert isinstance(payload, dict)


def test_signup_for_activity_adds_participant(test_client):
    # Arrange
    activity_name = "Math Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{activity_name}/signup"
    params = {"email": email}

    # Act
    response = test_client.post(url, params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/signup"
    params = {"email": email}

    # Act
    response = test_client.post(url, params=params)
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_existing_student(test_client):
    # Arrange
    activity_name = "Art Studio"
    email = "ava@mergington.edu"
    url = f"/activities/{activity_name}/participants"
    params = {"email": email}

    # Act
    response = test_client.delete(url, params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404(test_client):
    # Arrange
    activity_name = "Art Studio"
    email = "missingstudent@mergington.edu"
    url = f"/activities/{activity_name}/participants"
    params = {"email": email}

    # Act
    response = test_client.delete(url, params=params)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"


def test_signup_for_unknown_activity_returns_404(test_client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    url = f"/activities/{activity_name}/signup"
    params = {"email": email}

    # Act
    response = test_client.post(url, params=params)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
