// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HealthRecords {

    struct Report {
        string patientId;
        string ipfsCid;
        string encryptedKey;
        uint256 timestamp;
    }

    mapping(string => Report[]) private records;   // patientId => list of reports

    event ReportUploaded(string patientId, string ipfsCid, uint256 timestamp);

    function uploadReport(
        string memory patientId,
        string memory ipfsCid,
        string memory encryptedKey
    ) public {
        records[patientId].push(
            Report(patientId, ipfsCid, encryptedKey, block.timestamp)
        );

        emit ReportUploaded(patientId, ipfsCid, block.timestamp);
    }

    function getReports(string memory patientId)
        public
        view
        returns (Report[] memory)
    {
        return records[patientId];
    }
}
