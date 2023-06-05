import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from plyer import notification

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Define the load_contract function
def load_contract():

    # Load ABI
    with open(Path('./kitty.json')) as f:
        kitty_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=kitty_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()



################################################################################
# Display Votes
################################################################################

st.title("Election for CryptoKitty President")

st.sidebar.write("Choose a voting account")
account = st.sidebar.selectbox("Voter Address", w3.eth.accounts)

st.sidebar.write("Choose Candidate")
candidate = st.sidebar.text_input("Enter candidate name")
#cast_vote = contract.functions.castVote(candidate).call()

if st.button("Vote"):
    try:
        # Create a transaction
        transaction = contract.functions.castVote(candidate).buildTransaction({
            "from": account,
            "gas": 1000000,
        })
        # Sign the transaction using Metamask and send it to the network
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key="YOUR_PRIVATE_KEY")
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        st.success("Voted successfully!")
    except Exception as e:
        st.error("Error voting: {}".format(e))


# Add a button to see the election result, which is the number of votes that each candidate has received
if st.sidebar.button("See Election Result"):
    # Get the vote count for each candidate by calling the getVoteCount function
    vote_counts = {}
    for candidate in contract.functions.candidate().call():
        vote_counts[candidate] = contract.functions.winner().call()
    # Display the election result using table() function
    st.table(vote_counts)
