import pytest
from unittest.mock import patch, MagicMock
from app.core.workflow_service import WorkflowService


@pytest.fixture
def mock_load_config():
    """Mock the load_config function."""
    with patch("app.utils.config_loader.load_config", return_value={
        "1": "thumbnail",
        "2": "keywords",
        "3": "twitter",
        "4": "chatgpt",
        "5": "rabbitmq"
    }) as mock_config:
        yield mock_config


@pytest.fixture
def mock_rabbitmq_adapter():
    """Mock the RabbitMQAdapter class."""
    with patch("app.adapters.rabbitmq_adapter.RabbitMQAdapter") as MockRabbitMQAdapter:
        instance = MockRabbitMQAdapter.return_value
        instance.publish = MagicMock()
        instance.is_topic_available = MagicMock(return_value=True)
        yield instance


@pytest.fixture
def workflow_service(mock_load_config, mock_rabbitmq_adapter):
    """Fixture to initialize the WorkflowService with mocks."""
    return WorkflowService(rabbitmq_adapter=mock_rabbitmq_adapter)


def test_invalid_profile_id(workflow_service):
    """Test starting a workflow with an invalid profile ID."""
    with pytest.raises(ValueError, match="does not have a valid process type configured"):
        workflow_service.start_workflow("999", "content789")


@pytest.mark.parametrize("profile_id, process_type, id_content", [
    ("1", "thumbnail", "content123"),
    ("2", "keywords", "content456"),
])
def test_start_workflow(workflow_service, mock_rabbitmq_adapter, profile_id, process_type, id_content):
    """Test starting workflows for different process types."""
    workflow_id = workflow_service.start_workflow(profile_id, id_content)

    assert workflow_id is not None
    mock_rabbitmq_adapter.publish.assert_called_once_with(
        f"generator.{process_type}.process",
        {"workflow_id": workflow_id, "id_content": id_content}
    )


def test_rabbitmq_publish_failure(workflow_service, mock_rabbitmq_adapter):
    """Test handling a failure when publishing to RabbitMQ."""
    mock_rabbitmq_adapter.publish.side_effect = Exception("Publish failed")
    with pytest.raises(Exception, match="Publish failed"):
        workflow_service.start_workflow("1", "content123")


def test_basic():
    """Basic test to validate pytest setup."""
    assert 1 == 1
