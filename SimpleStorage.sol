// SPDX_License_Identifier: MIT
pragma solidity ^0.6.0; // defining the solidity version

// creating a contract
contract SimpleStorage {
    uint256 favoriteNumber;
    // making a structure
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // making a structure object
    // People public person = People({favoriteNumber : 2, name : "Patrick"});

    People[] public people; // declaring a dynamic array

    // MAPPING - A data structure to get a value in an array without iterating to it whole
    mapping(string => uint256) public nameToFavoriteNumber;

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    // function to view favorite number
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }
}
