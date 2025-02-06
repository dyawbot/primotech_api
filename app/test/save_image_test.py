import pytest
from unittest.mock import AsyncMock, MagicMock

from app.model.users import Users
from app.model.users import Images
from app.repository.images import save_image_data
from app.schemas.users import ImagesUsersSchema
from app.model.helper import StatusHelper, UserImageHelper

@pytest.fixture
def mock_db():
    """Mock the database session"""
    db = MagicMock()
    db.commit = AsyncMock()  # Mock async commit
    db.refresh = AsyncMock()  # Mock async refresh
    return db

@pytest.mark.asyncio  # Required for testing async functions
async def test_save_image_data_success(mock_db):
    """Test saving image data successfully"""

    # Mock user object
    mock_user = Users(id=1, userId="P1001", username="testuser")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    # Mock image data input
    image_input = UserImageHelper(image_name="test.jpg", image_path="path/to/image", username="P1001")

    # Call async function
    result = await save_image_data(mock_db, image_input)
    # print(result.json())
    print(result.result.__dict__)
    print(result.result)
    # Assertions
    assert isinstance(result, StatusHelper)
    assert result.code == 200
    assert result.status == "OK"
    assert result.message == "User save an image successfully"
    assert result.result.image_name == "test.jpg"
    assert result.result.image_page == "path/to/image"
    assert result.result.user_id == 1

@pytest.mark.asyncio
async def test_save_image_data_user_not_found(mock_db):
    """Test when user is not found"""
    mock_db.query.return_value.filter.return_value.first.return_value = None  # No user found

    image_input = UserImageHelper(image_name="test.jpg", image_path="path/to/image", username="999")

    result = await save_image_data(mock_db, image_input)

    assert isinstance(result, StatusHelper)
    assert result.code == 500  # Expected failure since user not found
    assert result.status == "Error"
