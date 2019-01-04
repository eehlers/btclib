#!/usr/bin/env python3

# Copyright (C) 2017-2019 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from hashlib import sha256
from btclib.base58 import b58encode, b58encode_check, b58decode, b58decode_check

# https://en.bitcoin.it/wiki/Wallet_import_format
print("\n****** Private ECDSA Key to WIF ******")

print("\n*** [1] Private ECDSA Key:")
q = 0xC28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D
print(hex(q))

print("\n*** [2] 0x80 Extended Key:")
ExtKey = b'\x80' + q.to_bytes(32, 'big')
print(ExtKey.hex())

print("\n*** [3] SHA-256 hashing of the Extended Key:")
h1 = sha256(ExtKey).digest()
print(h1.hex())

print("\n*** [4] SHA-256 hashing of the SHA-256:")
h2 = sha256(h1).digest()
print(h2.hex())

print("\n*** [5] First 4 bytes of the second SHA-256 hash used as address checksum:")
print(h2[:4].hex())

print("\n*** [6] checksum added at the end of extended key:")
addr = ExtKey + h2[:4]
print(addr.hex())

print("\n*** [7] Base58 encoding")
wif = b58encode(addr)
print(wif)
assert wif == b'5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ', "failure"
assert b58encode_check(ExtKey) == b'5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ', "failure"

print("\n****** WIF to private key ******")

print("\n*** [1] Base58 WIF")
print(wif)
compressed = len(wif)-51
print ("compressed" if (compressed==1) else "uncompressed")

print("\n*** [2] Base58 decoding")
addr = b58decode(wif)
print(addr.hex())

print("\n*** [3] Extended key (checksum verified)")
ExtKey, checksum = addr[:-4], addr[-4:]
verified = ( sha256(sha256(ExtKey).digest()).digest()[:4]==checksum )
print(ExtKey.hex() + " (" + ("true" if verified else "false") + ")")
print(b58decode_check(wif).hex())

print("\n*** [4] Private key")
q2 = ExtKey[1:-1].hex() if compressed else ExtKey[1:].hex()
assert int(q2, 16) == q, "failure"
print(q2)
