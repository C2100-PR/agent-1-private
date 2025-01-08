import pytest
from unittest.mock import Mock, patch
from src.agent_core.knowledge_manager import KnowledgeManager

@pytest.fixture
def mock_storage():
    with patch('google.cloud.storage.Client') as mock:
        mock_bucket = Mock()
        mock_blob = Mock()
        mock_blob.download_as_string.return_value = b'{"test": "data"}'
        mock_bucket.blob.return_value = mock_blob
        mock.return_value.bucket.return_value = mock_bucket
        yield mock

def test_load_knowledge_base(mock_storage):
    km = KnowledgeManager('test-bucket', 'test-prefix')
    kb = km.load_knowledge_base()
    assert kb == {"test": "data"}