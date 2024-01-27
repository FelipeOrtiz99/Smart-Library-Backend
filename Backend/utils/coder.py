import hashlib

def pass_sha256(input):
    encoded_text = input.encode('utf-8')
    sha256_hash = hashlib.sha256(encoded_text).hexdigest()
    return sha256_hash

def verified_hashes(input, password):
    if input == password:
        return True
    else:
        return False