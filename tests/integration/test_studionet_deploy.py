from gltest import get_contract_factory, get_default_account
from gltest.assertions import tx_execution_succeeded


def test_deploy_and_open_funded_sample_milestone():
    account = get_default_account()
    factory = get_contract_factory(contract_file_path="proofmint.py")
    contract = factory.deploy(
        account=account,
        consensus_max_rotations=3,
        wait_interval=1000,
        wait_retries=120,
    )

    print(f"PROOFMINT_CONTRACT_ADDRESS={contract.address}")

    receipt = contract.open_milestone(
        args=[
            account.address,
            "Responsive landing page milestone",
            (
                "The submitted project must include a working responsive landing "
                "page, clear setup instructions, and automated tests that pass. "
                "Evidence must use a full Git commit and verified SHA-256."
            ),
        ]
    ).transact(value=10**16, wait_interval=1000, wait_retries=120)

    assert tx_execution_succeeded(receipt)
    assert contract.get_milestone_count(args=[]).call() == 1
    totals = contract.get_totals(args=[]).call()
    assert int(totals["total_funded"]) == 10**16
