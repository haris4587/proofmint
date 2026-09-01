# ProofMint v2 Deployment Checklist

## 1. Publish the tracked repository

Create a public GitHub repository named `proofmint` under `haris4587`. Upload the
complete project, including `contracts/proofmint.py`, tests, `README.md`,
`EVIDENCE.md`, and the frontend source.

Do not deploy from an untracked local copy. Record the full commit SHA that
contains the final contract.

## 2. Deploy the exact tracked contract

1. Open <https://studio.genlayer.com/>.
2. Connect MetaMask wallet `0x805F46E1e097D1ed67d5619671E99036495DB95c`.
3. Select **Studionet** and keep **Simulation Mode unchecked**.
4. Create/import a contract using the exact tracked
   `contracts/proofmint.py` file from the recorded GitHub commit.
5. Deploy with no constructor arguments.
6. Wait for consensus acceptance and copy the new contract address.

Never reuse the rejected v1 address
`0xAd4Ae92FE7c0eb15E21f29346DE2Bfbaa2dC52F1`.

## 3. Execute a funded smoke test

Call `open_milestone` from the connected wallet with a small Studionet GEN value:

```text
worker: 0x805F46E1e097D1ed67d5619671E99036495DB95c
title: ProofMint v2 immutable evidence smoke test
criteria: The pinned EVIDENCE.md must describe ProofMint v2 escrow, immutable GitHub commit binding, validator SHA-256 verification, seven passing direct tests, and the public source and reviewer links.
value: 0.01 GEN (or another small Studionet test amount)
```

Then call `get_milestone_count()` and `get_totals()` to confirm accepted state.

## 4. Run a full evidence adjudication

Use the raw `EVIDENCE.md` URL pinned to the final 40-character Git commit. Compute
its SHA-256 and exact byte length from the raw bytes, then call:

```text
submit_evidence(milestone_id, raw_url, sha256, byte_length)
```

Wait for the consensus result and confirm the first append-only evidence version
through `get_evidence_version(milestone_id, 1)`.

## 5. Bind the website to the deployment

Update `lib/proofmint.ts`:

- replace the historical address with the new v2 address;
- set `PROOFMINT_DEPLOYMENT_READY = true`;
- confirm the GitHub and Explorer URLs;
- rebuild and redeploy the existing ProofMint Site.

## 6. Final reviewer checks

- `/source` opens without authentication.
- **Tracked source** opens the exact GitHub `.py` file.
- **Verify in Explorer** opens the new v2 contract.
- the source and deployed schema both show seven methods;
- the homepage wallet connects to Studionet;
- funded milestone and evidence forms target the new address;
- the old address is not presented as v2.

Only then submit the corrected GenLayer contribution.
