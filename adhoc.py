authorization_token_file_path = 'auth_token.txt'
authorization_token_file_descriptor = io.open(authorization_token_file_path, 'r', newline='' )
AUTHORIZATION_TOKEN = authorization_token_file_descriptor.read().rstrip()