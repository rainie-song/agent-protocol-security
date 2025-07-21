import uuid
import json
import hashlib
from datetime import datetime, timedelta
from keys_generator import generate_raw_keys, sign_vc


def get_did(data):
    id = uuid.uuid4()
    id = 'did:ietf:' + str(id).replace('-', '')

    authentication = {
        'id': id+'#key-1',
        'type': data.get('pktype'),
        'controller': id,
        'publicKeyMultibase': data.get('pk')
    }

    vch = {
        'id': '',
        'issuer': '',
        'subjectId': '',
        'credentialHash': '',
        'signature': ''
    }

    did = {
        'id': id,
        'type': data.get('type'),
        'relatedID': '',
        'authentication': authentication,
        'description': data.get('description', ''),
        'protocol': data.get('protocol', ''),
        'transparency': data.get('transparency', ''),
        'verifiableCredentialHash': ''
    }

    return did

def get_vc(data):
    idm_did = read_json_to_dict('mcp/data/idm-did.json')

    claim = {
        'service': data.get('content')
    }

    cs = {
        'id': data.get('subjectID'),
        'claim': claim
    }

    current_time = datetime.now()

    vc = {
        'id': str(uuid.uuid4()),
        'type': 'VerifiableCredential',
        'issuer': idm_did['id'],
        'name': 'attributeCredential',
        'description': data.get('usage'),
        'validFrom': str(current_time),
        'validUntil': str(current_time + timedelta(hours=24)),
        'credentialSubject': cs,
        'relatedVC': '',
        'domain': 'ietf',
        'proof': ''
    }

    # hash_object = hashlib.sha256(str(vc).encode())
    # hex_dig = hash_object.hexdigest()

    with open('mcp/data/idm-sk.txt', 'r') as file:
        sk = file.read()

    signed_vc = sign_vc(sk, str(vc)).hex()

    proof = {
        'type': 'DataIntegrityProof',
        'verificationMethod': idm_did['id'],
        'cryptoSuite': data.get('keyType'),
        'proofPurpose': 'assertionMethod',
        'proofValue': signed_vc
    }

    vc['proof'] = proof

    save_vc(vc)

    return vc

def save_vc(vc):
    try:
        with open('mcp/data/vc.json', 'r') as file:
            vc_list = json.load(file)
    except FileNotFoundError:
        vc_list = []

    vc_list.append(vc)

    with open('mcp/data/vc.json', 'w') as file:
        json.dump(vc_list, file, indent=2)


def verify_vc(vc):
    try:
        with open('mcp/data/vc.json', 'r') as f:
            vc_list = json.load(f)
    except FileNotFoundError:
        print('FileNotFoundError')
        return False
    
    if vc in vc_list:
        return True

def read_json_to_dict(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'. Check file format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == '__main__':
    # Run only once to create IDM DID and save key pairs
    public_key, secret_key = generate_raw_keys()

    with open('mcp/data/idm-pk.txt', 'w') as file:
        file.write(public_key)
    with open('mcp/data/idm-sk.txt', 'w') as file:
        file.write(secret_key)

    data = {
        'type': 'IDM',
        'pk': public_key,
        'pktype': 'ed25519',
    }
    did = get_did(data)
    with open('mcp/data/idm-did.json', 'w') as file:
        json.dump(did, file, indent=2)