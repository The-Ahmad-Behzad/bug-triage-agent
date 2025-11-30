"""Tests for database operations"""

import pytest
from unittest.mock import Mock, patch
from src.database.team_members import (
    create_team_member,
    get_team_member,
    update_team_member,
    query_by_language,
    query_by_skills,
    query_by_module
)
from src.database.module_ownership import (
    get_module_owners,
    get_modules_by_language
)
from src.database.developer_load import (
    get_developer_load,
    update_developer_load
)


@pytest.fixture
def mock_collection():
    """Mock MongoDB collection"""
    return Mock()


@patch('src.database.team_members.get_team_members_collection')
def test_create_team_member(mock_get_collection, mock_collection):
    """Test creating a team member"""
    mock_get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = None  # Member doesn't exist
    mock_collection.insert_one.return_value = Mock(inserted_id="test_id")
    
    member_data = {
        "member_id": "dev-01",
        "name": "Test Developer",
        "skills": {
            "languages": ["python", "java"],
            "frameworks": ["django"],
            "domains": ["backend"]
        }
    }
    
    result = create_team_member(member_data)
    assert result == "dev-01"
    mock_collection.insert_one.assert_called_once()


@patch('src.database.team_members.get_team_members_collection')
def test_get_team_member(mock_get_collection, mock_collection):
    """Test getting a team member"""
    mock_get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = {
        "_id": "test_id",
        "member_id": "dev-01",
        "name": "Test Developer"
    }
    
    result = get_team_member("dev-01")
    assert result is not None
    assert result["member_id"] == "dev-01"
    assert result["name"] == "Test Developer"


@patch('src.database.team_members.get_team_members_collection')
def test_query_by_language(mock_get_collection, mock_collection):
    """Test querying team members by language"""
    mock_get_collection.return_value = mock_collection
    mock_collection.find.return_value = [
        {
            "_id": "test_id_1",
            "member_id": "dev-01",
            "name": "Python Developer",
            "skills": {"languages": ["python"]}
        }
    ]
    
    result = query_by_language("python")
    assert len(result) == 1
    assert result[0]["member_id"] == "dev-01"


@patch('src.database.module_ownership.get_module_ownership_collection')
def test_get_module_owners(mock_get_collection, mock_collection):
    """Test getting module owners"""
    mock_get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = {
        "module_name": "auth",
        "owners": ["dev-01", "dev-02"]
    }
    
    result = get_module_owners("auth")
    assert len(result) == 2
    assert "dev-01" in result
    assert "dev-02" in result


@patch('src.database.developer_load.get_developer_load_collection')
def test_get_developer_load(mock_get_collection, mock_collection):
    """Test getting developer load"""
    mock_get_collection.return_value = mock_collection
    mock_collection.find_one.return_value = {
        "_id": "test_id",
        "member_id": "dev-01",
        "current_load_score": 0.5
    }
    
    result = get_developer_load("dev-01")
    assert result is not None
    assert result["member_id"] == "dev-01"
    assert result["current_load_score"] == 0.5



