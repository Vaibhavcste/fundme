//SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract fundme {
    using SafeMathChainlink for uint256;
    mapping(address => uint256) public addresstoamountfunded;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(priceFeed);
        owner = msg.sender;
    }

    function pay() public payable {
        uint256 minimumUSD = 20 * 10**18;
        //is the donated amount less than 20USD?
        require(
            getConversionrate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        addresstoamountfunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digit
        return uint256(answer * 10000000000);
    }

    //What the ETH => USD Conversion
    function getConversionrate(uint256 ethamt) public view returns (uint256) {
        uint256 ethprice = getPrice();
        uint256 ethAmountInUsd = (ethamt * ethprice) / 1000000000000000000;
        return ethAmountInUsd;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price + 1);
    }

    function withdraw() public payable onlyOwner {
        require(msg.sender == owner);
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addresstoamountfunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
