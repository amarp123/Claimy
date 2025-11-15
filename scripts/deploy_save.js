// We import the Hardhat Runtime Environment (hre) object implicitly
// This script assumes you are using ethers.js syntax (common in older Hardhat projects)

async function main() {
  // --- 1. Get the account used for deployment ---
  // If using hardhat-ethers:
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // --- 2. Get the Contract Factory ---
  // Replace "HealthRecords" with the exact name of your contract file/class
  const HealthRecords = await ethers.getContractFactory("HealthRecords");

  // --- 3. Deploy the Contract ---
  console.log("Deploying HealthRecords...");
  const healthRecords = await HealthRecords.deploy();

  // Wait for the contract to be deployed and confirmed
  await healthRecords.waitForDeployment();
  
  const contractAddress = await healthRecords.getAddress();

  console.log("HealthRecords deployed to:", contractAddress);

  // --- 4. Save Deployment Info (Optional but Recommended) ---
  // You would typically save the contract address to a file (like a JSON file)
  // so your backend can use it. Hardhat's 'artifacts' directory usually handles this, 
  // but if you need a custom file, you'd add that logic here.
}

// We recommend this pattern to be able to use async/await everywhere
// and handle errors properly.
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });