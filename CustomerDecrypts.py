import phe as paillier
import json
import numpy as np

def getKeys():
    # Load keys from custkeys.json file
    with open('PaillierKeys\custkeys.json', 'r') as file: 
        keys = json.load(file)
        # Reconstruct Paillier public-private key pair
        pub_key = paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
        priv_key = paillier.PaillierPrivateKey(pub_key, keys['private_key']['p'], keys['private_key']['q'])
        return pub_key, priv_key 

def loadAnswer():
    # Load encrypted answer from answer.json file
    with open('Encrypted_Predicted_value\\answer.json', 'r') as file: 
        ans = json.load(file)
    # Parse the JSON data
    answer_data = json.loads(ans)
    return answer_data

def decryptAnswer(pub_key, priv_key, answer_data):
    # Reconstruct answer key from the loaded data
    answer_key = paillier.PaillierPublicKey(n=int(answer_data['pubkey']['n']))
    # Reconstruct encrypted answer from the loaded data
    answer = paillier.EncryptedNumber(answer_key, int(answer_data['values'][0]), int(answer_data['values'][1]))
    
    # Check if the answer key matches the user's private key
    if answer_key == pub_key:
        # Decrypt the answer
        decrypted_answer = priv_key.decrypt(answer)
        # Transform the decrypted answer (assuming it's logarithmic, for example)
        final_prediction = np.exp(decrypted_answer)
        return final_prediction
    else:
        print("Error: The answer key does not match the user's public key.")
        return None

def main():
    # Load user's public and private keys
    pub_key, priv_key = getKeys()
    # Load the encrypted answer
    answer_data = loadAnswer()
    # Decrypt and process the answer
    final_prediction = decryptAnswer(pub_key, priv_key, answer_data)
    # Print the final prediction
    if final_prediction is not None:
        print("Final Prediction:", final_prediction)

if __name__ == "__main__":
    main()
