from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey 
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey 
from cryptography.hazmat.primitives import serialization 
from cryptography.exceptions import InvalidSignature 
import binascii

def generate_raw_keys():
  try:
    private_key = Ed25519PrivateKey.generate()
    
    raw_private_key = private_key.private_bytes_raw().hex()
  except Exception as e:
    print("Private key error:", e)
    
  try:
    public_key = private_key.public_key()
    
    raw_public_key = public_key.public_bytes_raw().hex()
  except Exception as e:
    print ("Public key error:", e)
    
  return raw_public_key, raw_private_key
