import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pandas as pd
from sklearn.preprocessing import StandardScaler


class Autoencoder(nn.Module):
    def __init__(self, input_size, encoding_size):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, encoding_size),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_size, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, input_size)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


class SCRNASeqDataset(Dataset):
    def __init__(self, data):
        self.data = data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]


datas = pd.read_csv('CRISPRGeneEffect.csv', index_col=0)
scaler=StandardScaler()
scaler.fit(datas)
scaled_data=scaler.transform(datas)

# convert scaled data to a PyTorch tensor
data = torch.FloatTensor(scaled_data)


# Define the hyperparameters
input_size = data.shape[1]
print(input_size)
encoding_size = 50
batch_size = 32
learning_rate = 0.001
num_epochs = 40


model = Autoencoder(input_size, encoding_size)


criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)


dataset = SCRNASeqDataset(data)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)


for epoch in range(num_epochs):
    for batch in dataloader:
        optimizer.zero_grad()
        x = batch.float()
        reconstructed = model(x)
        loss = criterion(reconstructed, x)
        loss.backward()
        optimizer.step()
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}')

# Use the autoencoder to reduce the dimensionality of the data
encoded_data = model.encoder(data.float()).detach().numpy()
