# PTTS
Private Token Transfer System

This GitHub page includes repositories both the private token transfer system and the balance range disclouse attack.

# For Private Token Transfer System

The frontend design of the web application is based on HTML and CSS languages located in index.html while the backend design is based on Javascript 
language located in index.js. For the backend design, (1) the ethers library [1] is used in order to bridge the web application to Ethereum, (2) the 
eccrypto library [2] to encrypt and decrypt with elliptic curve cryptography, (3) the Zokrates privacy-preserving tool [3] to generate verifiable proofs 
and finally (4) browserify [4] and webpack [5] bundlers to be able to run functions in the browser. For the blockchain-side, the smart
contracts in Ethereum are implemented with Solidity language [6] and compiled with 0.8.0-version of Remix compiler [7].

# Usage

The Metamask extension must be installed on the browser and the node-js extension must be also installed in order to run the server.js file.

In the directory of server.js file, execute ```node server.js``` in order to run the local server. 

Execute ```http://localhost:3300/``` on the browser where Metamask prompts you to connect on your Ethereum account.

Steps to make a private transaction:
1. Deploy a new token with a token symbol and token name.
2. Sender gets consent from receiver by providing token address and recevier address.
3. Receiver gives consent to sender by providing token address and sender address.
4. Sender deposits tokens to the smart contract by providing token address, receiver address, amount to send, current balance and secure number (secure number is initially 0). It takes nearly 2-3 minutes to generate zero-knowledge proof.
5. Receiver withdraws tokens from the smart contract by providing token address, sender address, private key (private key is used only inside browser and not transmitted over the network), current balance and secure number (secure number is initially 0). It takes nearly 2-3 minutes to generate zero-knowledge proof.

# For Balance Range Disclosure Attack

The users and the transactions between these users are randomly generated with respect to the number of users and the number of transactions parameters, 
respectively. The transactions to be disclosed to the adverserial entities are also randomly selected among all the transactions. The values for the 
network solution times and the error rate 20 metrics are the average of 20 different runs and in each run, balance of a randomly selected user is 
attacked. During the experiments, (1) the number of addresses changes in the range of 100 and 1,000,000, (2) the number of transactions changes in the 
range of 100 and 1,000,000 and (3) the default total token supply is 1,000,000 and default transaction leakage ratio is 0.5. We have employed Google 
OR-Tools [8] and three different versions of the Parallel Network Simplex algorithm [9] to solve the minimum cost flow network. These versions include 
PNS-Seq which is the sequential baseline network solver, PNS-Omp which is the parallel network solver by using OpenMP [10] and finally PNS-Omp-Avx2 which 
is the parallel and the advanced vector extended network solver for further acceleration. All the tests are performed upon MacBook Pro Notebook with a 
2.6 GHz Intel Core i7 processor, 16 GB memory and 6 cores. 

# Usage

Adjust the necessary parameters in the ```network_cost_solver.py```. In the default version, the parameters are as follows:

```
VISIBILITY = 0.5
TOTAL_SUPPLY = 1000000
NUMBER_OF_ADDRESS = 1000000
NUMBER_OF_TRANSACTION = 1000000
NUMBER_OF_RUN = 20
PRINT = False
```

Set ```PRINT = True``` for the verbose results.

The network cost solver is integrated with the parallel network simplex algorithm. Therefore, a compiler is necessary supporting C++11 and OpenMP. 
The Boost Align library [11] must be also installed in the standard include paths of the compiler. Otherwise, the path may need to be manually provided.

Execute the program a python IDE.

The program will return such an output:

```
Final Range:  15390 [15371, 66892]
Is Correct:  True
Error Rate:  0.948479
Average Elapsed Time Google-OR:  0.007690906524658203
Average Elapsed Time PNS:  0.008
```

[1] Ethers Javascript Library, URL: https://docs.ethers.io/v5/

[2] Eccrypto Javascript Library, URL: https://www.npmjs.com/package/eccrypto

[3] J. Eberhardt, S. Tai, "Zokrates-scalable privacy-preserving off-chain computations", IEEE International Conference on Internet of Things (iThings) 
and IEEE Green Computing and Communications (GreenCom) and IEEE Cyber, Physical and Social Computing (CPSCom) and IEEE Smart Data (SmartData),
pp. 1084-1091, 2018.

[4] Browserify Bundler, URL: https://browserify.org

[5] Webpack Bundler, URL: https://webpack.js.org

[6] Solidity Language, URL: https://docs.soliditylang.org/en/v0.8.15/

[7] Remix Compiler, URL: https://remix.ethereum.org

[8] Google OR-Tools, URL: https://developers.google.com/optimization

[9] Parallel network simplex algorithm for the minimum cost flow problem, URL: Phttps://github.com/gokcehan/pns

[10] L. Dagum, R. Menon, "OpenMP: an industry standard API for shared-memory programming", IEEE computational science and engineering, vol. 5, no. 1, 
pp. 46-55, 1998.

[11] Boost Align Library, URL: https://www.boost.org/doc/libs/1_79_0/doc/html/align.html











