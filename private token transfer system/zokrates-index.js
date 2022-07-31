import zokrates_hash from './zokrates-hash';
import zokrates_sender_proof from './zokrates-sender';
import zokrates_receiver_proof from './zokrates-receiver'; 

window.zokrates_hash = async function(a, b, c, d, e, f){
    return await zokrates_hash(a, b, c, d, e, f);
}

window.zokrates_sender_proof = async function(value, before, valueBlind, beforeBlind, afterBlind, valueHash, beforeHash, afterHash){
    return await zokrates_sender_proof(value, before, valueBlind, beforeBlind, afterBlind, valueHash, beforeHash, afterHash);
}

window.zokrates_receiver_proof = async function(value, before, valueBlind, beforeBlind, afterBlind, valueHash, beforeHash, afterHash){
    return await zokrates_receiver_proof(value, before, valueBlind, beforeBlind, afterBlind, valueHash, beforeHash, afterHash);
}