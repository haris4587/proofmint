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
- Tracked source commit: pending
- Tracked source: pending
- Raw tracked source: pending
- ProofMint v3 Explorer contract: pending
- Public reviewer page: <https://proofmint.ansaf1st33.chatgpt.site/source>

## Deployment binding

The v3 address, deployment transaction, exact source commit, source SHA-256, and
source byte length are inserted only after the contract is deployed from the
verified tracked bytes.

## Live revision-timeout test

The live test will fund a self-worker milestone, submit the commit-pinned
`evidence/revision-timeout-demo.txt` fixture, obtain `REVISION_REQUIRED`, wait for
its 300-second fixed deadline, and execute the client-only timeout refund. The
final record will include transaction links and reads proving `REFUNDED`, zero
escrow, and exact totals.

## Historical evidence — not v3 proof

```text
Rejected v1 address: 0xAd4Ae92FE7c0eb15E21f29346DE2Bfbaa2dC52F1
Superseded v2 address: 0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A
V2 funded transaction: 0xe3a6cee2b3c21da388c234fd84c0ed06aba9720952ace356f2f478f4e3805862
V2 PASS transaction: 0xfcc0dcdde4d43dead8b13a38643dcabe3433817dae9edb6f068e37fe0e4d0030
```

Those records remain only as history. They do not claim that v3's timeout path
was present or exercised.
