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

Completed v3 binding:

```text
Source commit: b03de3ec6fe9a9dbe4c5ffaa6be3cbaa1afe0639
Contract: 0x2E213ECc435D6475617cf13eA61065c6EcB865DC
Deploy transaction: 0x96271bdbefdee98240dec99842186f2e7d45f0f15f33084a6437f1022f519aa1
Source SHA-256: 25c0906d12ecd9bdfc00c375db748a426c6b98f16e3a143cda16daab5af358e0
Source byte length: 21325
Explorer contract: https://explorer-studio.genlayer.com/address/0x2E213ECc435D6475617cf13eA61065c6EcB865DC?tab=contract
```

The deploy transaction is `FINALIZED`, its GenVM execution is `SUCCESS`, and
Explorer's contract tab matches the tracked source hash and length exactly.

## 3. Execute the steward-path live test

Open a self-worker test milestone using a funded Studionet test value:

```text
worker: connected client address
title: ProofMint v3 revision timeout escape test
criteria: PASS only when the pinned artifact reports a complete deliverable,
          passing automated tests, and granted final approval. Incomplete but
          fixable work must be REVISION_REQUIRED rather than FAIL.
revision_window_seconds: 300
value: funded Studionet test value
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

Completed live record for milestone `0`:

```text
Open transaction: 0x5391935d4abee09b67e4d07798bef3fbfa8a87675828298a7a9a6f29737728fb
Evidence transaction: 0x611b6434b762a64f9b1cbda61ee21841aad34be68f621cdfba41dfe08146916a
Refund transaction: 0xeabf8444e23066b76a9dc94efe5a501c37fb37c6b597f626c4aee864e915ad93
Evidence result: REVISION_REQUIRED (FINALIZED / GenVM SUCCESS)
Revision window: 300 seconds
Revision deadline: 1788967766 (2026-09-09 15:29:26 UTC)
Final milestone status: REFUNDED
Final escrow balance: 0
Evidence versions: 1
Totals: total_released=0, total_refunded=total_funded, total_escrowed=0
```

All three calls are finalized on the same v3 address. The timeout refund was
submitted by the recorded client at/after the deadline and atomically zeroed the
remaining escrow. The terminal state prevents a second refund or later evidence.

## 4. Publication checks

- GitHub canonical and public source copies match.
- Explorer exposes the exact v3 deployed code and all eight public methods.
- README and `EVIDENCE.md` identify v1/v2 addresses as historical.
- Every v3 transaction link targets the v3 address.
- GitHub and Explorer are the authoritative v3 review links. Historical reviewer
  sites are deliberately excluded from the v3 deployment binding.

## Historical deployments

These addresses are preserved only for audit history and must not be submitted as
v3 proof:

```text
Rejected v1: 0xAd4Ae92FE7c0eb15E21f29346DE2Bfbaa2dC52F1
Superseded v2: 0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A
```
