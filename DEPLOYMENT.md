# ProofMint v2 Deployment Checklist

## 1. Publish the tracked repository

The public, contract-focused repository is available at
<https://github.com/haris4587/proofmint>. It includes the canonical contract,
tests, `README.md`, `EVIDENCE.md`, and deployment instructions.

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

Deployment completed from commit
`da7839cb86865db1308e0888d8059649604e0126`:

```text
ProofMint v2: 0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A
Explorer: https://explorer-studio.genlayer.com/address/0x59e3468A6fbC37B2fAc8D17f97695662aa31E33A?tab=contract
```

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

Completed:

```text
Milestone ID: 0
Fund transaction: 0xe3a6cee2b3c21da388c234fd84c0ed06aba9720952ace356f2f478f4e3805862
Funded: 0.01 GEN
```

## 4. Run a full evidence adjudication

Use the raw `EVIDENCE.md` URL pinned to the final 40-character Git commit. Compute
its SHA-256 and exact byte length from the raw bytes, then call:

```text
submit_evidence(milestone_id, raw_url, sha256, byte_length)
```

Wait for the consensus result and confirm the first append-only evidence version
through `get_evidence_version(milestone_id, 1)`.

Completed:

```text
Evidence transaction: 0xfcc0dcdde4d43dead8b13a38643dcabe3433817dae9edb6f068e37fe0e4d0030
Consensus: FINALIZED / MAJORITY_AGREE
Outcome: PASS
Score: 100/100
Evidence version: 1
Settlement: RELEASED (0.01 GEN)
```

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

All reviewer checks and the funded consensus path have now completed successfully.
The corrected GenLayer contribution is ready for resubmission after the final
public documentation update is deployed.
