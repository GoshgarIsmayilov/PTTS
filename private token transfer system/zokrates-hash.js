import { initialize } from 'zokrates-js';

export default async function zokrates_hash(a, b, c, d, e, f) {
  const hash = initialize().then((zokratesProvider) => {
    // const code = 'import "hashes/sha256/512bitPacked" as sha256packed\n def main(private field c, private field d) -> field:\n field[2] h = sha256packed([0, 0, c, d])\n return h[1]';
    const code = 'import "hashes/sha256/512bitPacked" as sha256packed\n def main(private field a, private field b, private field c, private field d, private field e, private field f) -> (field, field, field):\n field[2] h1 = sha256packed([0, 0, a, b])\n field[2] h2 = sha256packed([0, 0, c, d])\n field[2] h3 = sha256packed([0, 0, e, f])\n return h1[1], h2[1], h3[1]';
    const artifacts = zokratesProvider.compile(code);
    const { witness, output } = zokratesProvider.computeWitness(artifacts, [a, b, c, d, e, f]);
    return output;
  });
  return hash;
}