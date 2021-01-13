var GreenToken = artifacts.require('./contracts/GreenToken.sol');

module.exports = function(deployer){
    deployer.deploy(GreenToken);
}