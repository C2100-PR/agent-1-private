from google.cloud import secretmanager
from google.auth import default
from typing import Optional
import jwt
import time

class SecurityManager:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.secret_client = secretmanager.SecretManagerServiceClient()

    def generate_token(self, agent_id: str, expiry: int = 3600) -> str:
        credentials, project = default()
        token = jwt.encode(
            {
                'agent_id': agent_id,
                'exp': time.time() + expiry,
                'iat': time.time(),
                'iss': f'agent-{agent_id}@{self.project_id}.iam.gserviceaccount.com'
            },
            credentials.signing_key,
            algorithm='RS256'
        )
        return token

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            decoded = jwt.decode(
                token,
                options={'verify_signature': True}
            )
            return decoded if time.time() < decoded['exp'] else None
        except:
            return None