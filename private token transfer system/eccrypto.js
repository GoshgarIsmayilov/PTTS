var eccrypto = require("eccrypto");

window.encrypt = async function(publicKey, plaintext){
    var encrypted = await eccrypto.encrypt(Buffer.from(publicKey, "hex"), Buffer.from(plaintext));
    for (var key in encrypted) {
      encrypted[key] = encrypted[key].toString("hex");
    }
    encrypted = btoa(JSON.stringify(encrypted));
    return(encrypted);
}

window.decrypt = async function(privateKey, ciphertext) {
    ciphertext = JSON.parse(atob(ciphertext));
    for (var key in ciphertext) {
      ciphertext[key] = Buffer.from(ciphertext[key],"hex");
    }
    var plaintext = await eccrypto.decrypt(Buffer.from(privateKey, "hex"), ciphertext);
    return(plaintext.toString());
}