
# Project: Proof-of-Work-блокчейн  

## Goals:

1. To make the hash-function GOST R 34.11-2018 (Streebog-256) 
2. Compute randomizer with h0 = H(Full name, 512 bits), hi = H(h0||i)
3. Implement the key-prefixed Schnorr signature ( use parameters p, q, g from example A.3 of GOST R 34.10-94)  
4. To generate 5 200 bits each transactions with one transaction containing Full Name; sigh all five transactions with Schnorr signature 
5. Compute the Merkle root for those 5 made signed transactions by any realization at 2.3 in practice's paper
6. To construct a block header and find a nonce such that the first 5 bits of Streebog-256 ( block_header ) are all equall to zero  