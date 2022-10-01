// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.0;

import "../sender/verifier.sol";
import "../receiver/verifier.sol";

contract ERC20Basic {
    string public name;
    string public symbol;
    uint256 totalSupply;
    uint8 public constant decimals = 18;  

    uint256 public constant hash_0 = 89059515727727869117346995944635890507;
    uint256 public constant hash_1 = 307780299564696270546142378206422684517;
    uint256 public constant hash_1000 = 160447523714545220416709952320130456769;

    using SafeMath for uint256;
    mapping(address => string) publicKeys;
    mapping(address => uint256) balanceHashes;
    mapping(address => mapping (address => bool)) request;
    mapping(address => mapping (address => bool)) consent;
    mapping(address => mapping (address => uint256)) allowed;
    mapping(address => mapping (address => string)) encrpytedMessage;
    
    constructor(string memory _name, string memory _symbol) {  
        name = _name;
        symbol = _symbol;
	    totalSupply = 1000;
        balanceHashes[msg.sender] = hash_1000;
    }  

    function mint() public {
        balanceHashes[msg.sender] = hash_1;
    }

    function balanceHashOf(address tokenOwner) public view returns (uint256) {   
        return balanceHashes[tokenOwner];
    }

    function requestToSend(address _to) public {
        request[msg.sender][_to] = true;
    }

    function consentToSend(address _from, string memory publicKey) public {
        require(request[_from][msg.sender] == true);
        consent[_from][msg.sender] = true;
        publicKeys[msg.sender] = publicKey;
    }

    function getPublicKey(address _address) public view returns (string memory) {
        return publicKeys[_address];
    }

    function getMessage(address _from) public view returns (string memory) {
        return encrpytedMessage[_from][msg.sender];
    }

    function privateSend(
        address _to,
        uint256 hashValue,
        uint256 hashSenderBalanceAfter,
        string memory message,
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c
    ) public returns (bool) {
        require(consent[msg.sender][_to] == true);

        if(balanceHashes[msg.sender] == 0)
            balanceHashes[msg.sender] = hash_0;

        // uint256 hashSenderBalanceBefore = balanceHashes[msg.sender];
        VerifierSender verifier = new VerifierSender();
        bool senderProofIsCorrect = verifier.verifyTx2(a, b, c, [hashValue, balanceHashes[msg.sender], hashSenderBalanceAfter, 1]);

        if(senderProofIsCorrect) {
            balanceHashes[msg.sender] = hashSenderBalanceAfter;
            allowed[msg.sender][_to] = hashValue;
            encrpytedMessage[msg.sender][_to] = message;
        }

        return senderProofIsCorrect;
    }

    function privateReceive(
        address _from,
        uint256 hashValue,
        uint256 hashReceiverBalanceAfter,
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c
    ) public returns (bool) {
        require(consent[_from][msg.sender] == true);

        require(hashValue == allowed[_from][msg.sender]); 

        if(balanceHashes[msg.sender] == 0)
            balanceHashes[msg.sender] = hash_0;

        // uint256 hashReceiverBalanceBefore = balanceHashes[msg.sender];
        VerifierReceiver verifier = new VerifierReceiver();
        bool receiverProofIsCorrect = verifier.verifyTx2(a, b, c, [hashValue, balanceHashes[msg.sender], hashReceiverBalanceAfter, 1]);

        if(receiverProofIsCorrect) {
            balanceHashes[msg.sender] = hashReceiverBalanceAfter;
            allowed[_from][msg.sender] = 0;
        } 

        return receiverProofIsCorrect;
    }
}

library SafeMath { 
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
      assert(b <= a);
      return a - b;
    }
    
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
      uint256 c = a + b;
      assert(c >= a);
      return c;
    }
}