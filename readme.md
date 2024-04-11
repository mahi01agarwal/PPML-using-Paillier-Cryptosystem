# PPML using Paillier Cryptosystem

## Overview
PPML (Privacy-Preserving Machine Learning) using the Paillier Cryptosystem is a project aimed at developing a secure and privacy-preserving machine learning system using the Paillier encryption scheme. This project focuses on implementing machine learning algorithms while ensuring that sensitive data remains encrypted during processing, thus preserving the privacy of individual data points.

Linear regression is employed as the modeling technique to establish the relationship between the laptop features and their corresponding prices. By identifying the optimal coefficients that minimize the residuals, the model can accurately predict the prices of laptops based on their features. The use of linear regression in conjunction with the Paillier cryptosystem allows for both accuracy and privacy in the prediction process.

## Features
- Implements machine learning algorithms using the Paillier encryption scheme to perform computations on encrypted data.
- Ensures data privacy by encrypting data before processing.

## How does it work?
- The model is trained on the normal values and the values for the coefficient of fitted lines are derived.
- Then the user provides the encrypted data and the public key which is used to encrypt the data.
- Then the computations are done on this data using paillier block of code and the prediction is returned in the encrypted form.
- The user then decrypts this prediction using private key and gets the desired result.

## Usage
1. **Installation**: Clone the repository and install the required dependencies.
   ```
   git clone https://github.com/mahi01agarwal/PPML-using-Paillier-Cryptosystem.git
   cd PPML-using-Paillier-Cryptosystem
   pip install -r requirements.txt
   ```



## Contributing
Contributions to PPML using Paillier Cryptosystem are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

