pragma solidity ^0.5.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/GreenToken.sol";

contract TestGreenToken {
    function transferToken() public{
        GreenToken token = GreenToken(DeployedAddresses.GreenToken());

        address addr = 0x0278aA1Bf268Ad72dB892707cDd2A1c3C8dBFbF5; //put here a address to test
        uint amount = 20;

        bool transfCheck = token.transfer(addr, amount);
        bool check = true;

        Assert.equal(transfCheck, check, "Item check should match");
    }

    function getBalance() view public{
        GreenToken token = GreenToken(DeployedAddresses.GreenToken());

        address addr = 0x0278aA1Bf268Ad72dB892707cDd2A1c3C8dBFbF5; //put here a address to test
        uint balance;

        balance = token.balanceOf(addr);
    }

    function checkApprove() public{
        GreenToken token = GreenToken(DeployedAddresses.GreenToken());

        address spender = 0x65e9CB765eb38Bdd7D2B6eb7E4412c112029F0f9; //put here address of spender ( admin in this case )
        uint amount = 10; 

        bool checkApp = true;

        bool resApp = token.approve(spender, amount);

        Assert.equal(resApp, checkApp, "Item checkApp should match");
    }

    //test of mint function
    function tryMint() public{
        GreenToken token = GreenToken(DeployedAddresses.GreenToken());

        uint amount = 50000000000000000000000000; //get the half of total supply

        address addr = 0x0278aA1Bf268Ad72dB892707cDd2A1c3C8dBFbF5; //put here a address receiver to test
        

        bool transfCheck = token.transfer(addr, amount);
        bool check = true;

        Assert.equal(transfCheck, check, "Item check should match");

        //After transferring half of the total supply, we attempt a new transfer with more than the available budget of the contract
        //in order to call the internal mint function from smart contract
        uint amount2 = 60000000000000000000000000;
        bool transfCheck2 = token.transfer(addr, amount2);
        bool check2 = true;

        Assert.equal(transfCheck2, check2, "Item check should match");

        uint supply = token.totalSupply();

    }


}