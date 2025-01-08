import pytest
from src.security.auth import SecurityManager
from unittest.mock import patch
import time

@pytest.fixture
def security_manager():
    return SecurityManager('test-project')

def test_token_generation(security_manager):
    with patch('google.auth.default') as mock_default:
        mock_creds = Mock()
        mock_creds.signing_key = 'test-key'
        mock_default.return_value = (mock_creds, 'test-project')
        
        token = security_manager.generate_token('1')
        assert token is not None

def test_token_verification(security_manager):
    test_token = 'test.token.here'
    result = security_manager.verify_token(test_token)
    assert result is None  # Invalid token should return None