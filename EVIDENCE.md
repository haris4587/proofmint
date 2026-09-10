# ProofMint v3 — Steward Evidence Record

## Review claim

ProofMint v3 is a GenLayer Intelligent Contract that binds milestone adjudication
and GEN escrow settlement to exact immutable evidence while guaranteeing a
deterministic escape from `REVISION_REQUIRED`.

## Steward-requested lifecycle repair

The source now proves all of the following:

1. `open_milestone` records a client-selected revision window bounded to 300–
   2,592,000 seconds.
2. The first `REVISION_REQUIRED` decision sets `revision_deadline_unix` from the
   deterministic GenVM transaction timestamp.
3. Later revision decisions preserve that first deadline and cannot extend it.
4. The designated worker can resubmit only before the stored deadline.
5. At or after the deadline, only the recorded client can execute
   `claim_revision_timeout_refund`.
6. The refund transition writes `REFUNDED`, zeros `escrow_balance`, increments
   `total_refunded` by exactly the remaining escrow, then emits that exact transfer
   to the client.
7. The terminal state makes the refund single-use and blocks later submissions.
8. `total_escrowed = total_funded - total_released - total_refunded` makes the
   accounting invariant directly reviewable.

## Immutable evidence guarantees retained

- Only `raw.githubusercontent.com` URLs pinned to lowercase full 40-character
  commit SHAs are accepted.
- Validators require HTTP 200 and strict equality on SHA-256 and byte length.
- The caller's expected fingerprint must match the fetched bytes.
- The leader and custom validator independently re-fetch and re-hash the exact
  artifact during adjudication.
- Each evidence version remains append-only with its URL, expected/verified hash,
  length, verdict, score, breach flag, and summary.

## Verification results

```text
GenVM lint: PASS (3 checks)
GenVM semantic validation: PASS
Public methods: 8 (4 view, 4 write)
Direct tests: 9 passed
Canonical/public source byte comparison: PASS
Contract source SHA-256: 25c0906d12ecd9bdfc00c375db748a426c6b98f16e3a143cda16daab5af358e0
Contract source byte length: 21325
```

## Canonical v3 artifacts

- Repository: <https://github.com/haris4587/proofmint>
- Tracked source commit: <https://github.com/haris4587/proofmint/commit/b03de3ec6fe9a9dbe4c5ffaa6be3cbaa1afe0639>
- Tracked source: <https://github.com/haris4587/proofmint/blob/b03de3ec6fe9a9dbe4c5ffaa6be3cbaa1afe0639/contracts/proofmint.py>
- Raw tracked source: <https://raw.githubusercontent.com/haris4587/proofmint/b03de3ec6fe9a9dbe4c5ffaa6be3cbaa1afe0639/contracts/proofmint.py>
- Pinned test fixture: <https://raw.githubusercontent.com/haris4587/proofmint/b03de3ec6fe9a9dbe4c5ffaa6be3cbaa1afe0639/evidence/revision-timeout-demo.txt>
- ProofMint v3 Explorer contract: <https://explorer-studio.genlayer.com/address/0x2E213ECc435D6475617cf13eA61065c6EcB865DC?tab=contract>
- Public reviewer page: <https://proofmint.ansaf1st33.chatgpt.site/source>

## Deployment binding

The contract was deployed from the exact tracked source commit above:

```text
ProofMint v3 address: 0x2E213ECc435D6475617cf13eA61065c6EcB865DC
Deploy transaction: 0x96271bdbefdee98240dec99842186f2e7d45f0f15f33084a6437f1022f519aa1
Explorer: https://explorer-studio.genlayer.com/tx/0x96271bdbefdee98240dec99842186f2e7d45f0f15f33084a6437f1022f519aa1
Contract source SHA-256: 25c0906d12ecd9bdfc00c375db748a426c6b98f16e3a143cda16daab5af358e0
Contract source byte length: 21325
```

The deployment is `FINALIZED` with GenVM `SUCCESS`. Explorer's contract source
tab is byte-identical to the tracked source at the pinned commit.

## Live revision-timeout test

The funded self-worker test used milestone `0`, the commit-pinned
`evidence/revision-timeout-demo.txt` fixture, and a 300-second window:

```text
Open milestone: https://explorer-studio.genlayer.com/tx/0x5391935d4abee09b67e4d07798bef3fbfa8a87675828298a7a9a6f29737728fb
Evidence adjudication: https://explorer-studio.genlayer.com/tx/0x611b6434b762a64f9b1cbda61ee21841aad34be68f621cdfba41dfe08146916a
Timeout refund: https://explorer-studio.genlayer.com/tx/0xeabf8444e23066b76a9dc94efe5a501c37fb37c6b597f626c4aee864e915ad93
Evidence outcome: REVISION_REQUIRED
Revision deadline: 1788967766 (2026-09-09 15:29:26 UTC)
Final status: REFUNDED
Final escrow_balance: 0
Evidence version count: 1
total_funded: 1000000000000000000000000000000000
total_released: 0
total_refunded: 1000000000000000000000000000000000
total_escrowed: 0
```

The evidence transaction's equivalence outputs report HTTP 200, byte length 439,
the expected SHA-256, and `REVISION_REQUIRED`. After the fixed deadline, the
client-only refund finalized successfully, transferred the exact remaining
escrow, and left the terminal state with no escrow. The equality
`total_funded = total_refunded + total_released + total_escrowed` holds exactly.

## Historical evidence — not v3 proof

```text
Rejected v1 address: 0xAd4Ae92FE7c0eb15E21f29346DE2Bfbaa2dC52F1
Superseded v2 address: 0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A
V2 funded transaction: 0xe3a6cee2b3c21da388c234fd84c0ed06aba9720952ace356f2f478f4e3805862
V2 PASS transaction: 0xfcc0dcdde4d43dead8b13a38643dcabe3433817dae9edb6f068e37fe0e4d0030
```

Those records remain only as history. They do not claim that v3's timeout path
was present or exercised.
