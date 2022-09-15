import torch
import torch.nn as nn
import time
import pandas as pd
from sklearn import preprocessing
import numpy as np

class FCN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(FCN, self).__init__()
        self.input_size = input_size
        self.l1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out) 
        return out

model = FCN(1,1,1)
model = torch.load('model_finetune.pth')

TEST_DATA = 'test.csv'
TRAIN_DATA = 'train.csv'

test_df = pd.read_csv(TEST_DATA)
test_df = test_df[~test_df['Activity'].isin(['STANDING', 'WALKING'])]
features = [
    'tBodyAcc-mean()-X', 'tBodyAcc-mean()-Y', 'tBodyAcc-mean()-Z', 'tBodyAcc-std()-X',
    'tBodyAcc-std()-Y', 'tBodyAcc-std()-Z', 'tBodyAcc-max()-X', 'tBodyAcc-max()-Y',
    'tBodyAcc-max()-Z', 'tBodyAcc-min()-X', 'tBodyAcc-min()-Y', 'tBodyAcc-min()-Z',
    
    'tBodyGyro-mean()-X', 'tBodyGyro-mean()-Y', 'tBodyGyro-mean()-Z', 'tBodyGyro-std()-X',
    'tBodyGyro-std()-Y', 'tBodyGyro-std()-Z', 'tBodyGyro-max()-X', 'tBodyGyro-max()-Y',
    'tBodyGyro-max()-Z', 'tBodyGyro-min()-X', 'tBodyGyro-min()-Y', 'tBodyGyro-min()-Z',
    
    'tGravityAcc-std()-X', 'tGravityAcc-std()-Y', 'tGravityAcc-std()-Z', 'tGravityAcc-mad()-X',
    'tGravityAcc-mad()-Y', 'tGravityAcc-mad()-Z', 'tGravityAcc-max()-X', 'tGravityAcc-max()-Y',
    'tGravityAcc-max()-Z', 'tGravityAcc-min()-X', 'tGravityAcc-min()-Y', 'tGravityAcc-min()-Z',
    
    'Activity'
]

test_df = test_df[[f for f in features]]

X_test = test_df.iloc[:, :-1]
y_test = test_df[['Activity']]

le = preprocessing.LabelEncoder()
le.fit(y_test['Activity'].unique().tolist())
y_test = le.transform(y_test)

start_time = time.time()
data = torch.Tensor(X_test.iloc[1].astype(float))

with torch.no_grad():
    output = model(data)
    action = np.argmax(output)
    print(f"Inference time: {((time.time() - start_time) * 1000):.4f} ms")    
    print(action)