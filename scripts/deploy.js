const { ethers } = require("hardhat");
const fs = require("fs");

async function main() {
    const Contract = await ethers.getContractFactory("HealthRecords");
    const contract = await Contract.deploy();
    await contract.waitForDeployment();

    console.log("Deployed at:", await contract.getAddress());

    fs.writeFileSync(
        "backend/deployedInfo.json",
        JSON.stringify({ address: await contract.getAddress() })
    );
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
