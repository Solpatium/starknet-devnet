import asyncio
import os

from starknet_py.contract import Contract
from starknet_py.net import AccountClient
from starknet_py.net.gateway_client import GatewayClient

# Local network
from starknet_py.net.models import StarknetChainId

from starkware.starknet.testing.starknet import Starknet

# The path to the contract source code.
CAIRO_PATH = os.path.join(
    os.path.dirname(__file__), "cairo-contracts/src"
)
CONTRACT_FILE = os.path.join(
    CAIRO_PATH, "openzeppelin/token/erc20/presets/ERC20Mintable.cairo"
)

CALLS_COUNT = 200


async def test():
    client = GatewayClient("http://localhost:5050")
    account = await AccountClient.create_account(client, chain=StarknetChainId.TESTNET)
    account = AccountClient(address=account.address, client=client, signer=account.signer,
                            chain=StarknetChainId.TESTNET)

    tx = await Contract.deploy(
        account,
        compilation_source=[CONTRACT_FILE],
        constructor_args=[1, 2, 3, 4, 5, 6],
        search_paths=[CAIRO_PATH],
    )
    contract = tx.deployed_contract

    promises = []
    for _ in range(CALLS_COUNT):
        promises.append(contract.functions["balanceOf"].call(account.address))

    print("LEN", len(promises))
    print(
        await asyncio.gather(*promises)
    )


asyncio.run(test())
