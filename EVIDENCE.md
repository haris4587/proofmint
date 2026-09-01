# ProofMint v2 — Reviewer Evidence Record

## Review claim

ProofMint v2 is a GenLayer Intelligent Contract that binds milestone adjudication
and GEN escrow settlement to one exact, immutable evidence version.

## What the source demonstrates

- `open_milestone` is payable and records the client, designated worker, natural-
  language criteria, criteria SHA-256, funded amount, and escrow balance.
- Evidence is restricted to `raw.githubusercontent.com` URLs pinned to a lowercase
  full 40-character commit SHA.
- The contract fetches the artifact and verifies HTTP status, maximum size,
  SHA-256, and exact byte length through strict validator equality.
- The leader and custom validator independently re-fetch and re-hash the exact
  artifact during adjudication.
- `PASS` releases GEN to the worker; `REVISION_REQUIRED` holds escrow; demonstrated
  material `FAIL` refunds the client.
- Each evidence version is appended with URL, expected hash, verified hash, byte
  length, decision, score, material-breach flag, and summary.

## Local verification completed

```text
GenVM lint: PASS
GenVM semantic validation: PASS
Contract: ProofMint
Public methods: 7 (4 view, 3 write)
Direct tests: 7 passed
Site production build: PASS
Frontend tests: 5 passed
```

## Canonical artifacts

- Tracked source: <https://github.com/haris4587/proofmint/blob/da7839cb86865db1308e0888d8059649604e0126/contracts/proofmint.py>
- Raw tracked source: <https://raw.githubusercontent.com/haris4587/proofmint/da7839cb86865db1308e0888d8059649604e0126/contracts/proofmint.py>
- Repository: <https://github.com/haris4587/proofmint>
- Live reviewer page: <https://proofmint.ansaf1st33.chatgpt.site/source>
- Studionet Explorer v2: <https://explorer-studio.genlayer.com/address/0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A?tab=contract>

## Deployment binding

The ProofMint v2 deployment was created from the exact tracked
`contracts/proofmint.py` at commit
`da7839cb86865db1308e0888d8059649604e0126`.

```text
ProofMint v2 address: 0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A
Contract source SHA-256: a90e593eb7ee2eabfe5e4102e8584873a214ae31cd28763b35ac3d6fbe6bc3b5
Contract source byte length: 17452
```

The rejected v1 address
`0xAd4Ae92FE7c0eb15E21f29346DE2Bfbaa2dC52F1` is historical and is not valid v2
evidence.

The deployment record must capture the selected Git commit, this file's raw URL,
its SHA-256 digest, its exact byte length, and the resulting ProofMint v2 address.
Those values are recorded externally after the commit is created so this evidence
file never claims a self-referential commit hash. The immutable raw URL and
fingerprint for an adjudication are calculated after this record is committed.

## Live Studionet consensus record

```text
Milestone ID: 0
Fund transaction: 0xe3a6cee2b3c21da388c234fd84c0ed06aba9720952ace356f2f478f4e3805862
Evidence transaction: 0xfcc0dcdde4d43dead8b13a38643dcabe3433817dae9edb6f068e37fe0e4d0030
Evidence snapshot commit: bbb4d39dbd8a3e4581e029c1b3f06fffd76ac4ab
Evidence SHA-256: c29456e41c828b6976d29e762827c87dace201b4cafcaccb1f1aa104197f5923
Evidence byte length: 2980
Consensus: FINALIZED / MAJORITY_AGREE
Validator votes: 3 AGREE, 1 DISAGREE, 1 IDLE after quorum
Outcome: PASS
Score: 100/100
Evidence version: 1
Settlement: RELEASED
GEN funded: 0.01
GEN released: 0.01
Escrow remaining: 0
```

The accepted contract state stores the exact immutable URL, matching expected and
verified hashes, byte length 2,980, the PASS decision summary, score 100, and
evidence version 1. The full funded escrow was released to the designated worker.

## Resubmission gate

ProofMint is ready to resubmit only when all three links are public and mutually
consistent:

1. GitHub contains the tracked Python source.
2. Explorer exposes a v2 deployment created from that source.
3. The live reviewer page links both of them directly.
4. A funded full-consensus transaction stores PASS and releases escrow on-chain.
