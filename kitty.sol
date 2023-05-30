// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract votingSystem{
    
    mapping (uint => kittyCandidate) public kittyCandidates;
    mapping (address => kittyVoter) public voters;
    address public kittyAdmin;
    uint id;
    uint public totalVoter = 0;
    uint public totalCandidate=0;
    
    constructor () {
        kittyAdmin = msg.sender;
    }
    
    struct kittyVoter{
        string name;
        address voterAddress;
        uint hasVoted;
    }    

    struct kittyCandidate{
        uint kittyId;
        string kittyName;
        uint voteCount;
    }

    function registerKittyCandidate (string memory _kittyName) public {
        require (msg.sender == kittyAdmin , "only admin can authorize this function");
        id++;
        kittyCandidates[id] = kittyCandidate (id, _kittyName , 0);
        totalCandidate++;

    }

    function registerKittyVoter (address _voterAddress, string memory _name) public {
        require (msg.sender == kittyAdmin , "only admin can authorize this function");
        kittyVoter memory voter;
        voter.name =_name;
        voter.hasVoted = 0; // 0 = has not voted & 1 = has voted
        voters[_voterAddress] = voter;
        totalVoter++;
    }

    // function voteTo(string memory _kittyName) public {
    //     require (voters[voter] =)
    // }

}



