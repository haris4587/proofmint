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

- Tracked source: <https://github.com/haris4587/proofmint/blob/main/contracts/proofmint.py>
- Repository: <https://github.com/haris4587/proofmint>
- Live reviewer page: <https://proofmint.ansaf1st33.chatgpt.site/source>
- Studionet Explorer v2: pending deployment

## Deployment binding

The final submission must use the new ProofMint v2 address created from the exact
tracked `contracts/proofmint.py`. The rejected v1 address
`0xAd4Ae92FE7c0eb15E21f29346DE2Bfbaa2dC52F1` is historical and is not valid v2
evidence.

The deployment record must capture the selected Git commit, this file's raw URL,
its SHA-256 digest, its exact byte length, and the resulting ProofMint v2 address.
Those values are recorded externally after the commit is created so this evidence
file never claims a self-referential commit hash.

## Resubmission gate

ProofMint is ready to resubmit only when all three links are public and mutually
consistent:

1. GitHub contains the tracked Python source.
2. Explorer exposes a v2 deployment created from that source.
3. The live reviewer page links both of them directly.
