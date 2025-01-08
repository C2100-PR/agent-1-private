import pytest
from unittest.mock import Mock, patch
from src.agent_core.base import BaseAgent

@pytest.fixture
def mock_secret_manager():
    with patch('google.cloud.secretmanager.SecretManagerServiceClient') as mock:
        mock_response = Mock()
        mock_response.payload.data.decode.return_value = 'test-api-key'
        mock.return_value.access_secret_version.return_value = mock_response
        yield mock

def test_agent_initialization(mock_secret_manager):
    agent = BaseAgent('1')
    assert agent.agent_id == '1'
    assert agent.api_key == 'test-api-key'

@pytest.mark.asyncio
async def test_process_request():
    with patch('src.agent_core.base.BaseAgent._get_api_key') as mock_key:
        mock_key.return_value = 'test-key'
        agent = BaseAgent('1')
        response = await agent.process_request('test input')
        assert response is not None