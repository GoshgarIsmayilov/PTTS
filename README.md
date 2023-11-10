# PTTS
_Private Token Transfer System_

Blockchains are decentralized and immutable databases that are shared among the nodes of the network. Although blockchains have attracted a great scale of attention in the recent years by disrupting the traditional financial systems, the transaction privacy is still a challenging issue that needs to be addressed and analysed. We propose a Private Token Transfer System (PTTS) for the Ethereum public blockchain in the first part of this paper. For the proposed framework, zero-knowledge based protocol has been designed using Zokrates and integrated into our private token smart contract. With the help of web user interface designed, the end users can interact with the smart contract without any third-party setup. In the second part of the paper, we provide security and privacy analysis including the replay attack and the balance range privacy attack which has been modeled as a network flow problem. It is shown that in case some balance ranges are deliberately leaked out to particular organizations  or adversarial entities, it is possible to extract meaningful information about the user balances by employing minimum cost flow network algorithms that have polynomial complexity. The experimental study reports the Ethereum gas consumption and proof generation times for the proposed framework. It also reports network solution times and goodness rates for a subset of addresses under the balance range privacy attack with respect to number of addresses, number of transactions and ratio of leaked transfer transaction amounts.

# Private Token Transfer System

The frontend design of the web application is based on HTML and CSS languages located in index.html while the backend design is based on Javascript 
language located in index.js. For the backend design, (1) the ethers library [1] is used in order to bridge the web application to Ethereum, (2) the 
eccrypto library [2] to encrypt and decrypt with elliptic curve cryptography, (3) the Zokrates privacy-preserving tool [3] to generate verifiable proofs 
and finally (4) browserify [4] and webpack [5] bundlers to be able to run functions in the browser. For the blockchain-side, the smart
contracts in Ethereum are implemented with Solidity language [6] and compiled with 0.8.0-version of Remix compiler [7].

## To Run

The Metamask extension must be installed on the browser and the node-js extension must be also installed in order to run the server.js file.

In the directory of server.js file, execute ```node server.js``` in order to run the local server. 

Execute ```http://localhost:3300/``` on the browser where Metamask prompts you to connect on your Ethereum account.

Steps to make a private transaction:
1. Deploy a new token with a token symbol and token name.
2. Sender gets consent from receiver by providing token address and recevier address.
3. Receiver gives consent to sender by providing token address and sender address.
4. Sender deposits tokens to the smart contract by providing token address, receiver address, amount to send, current balance and secure number (secure number is initially 0). It takes nearly 2-3 minutes to generate zero-knowledge proof. The balance and the secure number of sender must be recorded in order to involve with private transactions later again.
5. Receiver withdraws tokens from the smart contract by providing token address, sender address, private key (private key is used only inside browser and not transmitted over the network), current balance and secure number (secure number is initially 0). It takes nearly 2-3 minutes to generate zero-knowledge proof. The balance and the secure number of receiver must be recorded in order to involve with private transactions later again.

The video to show the steps above can be found in: https://drive.google.com/file/d/1NqG2Zy1ujQ1_v9CaKG2JLIDC5iaZC2zZ/view?usp=sharing

<img src="https://github.com/GoshgarIsmayilov/PTTS/blob/master/auxiliary/screenshots/architecture.png" width="80%"/>

## Experimental Study 

### Blockchain Gas Consumption 

| Function        | Gas Units        | Gas Cost (Ether) | Gas Cost (USD)  |
| --------------- | ---------------- | ---------------- | --------------- |
| Deploy Contract | 4,557,726        | 0.00683658       | 8.19            |
| Get Consent     | 44,300           | 0.00006645       | 0.08            |
| Give Consent    | 183,344          | 0.00027501       | 0.33            |
| Deposit Tokens  | 2,060,133        | 0.00309019       | 3.70            |
| Withdraw Tokens | 1,699,399        | 0.00253816       | 3.04            |

Transactions:
For Rinkeby (deprecated):

https://rinkeby.etherscan.io/tx/0x1ca09fefb6893ac9dff5e8157f14ca39558dd5ea1423f09cbe6421d62886ddd6

https://rinkeby.etherscan.io/tx/0x3f5766fd4c5e242fd4f322152a9dea1a93cb3fbc987d7c5da12e2058387b3940

https://rinkeby.etherscan.io/tx/0x6c9d668bd3dcb19f308f6ad3cf207941da3d69fddbd3220654cbd91b9d237bb7

https://rinkeby.etherscan.io/tx/0x6b8c6d79c772c19a04211ee8ee2310ffd55abf7c4440ff9a4dc3decd8f3d0116

https://rinkeby.etherscan.io/tx/0x3f9f10b8fba844dcc6ab81748fe57fd8d1210b16ced9634e87f60425e3865de7

For Avalanche Fuji: 

https://testnet.snowtrace.io/tx/0x67befec299ef77a1848d698eb7ebd37efc2e4875f1318a439c6773c95867d12a

https://testnet.snowtrace.io/tx/0x0e20a88face15370f98f8e7e1d9ed4f9fc158e4d81f80d004a43dba73a9fb790

https://testnet.snowtrace.io/tx/0x8286b079e18a82cc116f86408d9cd0053d798edcc2913ebc2f7268f6a43a6daa

https://testnet.snowtrace.io/tx/0xa9c0a9cc5de6bd4ce4383c2cfa3402b26da62f978c0e9605f42021f6158d75ba

https://testnet.snowtrace.io/tx/0x1d330807c448dc59864f989ca9c87273a5d953541e7422b1e6697f7fd90fcdc3

### Zero-Knowledge Proof Generation/Verification Times

Proof Generation Time for Sender: 147 seconds

Proof Generation Time for Receicer: 145 seconds

The proofs are verified on-chain, without requiring any time cost.

## Some Maths

The sender balance $\beta_s$, the receiver balance $\beta_r$ and the transaction amount $\Delta$ are hidden values and only their commitments $c^\beta_s, c^\beta_r$ and $c^\Delta$ are publicly stored in the smart contract after masked by the blind factors $bf^\beta_s, bf^\beta_r$ and $bf^\Delta$ with the following way:

$$
\begin{align}
& c^\beta_s = Comm(\beta_s, bf^\beta_s) \\
& c^\beta_r = Comm(\beta_r, bf^\beta_r) \\
& c^\Delta = Comm(\Delta, bf^\Delta)
\end{align}
$$

\noindent
where $Comm$ is the commitment function. The transaction amount to be deposited is shared after the encryption with the receiver public key $pk^r$. Later, the receiver performs the decryption with its own secret key $sk^r$:

$$
\begin{align}
& E = Enc([\Delta, bf^\Delta], pk^r) \\
& [\Delta, bf^\Delta] = Dec([E], sk^r) 
\end{align}
$$

\noindent
where $Enc$ and $Dec$ are the encryption and decryption functions.

Later, both the sender and the receiver must generate their corresponding proofs $\pi^s$ and $\pi^r$ off-chain to show that their balances are updated accordingly:

$$
\begin{align}
\pi^s = ZkpGen([& \beta_s^{t+1} = \beta_s^{t} - \Delta], \nonumber \\
& [bf^\beta_s, bf^\Delta, c^\beta_s, c^\Delta]) \\
\pi^r = ZkpGen([& \beta_r^{t+1} = \beta_r^{t} + \Delta], \nonumber \\
& [bf^\beta_r, bf^\Delta, c^\beta_r, c^\Delta]) \\
\end{align}
$$

\noindent
where $ZkpGen$ is the zero-knowledge proof generation function and $t$ is the time point. The proofs generated must be later verified on-chain with respect to the commitments stored in the contract:

$$
\begin{align}
b^s = ZkpVfy([& \pi^s, c^\beta_s, c^\Delta]) \\
b^r = ZkpVfy([& \pi^r, c^\beta_r, c^\Delta])
\end{align}
$$

\noindent
where $ZkpVfy$ is the zero-knowledge proof verification function; and $b^s$ and $b^r$ are the boolean outputs. The given theoretical representation above provides the security of the proposed protocol.

## Web User Interface

Deploy Contract...   Get Request...   Give Request...

<img src="https://github.com/GoshgarIsmayilov/PTTS/blob/master/auxiliary/screenshots/deploy.png" width="33%"/> <img src="https://github.com/GoshgarIsmayilov/PTTS/blob/master/auxiliary/screenshots/get.png" width="30%"/> <img src="https://github.com/GoshgarIsmayilov/PTTS/blob/master/auxiliary/screenshots/give.png" width="33%"/>

Deposit Tokens...   Withdraw Tokens... 

<img src="https://github.com/GoshgarIsmayilov/PTTS/blob/master/auxiliary/screenshots/send.png" width="30%"/> <img src="https://github.com/GoshgarIsmayilov/PTTS/blob/master/auxiliary/screenshots/receive.png" width="30%"/>

# Balance Range Disclosure Attack

The users and the transactions between these users are randomly generated with respect to the number of users and the number of transactions parameters, 
respectively. The transactions to be disclosed to the adverserial entities are also randomly selected among all the transactions. The values for the 
network solution times and the error rate 20 metrics are the average of 20 different runs and in each run, balance of a randomly selected user is 
attacked. During the experiments, (1) the number of addresses changes in the range of 100 and 1,000,000, (2) the number of transactions changes in the 
range of 100 and 1,000,000 and (3) the default total token supply is 1,000,000 and default transaction leakage ratio is 0.5. We have employed Google 
OR-Tools [8] and three different versions of the Parallel Network Simplex algorithm [9] to solve the minimum cost flow network. These versions include 
PNS-Seq which is the sequential baseline network solver, PNS-Omp which is the parallel network solver by using OpenMP [10] and finally PNS-Omp-Avx2 which 
is the parallel and the advanced vector extended network solver for further acceleration. All the tests are performed upon MacBook Pro Notebook with a 
2.6 GHz Intel Core i7 processor, 16 GB memory and 6 cores. 

## To Run

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

## Some Maths

Let $G = (V, E)$ be a directed graph where $V$ is the set of nodes (i.e.  users) and $E$ is the set of edges (i.e. transactions). $E^*$ is the subset of transactions that are already leaked/sold to a particular organization in the blockchain. Each node $i$ is associated with a supply value $b_i$ where the source node $S$ supplies all the tokens while the sink node $T$ demands these tokens and the rest of the nodes have $b_i$ set to 0. The node corresponding to the user whose balance is in our focus is denoted as $U$. Each edge between the nodes $i$ and $j$ is also associated with lower/upper bounds $[l\_{ij}, u\_{ij}]$  on the feasible flow that can pass through the edge and a cost value $c_{ij}$ to be used in the objective function. For each edge corresponding to a leaked transaction, the lower and upper bounds are the same and equal to the transaction amount $v_{ij}$. For the remaining non-leaked transactions, we take $l_{ij}$ as 0 and $u_{ij}$ as the total token supply. The decision variable (i.e. flow) on the edge is denoted as $x_{ij}$. The balance range disclosure problem as the minimum cost flow network problem with the two objectives are defined as follows: 

$$
\begin{equation}
min. \sum_{(i, j) \in E} c_{ij} x_{ij} = -c_{UT} x_{UT}
\end{equation}
$$

$$
\begin{equation}
min. \sum_{(i, j) \in E} c_{ij} x_{ij} = +c_{UT} x_{UT}
\end{equation}
$$

\noindent
which are both subject to the following same constraints:

$$
\begin{align}
s.t. & \sum_{(i, j) \in E} x_{ij} - \sum_{(j, i) \in E} x_{ij} = b_i, \forall i \in V \nonumber \\
& l_{ij} \leq x_{ij} \leq u_{ij} , \forall (i, j) \in E \nonumber \\
& l_{ij} = u_{ij} = v_{ij}, \forall (i, j) \in E^* \nonumber \\
& b_{S} = b_{total} \nonumber \\
& b_{T} = -b_{total} \nonumber \\
\end{align}
$$

\noindent
Here, $b_{total}$ is the total token supply to the blockchain. The eqns. (1) and (2) are the objectives of the first and the second minimum cost flow network problems respectively while the eqn. (3) are the common constraints.

# Publications to Read

1. Ethers Javascript Library, URL: https://docs.ethers.io/v5/

2. Eccrypto Javascript Library, URL: https://www.npmjs.com/package/eccrypto

3. J. Eberhardt, S. Tai, "Zokrates-scalable privacy-preserving off-chain computations", IEEE International Conference on Internet of Things (iThings) 
and IEEE Green Computing and Communications (GreenCom) and IEEE Cyber, Physical and Social Computing (CPSCom) and IEEE Smart Data (SmartData),
pp. 1084-1091, 2018.

4. Browserify Bundler, URL: https://browserify.org

5. Webpack Bundler, URL: https://webpack.js.org

6. Solidity Language, URL: https://docs.soliditylang.org/en/v0.8.15/

7. Remix Compiler, URL: https://remix.ethereum.org

8. Google OR-Tools, URL: https://developers.google.com/optimization

9. Parallel network simplex algorithm for the minimum cost flow problem, URL: Phttps://github.com/gokcehan/pns

10. L. Dagum, R. Menon, "OpenMP: an industry standard API for shared-memory programming", IEEE computational science and engineering, vol. 5, no. 1, 
pp. 46-55, 1998.

11. Boost Align Library, URL: https://www.boost.org/doc/libs/1_79_0/doc/html/align.html

# Disclaimer

This software is made available for educational purposes only.









