var eccrypto = require("eccrypto");

async function decrypt(privateKey, ciphertext) {
    ciphertext = JSON.parse(atob(ciphertext));
    for (var key in ciphertext) {
      ciphertext[key] = Buffer.from(ciphertext[key],"hex");
    }
    var plaintext = await eccrypto.decrypt(Buffer.from(privateKey, "hex"), ciphertext);
    console.log(plaintext.toString());
}

decrypt("7e5bfb82febc4c2c8529167104271ceec190eafdca277314912eaabdb67c6e5f", "eyJpdiI6ImEyNTljYzcwYWU0NTNkZGE0OGNlMTE3NmQ2YzE2MGZlIiwiZXBoZW1QdWJsaWNLZXkiOiIwNGZlMWJlZTNiODE0ODYzODEwMGU5YjUwZDE2MzNjOWVkNjJkMjkxYTA1YjVhNjFhMDU3ZmFkN2Q2MWFlN2JhNTE0MmYwYWQ5NjhiZGVjMjRhYTM3MmVmYjk4NjhmODEzZGIyYTI3OWIyY2YyYjU4YjBkY2I2ZWFjM2E2MDU5N2JhIiwiY2lwaGVydGV4dCI6IjAwMWQ3ZDdmYWY4OTk2ZGE0YjkwMTJlNDQ4MWIyMzYzIiwibWFjIjoiZWFkYmQ2MTRlZjQ4NmNiMmE2MjdkMmJlYzI4NGM3ZTI0ZDJjMTJlOTg4ODhlOTE5MjhjN2I2ODMzZDJiODBkMSJ9")
