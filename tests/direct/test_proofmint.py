import hashlib
import json


TITLE = "Responsive landing page milestone"
CRITERIA = (
    "Deliver a responsive landing page, clear setup instructions, and automated "
    "tests that pass. The evidence must directly show every requirement."
)
COMMIT = "a" * 40
EVIDENCE_URL = (
    "https://raw.githubusercontent.com/haris4587/proofmint/"
    f"{COMMIT}/EVIDENCE.md"
)
EVIDENCE_BODY = (
    b"# Delivery evidence\n\nResponsive layout: complete.\n"
    b"Setup guide: complete.\nAutomated tests: 12 passing.\n"
)
EVIDENCE_SHA = hashlib.sha256(EVIDENCE_BODY).hexdigest()
ESCROW = 2_000_000_000_000_000_000


def addr_hex(address):
    return "0x" + bytes(address).hex()


def open_case(contract, direct_vm, client, worker, value=ESCROW):
    direct_vm.sender = client
    direct_vm.value = value
    milestone_id = contract.open_milestone(addr_hex(worker), TITLE, CRITERIA)
    direct_vm.value = 0
    return milestone_id


def mock_decision(direct_vm, outcome, score, summary, material_breach=False):
    direct_vm.mock_web(
        r".*raw\.githubusercontent\.com/haris4587/proofmint/.*",
        {"status": 200, "body": EVIDENCE_BODY},
    )
    direct_vm.mock_llm(
        r".*You are ProofMint, a conservative milestone adjudicator.*",
        json.dumps(
            {
                "outcome": outcome,
                "score": score,
                "material_breach": material_breach,
                "summary": summary,
            }
        ),
    )
    direct_vm.mock_llm(
        r".*Independently verify this ProofMint adjudication proposal.*",
        json.dumps({"agree": True}),
    )


def submit(contract, direct_vm, worker, milestone_id):
    direct_vm.sender = worker
    contract.submit_evidence(
        milestone_id,
        EVIDENCE_URL,
        EVIDENCE_SHA,
        len(EVIDENCE_BODY),
    )


def test_open_funded_milestone_and_totals(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/proofmint.py")
    milestone_id = open_case(contract, direct_vm, direct_alice, direct_bob)

    milestone = contract.get_milestone(milestone_id)
    totals = contract.get_totals()
    assert milestone.milestone_id == 0
    assert milestone.client == addr_hex(direct_alice)
    assert milestone.worker == addr_hex(direct_bob)
    assert milestone.funded_amount == ESCROW
    assert milestone.escrow_balance == ESCROW
    assert milestone.criteria_sha256 == hashlib.sha256(CRITERIA.encode()).hexdigest()
    assert milestone.status == "OPEN"
    assert contract.get_milestone_count() == 1
    assert totals["total_funded"] == ESCROW


def test_open_rejects_zero_escrow_and_invalid_worker(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/proofmint.py")
    direct_vm.sender = direct_alice
    direct_vm.value = 0
    with direct_vm.expect_revert("Milestone escrow must be greater than zero"):
        contract.open_milestone(addr_hex(direct_bob), TITLE, CRITERIA)

    direct_vm.value = ESCROW
    with direct_vm.expect_revert("Worker must be a valid 0x address"):
        contract.open_milestone("not-an-address", TITLE, CRITERIA)


def test_rejects_mutable_or_abbreviated_github_evidence(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/proofmint.py")
    milestone_id = open_case(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_bob

    with direct_vm.expect_revert(
        "Evidence must be a raw.githubusercontent.com URL pinned to a commit"
    ):
        contract.submit_evidence(
            milestone_id,
            "https://github.com/haris4587/proofmint/blob/main/EVIDENCE.md",
            EVIDENCE_SHA,
            len(EVIDENCE_BODY),
        )

    short_sha_url = EVIDENCE_URL.replace(COMMIT, "abc1234")
    with direct_vm.expect_revert(
        "Evidence URL must use a lowercase full 40-character commit SHA"
    ):
        contract.submit_evidence(
            milestone_id,
            short_sha_url,
            EVIDENCE_SHA,
            len(EVIDENCE_BODY),
        )


def test_rejects_caller_fingerprint_that_does_not_match_fetched_bytes(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/proofmint.py")
    milestone_id = open_case(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_bob
    direct_vm.mock_web(
        r".*raw\.githubusercontent\.com/haris4587/proofmint/.*",
        {"status": 200, "body": EVIDENCE_BODY},
    )

    with direct_vm.expect_revert(
        "Fetched evidence does not match the supplied SHA-256"
    ):
        contract.submit_evidence(
            milestone_id,
            EVIDENCE_URL,
            "0" * 64,
            len(EVIDENCE_BODY),
        )


def test_only_designated_worker_can_submit(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie
):
    contract = direct_deploy("contracts/proofmint.py")
    milestone_id = open_case(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_charlie

    with direct_vm.expect_revert("Only the designated worker can submit evidence"):
        contract.submit_evidence(
            milestone_id,
            EVIDENCE_URL,
            EVIDENCE_SHA,
            len(EVIDENCE_BODY),
        )


def test_revision_is_append_only_and_validator_refetches_exact_bytes(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/proofmint.py")
    milestone_id = open_case(contract, direct_vm, direct_alice, direct_bob)
    mock_decision(
        direct_vm,
        "REVISION_REQUIRED",
        72,
        "The responsive layout is visible, but the setup proof needs more detail.",
    )
    submit(contract, direct_vm, direct_bob, milestone_id)

    milestone = contract.get_milestone(milestone_id)
    version = contract.get_evidence_version(milestone_id, 1)
    assert milestone.status == "REVISION_REQUIRED"
    assert milestone.escrow_balance == ESCROW
    assert milestone.evidence_count == 1
    assert version.immutable_url == EVIDENCE_URL
    assert version.expected_sha256 == EVIDENCE_SHA
    assert version.verified_sha256 == EVIDENCE_SHA
    assert version.byte_length == len(EVIDENCE_BODY)
    assert direct_vm.run_validator() is True

    direct_vm.clear_mocks()
    direct_vm.mock_web(
        r".*raw\.githubusercontent\.com/haris4587/proofmint/.*",
        {"status": 200, "body": b"changed bytes"},
    )
    direct_vm.mock_llm(
        r".*Independently verify this ProofMint adjudication proposal.*",
        json.dumps({"agree": True}),
    )
    assert direct_vm.run_validator() is False


def test_release_refund_and_cancel_settlement_paths(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/proofmint.py")

    pass_id = open_case(contract, direct_vm, direct_alice, direct_bob)
    mock_decision(
        direct_vm,
        "PASS",
        96,
        "The pinned artifact directly demonstrates every stored acceptance criterion.",
    )
    submit(contract, direct_vm, direct_bob, pass_id)
    assert contract.get_milestone(pass_id).status == "RELEASED"
    assert contract.get_milestone(pass_id).escrow_balance == 0

    direct_vm.clear_mocks()
    fail_id = open_case(contract, direct_vm, direct_alice, direct_bob)
    mock_decision(
        direct_vm,
        "FAIL",
        8,
        "The pinned artifact is unrelated to the milestone and demonstrates a material breach.",
        material_breach=True,
    )
    submit(contract, direct_vm, direct_bob, fail_id)
    assert contract.get_milestone(fail_id).status == "REFUNDED"
    assert contract.get_milestone(fail_id).escrow_balance == 0

    direct_vm.clear_mocks()
    cancel_id = open_case(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    contract.cancel_milestone(cancel_id)
    assert contract.get_milestone(cancel_id).status == "CANCELLED"
    assert contract.get_milestone(cancel_id).escrow_balance == 0

    totals = contract.get_totals()
    assert totals["total_funded"] == ESCROW * 3
    assert totals["total_released"] == ESCROW
    assert totals["total_refunded"] == ESCROW * 2
