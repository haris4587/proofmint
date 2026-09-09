# ProofMint v3 Deployment and Verification Record

## Steward requirement

The v2 lifecycle could leave escrow permanently locked after
`REVISION_REQUIRED`. ProofMint v3 adds a bounded, fixed revision deadline and the
client-only `claim_revision_timeout_refund` terminal transition. Source, tests,
deployment, and live evidence must all describe this same v3 implementation.

## 1. Verify the tracked source

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/genvm-lint check contracts/proofmint.py
.venv/bin/python -m pytest tests/direct -q
cmp contracts/proofmint.py public/proofmint.py
```

Required result:

```text
GenVM lint and semantic validation: PASS
Direct tests: 9 passed
Canonical and public source copies: byte-identical
```

## 2. Deploy the exact tracked contract

1. Open <https://studio.genlayer.com/>.
2. Use Studionet with simulation mode disabled.
3. Load the exact `contracts/proofmint.py` bytes from the recorded source commit.
4. Deploy with no constructor arguments and wait for accepted/finalized success.
5. Compare the Explorer contract code with the tracked source.

Final v3 source commit, address, transaction, source SHA-256, and byte length are
recorded after deployment; no placeholder is evidence.

## 3. Execute the steward-path live test

Open a self-worker test milestone using a small Studionet GEN amount:

```text
worker: connected client address
title: ProofMint v3 revision timeout escape test
criteria: PASS only when the pinned artifact reports a complete deliverable,
          passing automated tests, and granted final approval. Incomplete but
          fixable work must be REVISION_REQUIRED rather than FAIL.
revision_window_seconds: 300
value: small Studionet test amount
```

Submit the immutable raw URL for
`evidence/revision-timeout-demo.txt`, pinned to the full source commit, with its
exact SHA-256 and byte length. The fixture intentionally describes fixable,
incomplete work and should produce `REVISION_REQUIRED`.

Verify `get_milestone(id)` stores:

- `status = REVISION_REQUIRED`;
- the original full `escrow_balance`;
- `revision_window_seconds = 300`;
- a nonzero `revision_deadline_unix` equal to the evidence transaction timestamp
  plus 300 seconds.

At or after that deadline, call `claim_revision_timeout_refund(id)` from the
client. Verify the final state is `REFUNDED`, escrow is zero, `total_refunded`
increased once, and `total_escrowed` returned to zero. A second refund call and a
late worker resubmission must be rejected by the terminal state.

## 4. Publication checks

- GitHub canonical and public source copies match.
- Explorer exposes the exact v3 deployed code and all eight public methods.
- README and `EVIDENCE.md` identify v1/v2 addresses as historical.
- Every v3 transaction link targets the v3 address.
- The public reviewer page, if retained as evidence, links the v3 repository and
  v3 Explorer deployment rather than the superseded v2 address.

## Historical deployments

These addresses are preserved only for audit history and must not be submitted as
v3 proof:

```text
Rejected v1: 0xAd4Ae92FE7c0eb15E21f29346DE2Bfbaa2dC52F1
Superseded v2: 0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A
```
