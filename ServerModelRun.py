import phe as paillier
import json
import numpy as np

# Function to load data from JSON file
def getData():
    with open('Encrypted_Data\data.json', 'r') as file: 
        d = json.load(file)
    data = json.loads(d)
    return data

# Function to load coefficients from JSON file
def getCoef():
    with open('Encrypted_ModelParameters\Coefficients.json', 'r') as file: 
        d = json.load(file) 
        coef = np.array(d)
    return coef  

# Function to load intercept from JSON file
def get_Intercept():
    with open('Encrypted_ModelParameters\Intercept.json', 'r') as file: 
        d = json.load(file)
    return d   

# Function to encrypt intercept using Paillier encryption
def get_encryted_intercept():
    data = getData()
    intercept = get_Intercept()
    public_key = paillier.PaillierPublicKey(n=int(data['public_key']['n']))
    encrypted_intercept = public_key.encrypt(intercept)
    return encrypted_intercept 

# Function to compute encrypted results using loaded data, coefficients, and encrypted intercept
def computeData():
    data = getData()
    mycoef = getCoef()
    intercept = get_encryted_intercept()
    pk = data['public_key']
    pubkey = paillier.PaillierPublicKey(n=int(pk['n']))
    enc_nums_rec = [paillier.EncryptedNumber(pubkey, int(x[0]), int(x[1])) for x in data['values']]
    results = (sum([mycoef[i] * enc_nums_rec[i] for i in range(len(mycoef))]) + intercept)
    return results, pubkey

# Function to serialize computed data and save it to a JSON file
def serializeData():
    results, pubkey = computeData()
    encrypted_data = {}
    encrypted_data['pubkey'] = {'n': pubkey.n}
    encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
    serialized = json.dumps(encrypted_data)
    return serialized

# Main function to execute the code
def main():
    datafile = serializeData()
    with open('Encrypted_Predicted_value\\answer.json', 'w') as file:
        json.dump(datafile, file)

if __name__ == "__main__":
    main()
