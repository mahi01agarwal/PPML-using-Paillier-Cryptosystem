# PPML using Paillier Cryptosystem

## Overview
PPML (Privacy-Preserving Machine Learning) using the Paillier Cryptosystem is a project aimed at developing a secure and privacy-preserving machine learning system using the Paillier encryption scheme. This project focuses on implementing machine learning algorithms while ensuring that sensitive data remains encrypted during processing, thus preserving the privacy of individual data points.

Linear regression is employed as the modeling technique to establish the relationship between the laptop features and their corresponding prices. By identifying the optimal coefficients that minimize the residuals, the model can accurately predict the prices of laptops based on their features. The use of linear regression in conjunction with the Paillier cryptosystem allows for both accuracy and privacy in the prediction process.

## Features
- Implements machine learning algorithms using the Paillier encryption scheme to perform computations on encrypted data.
- Ensures data privacy by encrypting data before processing.
- Encrypts and decrypts data using a public-private key pair.
- Performs linear regression to predict laptop prices while maintaining data privacy.

## How does it work?
1. **Key Generation and Storage:**
   - Generate a Paillier public-private key pair.
   - Store the keys securely in a JSON file.
   
2. **Data Preprocessing:**
   - Convert raw data into a suitable format for machine learning.
   - Serialize and encrypt the preprocessed data using the public key.

3. **Model Computation:**
   - Perform computations on the encrypted data using linear regression coefficients.
   - Encrypt the model's intercept using the public key.
   
4. **Prediction:**
   - Compute predictions on encrypted data.
   - Return predictions in encrypted form.
   
5. **Decryption:**
   - Decrypt the predictions using the private key.
   - Obtain the final prediction result.

## Project Structure

      
      PPML-using-Paillier-Cryptosystem/
      ├── Data/
      ├── Encrypted_Data/
      ├── Encrypted_ModelParameters/
      ├── Encrypted_Predicted_value/
      ├── PaillierKeys/
      ├── Tests/
      │ ├── test_CustomerDecrypts.py
      │ ├── test_CustomerEncrypts.py
      │ ├── test_ServerModelRun.py
      ├── col_tnf.pkl
      ├── CustomerDecrypts.py
      ├── CustomerEncrypts.py
      ├── LICENSE
      ├── PreProcessingDataAndModel.pkl
      ├── readme.md
      └── ServerModelRun.py

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/PPML-using-Paillier-Cryptosystem.git
   cd PPML-using-Paillier-Cryptosystem

## Usage
1. Generate Keys:
    ```sh
    python CustomerEncrypts.py
2. Encrypt Data:
    - Ensure your data is in the appropriate format.
    - Run the script to preprocess and encrypt data.
    ```sh
    python CustomerEncrypts.py
3. Compute Encrypted Predictions:
    ```sh
    python ServerModelRun.py
4. Decrypt Predictions:
    ```sh
    python CustomerDecrypts.py


## Contributing
Contributions to PPML using Paillier Cryptosystem are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

