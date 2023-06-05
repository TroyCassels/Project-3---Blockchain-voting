// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract VotingSystem {
    struct Candidate {
        string name;
        uint voteCount;
    }
    mapping(address => bool) public votersList;
    Candidate[] public candidatesList;
    constructor() {
        // Initialize the candidates list with their names and initial vote counts
        candidatesList.push(Candidate("Candidate 1", 0));
        candidatesList.push(Candidate("Candidate 2", 0));
        candidatesList.push(Candidate("Candidate 3", 0));
    }
    function hasVoted(address voter) internal view returns (bool) {
        // Check if the voter has already voted
        return votersList[voter];
    }
    function isValidCandidate(string memory candidateName) internal view returns (bool) {
        // Check if the candidate name is valid by iterating through the candidates list
        for (uint i = 0; i < candidatesList.length; i++) {
            if (keccak256(bytes(candidatesList[i].name)) == keccak256(bytes(candidateName))) {
                return true;
            }
        }
        return false;
    }
    function castVote(string memory candidateName) public {
        address voter = msg.sender;
        require(!hasVoted(voter), "Voter has already voted");
        require(isValidCandidate(candidateName), "Invalid candidate name");
        // Increment the vote count for the selected candidate
        for (uint i = 0; i < candidatesList.length; i++) {
            if (keccak256(bytes(candidatesList[i].name)) == keccak256(bytes(candidateName))) {
                candidatesList[i].voteCount++;
                break;
            }
        }
        // Mark the voter as voted
        votersList[voter] = true;
    }
    function winner() public view returns (string memory winnerName, uint winnerVotes) {
        uint maxVotes = 0;
        // Find the candidate with the highest vote count
        for (uint i = 0; i < candidatesList.length; i++) {
            if (candidatesList[i].voteCount > maxVotes) {
                maxVotes = candidatesList[i].voteCount;
                winnerName = candidatesList[i].name;
                winnerVotes = candidatesList[i].voteCount;
            }
        }
        // Return the name and vote count of the winner
        return (winnerName, winnerVotes);
    }
}






