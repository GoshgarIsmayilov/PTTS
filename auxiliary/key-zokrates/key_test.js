const { initialize } = require('zokrates-js/node');
const fs = require('fs');

function generate_sender_proof(a, b){
    initialize().then((zokratesProvider) => {
        const source = 'def main(private field a, field b) -> bool:\nreturn a * a == b';
        const artifacts = zokratesProvider.compile(source);
        const { witness, output } = zokratesProvider.computeWitness(artifacts, [a, b]);

        const pk = fs.readFileSync('proving.key');
        // var pkStr = Buffer.from(pk).toString('base64');
        pkStr = "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";
        const pkRestored = new Uint8Array(Buffer.from(pkStr, 'base64'));

        const proof = zokratesProvider.generateProof(artifacts.program, witness, pkRestored); 

        console.log(proof.proof.a);
        console.log(proof.proof.b);
        console.log(proof.proof.c); 
        console.log(proof.inputs); 
    });
}

generate_sender_proof("2", "4")

