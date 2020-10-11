Remote server part

## Install

Requirements:

- jwcrypto
- cryptography
- pyopenssl
- flask

cacert = workstation001 (self signed)

checks:

- included cert validity
- cert chain until cacert
- cert chain not revoked
- token signature with included cert
- request parameters (nonce)
- cert cn vs system hostname
- system information parameters

Todo:

- https
- separate files
