
import hashlib
import secrets
import os
class TokenUtils():
    def generate_node_registration_token(self) -> str:
        return secrets.token_hex(32)
    
    def generate_node_api_key(self) -> str:
        #Change this once production 
        return "NP_" + secrets.token_urlsafe(32)

    def generate_node_api_key_has(self , api_key) -> str:
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def verify_node_api_key(self , api_key , api_key_hash) -> bool:
        return self.generate_node_api_key_has(api_key) == api_key_hash
    
if __name__ == "__main__" :

    token_utils = TokenUtils()
    print(token_utils.generate_node_registration_token())
    print(token_utils.generate_node_api_key())
    print(token_utils.generate_node_api_key_has(token_utils.generate_node_api_key()))