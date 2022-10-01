var eccrypto = require("eccrypto");

async function encrypt(publicKey, plaintext){
    var encrypted = await eccrypto.encrypt(Buffer.from(publicKey, "hex"), Buffer.from(plaintext));
    for (var key in encrypted) {
      encrypted[key] = encrypted[key].toString("hex");
    }
    encrypted = btoa(JSON.stringify(encrypted));
    console.log(encrypted);
}

encrypt("043809548b407a0463cbc15512bf2ad9b8e883b5758c297908c543e711bfc3abfab208ea0b49125995b6baf293e3bee817cfff5cc36b67f39094a69b9d0178714f", "500")