const { initialize } = require('zokrates-js/node');

function hash(c, d) {
    initialize().then((zokratesProvider) => {
        const code = 'import "hashes/sha256/512bitPacked" as sha256packed\n def main(private field c, private field d) -> field:\n field[2] h = sha256packed([0, 0, c, d])\n return h[1]';
        const artifacts = zokratesProvider.compile(code);
        var { witness, output } = zokratesProvider.computeWitness(artifacts, [c, d]);
        console.log(output);
        var a = zokratesProvider.computeWitness(artifacts, [c, d]);
        console.log(a.output);       
    });
}

hash("0", "50")