# ProofMint v3 — Deadline-Safe Immutable Evidence Escrow

ProofMint is a GenLayer Intelligent Contract for version-bound milestone escrow.
A client funds a milestone in native GEN and designates one worker. The worker
submits an immutable GitHub artifact, its SHA-256, and exact byte length. The
contract independently verifies those bytes before GenLayer validators judge the
artifact against the stored natural-language acceptance criteria. Each milestone
also commits to a client-selected revision window of 300 to 2,592,000 seconds.

The settlement result is deterministic:

- `PASS` releases escrow to the designated worker.
- `REVISION_REQUIRED` starts one fixed revision deadline and permits another
  immutable version only before that deadline.
- `FAIL` with a demonstrated material breach refunds the client.
- When the fixed revision deadline expires, only the client can call
  `claim_revision_timeout_refund` to recover the full remaining escrow.
- A client may cancel and recover escrow only before the first submission.

## Why v3 exists

A steward found that v2 escrow could remain locked forever after
`REVISION_REQUIRED` if the worker stopped resubmitting. v3 closes that lifecycle
gap with a deterministic, authorized, fully accounted timeout transition.

- The client chooses a bounded revision window when funding the milestone.
- The worker accepts that on-chain term by choosing to submit the first evidence.
- The first `REVISION_REQUIRED` result stores `revision_deadline_unix` using the
  deterministic GenVM transaction timestamp.
- Later revisions preserve the first deadline; a worker cannot extend it.
- Worker resubmission is rejected at or after the deadline.
- At or after the deadline, only the client may atomically zero escrow, increment
  `total_refunded`, transition to `REFUNDED`, and receive the full balance.
- The terminal status prevents a second refund or any later evidence submission.
- `get_totals()` exposes `total_escrowed`, so reviewers can verify
  `funded = released + refunded + escrowed`.

## Why v2 existed

The original ProofMint submission was rejected because its Studio link opened the
Studio application instead of exposing reviewable contract source. v2 fixes the
review path and materially strengthens the protocol itself:

- canonical public GitHub repository with tracked `contracts/proofmint.py`;
- matching GenLayer Explorer deployment address;
- public `/source` page linking both artifacts;
- native GEN escrow rather than a decision-only prototype;
- immutable evidence binding instead of a mutable HTTPS URL;
- append-only evidence versions and explicit settlement accounting.

The rejected v1 and superseded v2 deployments are historical and must not be used
as proof of v3.

## Revision escape invariant

The deadline is exclusive for the worker and inclusive for the client: evidence
may be resubmitted only while `transaction_timestamp < revision_deadline_unix`;
the timeout refund becomes available when
`transaction_timestamp >= revision_deadline_unix`. There is no overlap and no
unowned time gap. Because later `REVISION_REQUIRED` outcomes preserve the first
deadline, repeated submissions cannot postpone the client escape path.

## Immutable evidence invariant

ProofMint accepts evidence only when every condition below is satisfied:

1. The URL begins with `https://raw.githubusercontent.com/`.
2. It contains an owner, repository, lowercase full 40-character commit SHA,
   and file path.
3. It has no query string or fragment.
4. The fetched response is HTTP 200 and no larger than 500,000 bytes.
5. Validators reach strict equality on the fetched SHA-256 and byte length.
6. The verified values exactly match the caller's supplied fingerprint.
7. The leader and custom validator independently re-fetch and re-hash the same
   pinned artifact before accepting an AI verdict.

The caller cannot make a mutable URL or false fingerprint authoritative.

## Contract interface

| Method | Type | Purpose |
| --- | --- | --- |
| `open_milestone(worker, title, criteria, revision_window_seconds)` | payable write | Stores the rubric, worker, and bounded timeout term; locks `gl.message.value`. |
| `submit_evidence(id, url, sha256, bytes)` | write + consensus | Verifies the pinned artifact, adjudicates it, and settles or holds escrow. |
| `claim_revision_timeout_refund(id)` | write | After the fixed revision deadline, atomically refunds the remaining escrow to the client. |
| `cancel_milestone(id)` | write | Refunds an unsubmitted open milestone to its client. |
| `get_milestone(id)` | view | Returns current milestone and escrow state. |
| `get_evidence_version(id, version)` | view | Returns one immutable append-only submission record. |
| `get_milestone_count()` | view | Returns the number of milestones. |
| `get_totals()` | view | Returns funded, released, refunded, and version totals. |

## Consensus model

The contract uses two distinct equivalence checks:

- `gl.eq_principle.strict_eq` for the exact artifact fingerprint. This is safe
  because the processed result is a deterministic status/hash/length object.
- `gl.vm.run_nondet_unsafe` with a custom validator for the qualitative verdict.
  The leader proposes a structured scorecard; validators independently retrieve
  the same bytes and accept only a source-grounded proposal that follows the
  `PASS` / `REVISION_REQUIRED` / material `FAIL` rubric.

Evidence is explicitly treated as untrusted data. Prompts forbid following
instructions inside the artifact or relying on linked/outside material.

## Tests

The direct suite contains nine tests covering:

- funded creation and totals;
- zero-value and invalid-address guards;
- mutable and abbreviated GitHub URL rejection;
- caller-supplied fingerprint mismatch rejection;
- designated-worker authorization;
- append-only revision history and independent validator re-fetching;
- bounded revision-window validation;
- fixed-deadline non-extension across repeated revisions;
- exact deadline boundary, late-worker rejection, and client-only authorization;
- one-time timeout refund and funded/released/refunded/escrowed accounting;
- release, material-breach refund, and pre-submission cancellation paths.

Run the complete verification:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/genvm-lint check contracts/proofmint.py
.venv/bin/python -m pytest tests/direct -q
```

The direct suite pins the official GenVM `v0.2.16` runner bundle. This avoids
dependency drift in `genlayer-test==0.29.2`, whose automatic latest-release
lookup still expects the pre-0.3 bundle filename.

Expected results:

```text
GenVM lint passed
GenVM validation passed
Contract: ProofMint
Methods: 8 (4 view, 4 write)
9 passed
```

## Project structure

This public repository is intentionally contract-focused. GitHub and GenLayer
Explorer are the authoritative source and deployment records.

```text
contracts/proofmint.py                 Canonical Intelligent Contract
public/proofmint.py                    Byte-identical direct review copy
tests/direct/test_proofmint.py         Nine direct tests
tests/integration/test_studionet_deploy.py  Deployment smoke test
evidence/revision-timeout-demo.txt     Pinned live timeout-path fixture
EVIDENCE.md                            Verifiable review record
DEPLOYMENT.md                          Deployment and resubmission checklist
```

## Current publication

- Repository target: <https://github.com/haris4587/proofmint>
- Deployment source commit: <https://github.com/haris4587/proofmint/commit/b03de3ec6fe9a9dbe4c5ffaa6be3cbaa1afe0639>
- ProofMint v3 Studionet address: <https://explorer-studio.genlayer.com/address/0x2E213ECc435D6475617cf13eA61065c6EcB865DC?tab=contract>
- Deployment transaction: <https://explorer-studio.genlayer.com/tx/0x96271bdbefdee98240dec99842186f2e7d45f0f15f33084a6437f1022f519aa1>

The deployed contract source is byte-identical to the tracked v3 source (21,325
bytes; SHA-256
`25c0906d12ecd9bdfc00c375db748a426c6b98f16e3a143cda16daab5af358e0`).

## Live v3 revision-timeout proof

The funded Studionet test used milestone `0` and a 300-second revision window:

- Open milestone: <https://explorer-studio.genlayer.com/tx/0x5391935d4abee09b67e4d07798bef3fbfa8a87675828298a7a9a6f29737728fb>
- Evidence adjudication (`REVISION_REQUIRED`): <https://explorer-studio.genlayer.com/tx/0x611b6434b762a64f9b1cbda61ee21841aad34be68f621cdfba41dfe08146916a>
- Client timeout refund: <https://explorer-studio.genlayer.com/tx/0xeabf8444e23066b76a9dc94efe5a501c37fb37c6b597f626c4aee864e915ad93>

The finalized read for milestone `0` is `REFUNDED` with one evidence version,
`revision_deadline_unix = 1788967766`, and zero escrow. `get_totals()` reports
`total_released = 0`, `total_refunded = total_funded`, and `total_escrowed = 0`.
The artifact used in the adjudication is the commit-pinned
`evidence/revision-timeout-demo.txt` fixture recorded in `EVIDENCE.md`.

## Historical v2 Studionet proof

- Fund transaction: <https://explorer-studio.genlayer.com/tx/0xe3a6cee2b3c21da388c234fd84c0ed06aba9720952ace356f2f478f4e3805862>
- Evidence transaction: <https://explorer-studio.genlayer.com/tx/0xfcc0dcdde4d43dead8b13a38643dcabe3433817dae9edb6f068e37fe0e4d0030>
- Consensus: `FINALIZED / MAJORITY_AGREE`
- Verdict: `PASS`, score `100/100`
- Settlement: evidence version `1`; `0.01 GEN` released; escrow balance `0`

This record proves the older v2 happy path only. It is not presented as evidence
that v3's revision-timeout path has deployed or executed.

## License

MIT
