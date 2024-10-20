import time
from uagents import Agent, Context, Model
from typing import List, Dict
from xrpl.transaction import submit_and_wait
from xrpl.models.transactions.nftoken_mint import NFTokenMint, NFTokenMintFlag
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.clients import JsonRpcClient
import xrpl
import asyncio

# XRPL Helper class to handle NFT minting
class XRPLHelper:
    def __init__(self, seed=""):
        self.JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
        self.client = JsonRpcClient(self.JSON_RPC_URL)
        
        if seed == "":
            self.wallet = generate_faucet_wallet(client=self.client)
        else:
            self.wallet = Wallet.from_seed(seed=seed)
            
        self.address = self.wallet.address

    def string_to_hex(self, string):
        return bytes.fromhex(string.encode().hex()).hex()

    def mint_nft(self, url):
        try:
            mint_tx = NFTokenMint(
                account=self.address,
                nftoken_taxon=1,
                flags=NFTokenMintFlag.TF_TRANSFERABLE,
                uri=self.string_to_hex(url)
            )
            
            mint_tx_response = submit_and_wait(
                transaction=mint_tx,
                client=self.client,
                wallet=self.wallet
            )
            
            # Extract NFT ID from response
            nft_id = None
            for node in mint_tx_response.result['meta']['AffectedNodes']:
                print(node)
                if "CreatedNode" in node:
                    nft_id = node['CreatedNode']['NewFields']['NFTokens'][0]['NFToken']['NFTokenID']
                    break
                    
            return True, nft_id
            
        except Exception as e:
            return False, str(e)




xrpl_helper = XRPLHelper()  # Initialize with empty seed for test account

def put_on_blockchain(urls):
    nft_ids = []
    for url in urls:
        mint_success, result = xrpl_helper.mint_nft(url)
        if mint_success:
            nft_ids.append(result)
        else:
            success = False
            error_message = f"Failed to mint NFT for URL {url}: {result}"
            print(error_message)
    return nft_ids



# put_on_blockchain(["https://example.com/nft1", "https://example.com/nft2"])
