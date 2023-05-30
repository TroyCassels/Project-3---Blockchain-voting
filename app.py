import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/certificate_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()



################################################################################
# Display Votes
################################################################################
candidate_name = st.number_input("Enter Kitty Candidate votes to display", value=0, step=1)
if st.button("Display Votes"):
    # Get the candidate name
    certificate_owner = contract.functions.ownerOf(candidate_name).call()
    st.write(f"The votes relate to  {candidate_name}")

    # Get the candidates's metadata
    candidate_uri = contract.functions.tokenURI(candidate_name).call()
    st.write(f"The candidate's tokenURI metadata is {candidate_uri}")
