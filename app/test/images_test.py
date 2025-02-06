import pytest
import warnings
from unittest.mock import MagicMock

from app.model.users import Users  # Import your actual User model
from app.db.session import get_db  # Import your DB session function
from app.repository.images import get_user_id_by_user_id  # Import your function

# Sample user data
mock_user = Users(id=1, userId="P1001", username="testuser")

@pytest.fixture
def mock_db():
    """Mock the database session"""
    db = MagicMock()
    return db

def test_get_user_id_by_user_id_found(mock_db):
    """Test when user is found"""
    # Mock the query to return a user object

    print("SHITTTTTTTTTTTTTT")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    user_id = get_user_id_by_user_id(mock_db, "P1001")
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print(user_id.username)
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    warnings.warn(UserWarning("api v1, should use functions from v2"))
    # mock_user = Users(id=1, user_id="P1001", username="testuser") 


    assert user_id.id == 1  # Expecting the returned ID to be 1

def test_get_user_id_by_user_id_not_found(mock_db):
    """Test when user is NOT found"""
    # Mock the query to return None
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        get_user_id_by_user_id(mock_db, "P9999")  # Non-existing user
