const { initialize } = require('zokrates-js/node');

function generate_sender_proof(value, before, valueBlind, beforeBlind, afterBlind, valueHash, beforeHash, afterHash){
    initialize().then((zokratesProvider) => {
        const source = 'import "hashes/sha256/512bitPacked" as sha256packed\n def main(private field value, private field before, private field valueBlind, private field beforeBlind, private field afterBlind, field valueHash, field beforeHash, field afterHash) -> (field):\n field[2] priBefore = sha256packed([0, 0, beforeBlind, before])\n field[2] priAfter = sha256packed([0, 0, afterBlind, before-value])\n field[2] priValue = sha256packed([0, 0, valueBlind, value])\n field result = if(value <= before && priBefore[1] == beforeHash && priAfter[1] == afterHash && priValue[1] == valueHash) then 1 else 0 fi\n return result';
        const artifacts = zokratesProvider.compile(source);
        const keypair = zokratesProvider.setup(artifacts.program);
        const verifier = zokratesProvider.exportSolidityVerifier(keypair.vk, "v1");
        const { witness, output } = zokratesProvider.computeWitness(artifacts, [value, before, valueBlind, beforeBlind, afterBlind, valueHash, beforeHash, afterHash]);
        const proof = zokratesProvider.generateProof(artifacts.program, witness, keypair.pk);

        console.log(proof.proof.a);
        console.log(proof.proof.b);
        console.log(proof.proof.c);
    });
}

generate_sender_proof("50", "1000", "0", "0", "0", "88795392107901394003693036759300599309", "160447523714545220416709952320130456769", "274640773982596794647287725883761604086")