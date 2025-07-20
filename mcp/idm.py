import uuid
import datetime


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
    claim = {
        'service': data.get('content')
    }

    cs = {
        'id': uuid.uuid4(),
        'claim': claim
    }

    proof = {
        'type': '',
        'verificationMethod': '',
        'cryptoSuite': '',
        'proofPurpose': '',
        'proofValue': ''
    }

    vc = {
        'id': '',
        'type': '',
        'issuer': '',
        'name': '',
        'description': '',
        'validFrom': '',
        'validUntil': '',
        'credentialSubject': '',
        'relatedVC': '',
        'domain': 'ietf',
        'proof': ''
    }


if __name__ == '__main__':
    print('Hello World')