# ProofMint v2

ProofMint is a GenLayer Intelligent Contract for version-bound milestone escrow.
A client funds a milestone in native GEN and designates one worker. The worker
submits an immutable GitHub artifact, its SHA-256, and exact byte length. The
contract independently verifies those bytes before GenLayer validators judge the
artifact against the stored natural-language acceptance criteria.

The settlement result is deterministic:

- `PASS` releases escrow to the designated worker.
- `REVISION_REQUIRED` keeps escrow locked and permits another immutable version.
- `FAIL` with a demonstrated material breach refunds the client.
- A client may cancel and recover escrow only before the first submission.

## Why v2 exists

The original ProofMint submission was rejected because its Studio link opened the
Studio application instead of exposing reviewable contract source. v2 fixes the
review path and materially strengthens the protocol itself:

- canonical public GitHub repository with tracked `contracts/proofmint.py`;
- matching GenLayer Explorer deployment address;
- public `/source` page linking both artifacts;
- native GEN escrow rather than a decision-only prototype;
- immutable evidence binding instead of a mutable HTTPS URL;
- append-only evidence versions and explicit settlement accounting.

The rejected v1 deployment is historical and must not be used as proof of v2.

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
| `open_milestone(worker, title, criteria)` | payable write | Stores the rubric and designated worker; locks `gl.message.value`. |
| `submit_evidence(id, url, sha256, bytes)` | write + consensus | Verifies the pinned artifact, adjudicates it, and settles or holds escrow. |
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

The direct suite contains seven tests covering:

- funded creation and totals;
- zero-value and invalid-address guards;
- mutable and abbreviated GitHub URL rejection;
- caller-supplied fingerprint mismatch rejection;
- designated-worker authorization;
- append-only revision history and independent validator re-fetching;
- release, material-breach refund, and pre-submission cancellation paths.

Run the complete verification:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/genvm-lint check contracts/proofmint.py
.venv/bin/python -m pytest tests/direct -q
npm run install:ci
npm test
```

Expected results:

```text
GenVM lint passed
GenVM validation passed
Contract: ProofMint
Methods: 7 (4 view, 3 write)
7 passed
Site build passed
5 frontend tests passed
```

## Project structure

```text
contracts/proofmint.py                 Canonical Intelligent Contract
public/proofmint.py                    Byte-identical direct review copy
tests/direct/test_proofmint.py         Seven direct tests
tests/integration/test_studionet_deploy.py  Deployment smoke test
app/page.tsx                           MetaMask protocol interface
app/source/page.tsx                    Reviewer evidence page
EVIDENCE.md                            Verifiable review record
DEPLOYMENT.md                          Deployment and resubmission checklist
```

## Current publication

- Site: <https://proofmint.ansaf1st33.chatgpt.site>
- Repository target: <https://github.com/haris4587/proofmint>
- New v2 Studionet address: pending wallet deployment

Do not resubmit until the repository is public and the new v2 Explorer address is
linked from the live `/source` page.

## License

MIT
