import phe as paillier
import json
from sklearn.compose import ColumnTransformer
import pickle

def storeKeys():
    # Generate Paillier public-private key pair
    public_key, private_key = paillier.generate_paillier_keypair()
    
    # Store keys in a dictionary
    keys = {
        'public_key': {'n': public_key.n},
        'private_key': {'p': private_key.p, 'q': private_key.q}
    }
    
    # Save keys to a JSON file
    with open('custkeys.json', 'w') as file: 
        json.dump(keys, file)

def getKeys():
    # Load keys from JSON file
    with open('custkeys.json', 'r') as file: 
        keys = json.load(file)
        # Reconstruct Paillier public-private key pair
        pub_key = paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
        priv_key = paillier.PaillierPrivateKey(pub_key, keys['private_key']['p'], keys['private_key']['q'])
        return pub_key, priv_key    

def serializeData(public_key, data):
    # Encrypt data using the provided public key
    encrypted_data_list = [public_key.encrypt(x) for x in data]
    
    # Prepare data for serialization
    encrypted_data = {
        'public_key': {'n': public_key.n},
        'values': [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
    }
    
    # Serialize encrypted data
    serialized = json.dumps(encrypted_data)
    return serialized         

def preprocessData(data):
    # Load the ColumnTransformer object from file
    with open('col_tnf.pkl', 'rb') as file:
        col_tnf = pickle.load(file)
    
    # Transform the data using the loaded ColumnTransformer
    trans_data = col_tnf.transform(data)
    
    # Reshape the transformed data
    new_data = trans_data.reshape(-1)
    return new_data

def main():
    # Generate and store Paillier keys
    storeKeys()
    
    # Load Paillier keys
    pub_key, priv_key = getKeys()
    
    # Sample data: ['Company', 'TypeName', 'Ram', 'OpSys', 'Weight', 'os', 'Cpu brand', 'ProcessorSpeed', 'Gpu brand', 'GpuModel', 'HDD', 'SSD', 'Hybrid', 'Flash_Storage', 'TouchScreen', 'IPSPanel', 'PPI']
    data = [['Dell', 'Notebook', 8, 'Windows 10', 2.00, 'Windows', 'Intel Core i7', 2.8, 'Nvidia', 1050.0, 0, 256, 0, 0, 0, 0, 141.0211998]]
    
    # Preprocess the data
    new_data = preprocessData(data)
    
    # Serialize and save the preprocessed data
    datafile = serializeData(pub_key, new_data)
    with open('data.json', 'w') as file: 
        json.dump(datafile, file)

if __name__ == "__main__":
    main()
