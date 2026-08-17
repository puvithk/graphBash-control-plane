
import secrets
class TokenUtils():
    def generate_node_registration_token(self) -> str:
        return secrets.token_hex(32)


if __name__ == "__main__" :

    token_utils = TokenUtils()
    print(token_utils.generate_node_registration_token())