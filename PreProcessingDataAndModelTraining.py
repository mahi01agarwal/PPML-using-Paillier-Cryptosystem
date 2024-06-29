import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression
import pickle
import json
import os
import re

# Preprocess the dataset
def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')
    df["Ram"] = df["Ram"].str.replace("GB", "").astype('int32')
    df["Weight"] = df["Weight"].str.replace("kg", "").astype('float32')

    def cat_os(inp):
        if inp == 'Windows 10' or inp == 'Windows 7' or inp == 'Windows 10 S':
            return 'Windows'
        elif inp == 'macOS' or inp == 'Mac OS X':
            return 'Mac'
        else:
            return 'Others/No OS/Linux'

    df['os'] = df['OpSys'].apply(cat_os)
    df = df.drop('OpSys', axis='columns')

    def fetch_processor(text):
        if text == 'Intel Core i7' or text == 'Intel Core i5' or text == 'Intel Core i3':
            return text
        else:
            if text.split()[0] == 'Intel':
                return 'Other Intel Processor'
            else:
                return 'AMD Processor'

    df['Cpu Name'] = df['Cpu'].apply(lambda x: " ".join(x.split()[0:3]))
    df['Cpu brand'] = df['Cpu Name'].apply(fetch_processor)
    df['ProcessorSpeed'] = df['Cpu'].apply(lambda x: re.findall(r'\d+\.\d+?', x))

    def convert_to_float(lst):
        return float(lst[0]) if lst else None

    df['ProcessorSpeed'] = df['ProcessorSpeed'].apply(convert_to_float)
    df = df.drop(['Cpu', 'Cpu Name'], axis='columns')
    df['Gpu brand'] = df['Gpu'].apply(lambda x: x.split()[0])
    df['GpuModel'] = df['Gpu'].apply(lambda x: re.findall(r'\d+', x))
    df['GpuModel'] = df['GpuModel'].apply(convert_to_float)
    df = df.drop('Gpu', axis='columns')

    df['Memory'] = df['Memory'].astype(str).replace('\.0', '', regex=True)
    df["Memory"] = df["Memory"].str.replace('GB', '')
    df["Memory"] = df["Memory"].str.replace('TB', '000')
    new = df["Memory"].str.split("+", n=1, expand=True)

    df["first"] = new[0].str.strip()
    df["second"] = new[1]

    df["Layer1HDD"] = df["first"].apply(lambda x: 1 if "HDD" in x else 0)
    df["Layer1SSD"] = df["first"].apply(lambda x: 1 if "SSD" in x else 0)
    df["Layer1Hybrid"] = df["first"].apply(lambda x: 1 if "Hybrid" in x else 0)
    df["Layer1Flash_Storage"] = df["first"].apply(lambda x: 1 if "Flash Storage" in x else 0)

    df['first'] = df['first'].str.replace(r'\D', '', regex=True)
    df["second"].fillna("0", inplace=True)
    df["Layer2HDD"] = df["second"].apply(lambda x: 1 if "HDD" in x else 0)
    df["Layer2SSD"] = df["second"].apply(lambda x: 1 if "SSD" in x else 0)
    df["Layer2Hybrid"] = df["second"].apply(lambda x: 1 if "Hybrid" in x else 0)
    df["Layer2Flash_Storage"] = df["second"].apply(lambda x: 1 if "Flash Storage" in x else 0)
    df['second'] = df['second'].str.replace(r'\D', '', regex=True)
    df["first"] = df["first"].astype(int)
    df["second"] = df["second"].astype(int)

    df["HDD"] = (df["first"] * df["Layer1HDD"] + df["second"] * df["Layer2HDD"])
    df["SSD"] = (df["first"] * df["Layer1SSD"] + df["second"] * df["Layer2SSD"])
    df["Hybrid"] = (df["first"] * df["Layer1Hybrid"] + df["second"] * df["Layer2Hybrid"])
    df["Flash_Storage"] = (df["first"] * df["Layer1Flash_Storage"] + df["second"] * df["Layer2Flash_Storage"])

    df = df.drop(['first', 'second', 'Layer1HDD', 'Layer1SSD', 'Layer1Hybrid',
                  'Layer1Flash_Storage', 'Layer2HDD', 'Layer2SSD', 'Layer2Hybrid',
                  'Layer2Flash_Storage', 'Memory'], axis='columns')

    df['TouchScreen'] = df['ScreenResolution'].apply(lambda x: 1 if 'Touchscreen' in x else 0)
    df['IPSPanel'] = df['ScreenResolution'].apply(lambda x: 1 if 'IPS Panel' in x else 0)
    new = df['ScreenResolution'].str.split('x', expand=True)
    df['Y_res'] = new[1]
    df['X_res'] = new[0].apply(lambda x: re.findall(r'\d+', x)).apply(lambda x: x[0])
    df['X_res'] = df['X_res'].astype('int')
    df['Y_res'] = df['Y_res'].astype('int')
    df = df.drop('ScreenResolution', axis='columns')
    df['PPI'] = ((df['X_res'] ** 2) + (df['Y_res']) ** 2) ** 0.5 / df['Inches']
    df = df.drop(['Inches', 'X_res', 'Y_res'], axis='columns')
    df = df.dropna(how='any')

    return df

# Train the model and save the ColumnTransformer
def train_model(df):
    X = df.drop(columns=['Price'])
    y = np.log(df['Price'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=0)

    categorical_features = ['Company', 'TypeName', 'Gpu brand', 'os', 'Cpu brand']  # Updated list
    X_train[categorical_features] = X_train[categorical_features].astype(str)
    X_test[categorical_features] = X_test[categorical_features].astype(str)

    col_tnf = ColumnTransformer(transformers=[
        ('col_tnf', OneHotEncoder(drop='first'), categorical_features)
    ], remainder='passthrough')

    X_train_transformed = col_tnf.fit_transform(X_train)

    # Save the ColumnTransformer
    with open('col_tnf.pkl', 'wb') as file:
        pickle.dump(col_tnf, file)

    X_test_transformed = col_tnf.transform(X_test)

    regression_model = LinearRegression()
    regression_model.fit(X_train_transformed, y_train)
    y_pred = regression_model.predict(X_test_transformed)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print('R2 score:', r2)
    print('MAE:', mae)

    coef_list = regression_model.coef_.tolist()
    intercept = regression_model.intercept_

    output_dir = 'Encrypted_ModelParameters'
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, 'Coefficients.json'), "w") as file:
        json.dump(coef_list, file)
    
    with open(os.path.join(output_dir, 'Intercept.json'), 'w') as file:
        json.dump(intercept, file)

if __name__ == "__main__":
    # Preprocess the data
    df = preprocess_data('Data\laptop_data.csv')
    
    # Save preprocessed data to CSV
    df.to_csv("Data\Preprocessed_data.csv", index=False)
    
    # Train the model and save the ColumnTransformer
    train_model(df)
