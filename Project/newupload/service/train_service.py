import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader, random_split, ConcatDataset
import os


class SignalDataset(Dataset):
    """ Signal dataset."""
    # Initialize your data, download, etc.

    def __init__(self, directoryPath):
        signals = getSignalTensor(directoryPath)
        
        self.len = signals.shape[0]
        self.x_data = signals

        results = pd.read_pickle(os.path.join(directoryPath,"target.pkl"))
        self.y_data = torch.from_numpy(results.values)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len


def getSignalTensor(path):
    all_signals = []

    path, direct, files = next(os.walk(path))
    #leggo il file relativo ad ogni canale
    nChn = len(files) - 1
    for i in range(nChn):
        sig = pd.read_pickle(os.path.join(path,"chn"+str(i)+".pkl"))
        all_signals.append(torch.tensor(sig.values))

    #unisco tutti i canali in un unico tensore (3d)
    signals_tensor = torch.stack(all_signals, dim=0)
    #trasposta lungo dimensione 0 -> da una faccia per canale a una faccia per finestra
    signals_tensor = signals_tensor.transpose(0,1)
    #ora ho un "cubo", ogni faccia contiene una finestra, con una riga per ogni canale
    return signals_tensor



class ConvNet(nn.Module):
    def __init__(self, channels, windowSize):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv1d(channels, 10, kernel_size=10, stride=5, padding=10-1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )
        outL1 = int(((windowSize - 10 + 9*2)/5 + 1)/2)

        self.layer2 = nn.Sequential(
            nn.Conv1d(10, 5, kernel_size=5, stride=4, padding= 4),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )
        
        outL2 = int(((outL1 - 5 + 4*2)/4 + 1)/2)
        
        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(outL2*5, 15)
  
        self.fc3 = nn.Linear(15, 2)
        #softmax dim=1 -> normalizza riga per riga (?)
        self.soft = nn.Softmax(1)


    def forward(self, x):
        x = x.float()
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(1,-1)
        out = self.drop_out(out)
        out = self.fc1(out)
        # out = self.fc2(out)
        out = self.fc3(out)
        # out = self.soft(out)

        return out

def k_win_train(model, dataset, num_epochs):
    learning_rate = 0.001
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        print(f'Epoch [{epoch+1}/{num_epochs}]')
        #split the dataset into train and test
        if(dataset.__len__() % 0.8 == 0):
            train_lenght = int(dataset.__len__() * 0.8)
        else:
            train_lenght = int(dataset.__len__() * 0.8)+1
        
        test_lenght = dataset.__len__() - train_lenght
        
        train_dataset, test_dataset = random_split(dataset, (train_lenght, test_lenght))

        train_loader = DataLoader(dataset=train_dataset,
                                batch_size=1,
                                shuffle=True)
        
        test_loader = DataLoader(dataset=test_dataset,
                                batch_size=1,
                                shuffle=True)
        model = model.train()
        tot=0
        
        #training
        for i, (data, target) in enumerate(train_loader):
            x = data
            y = target.reshape(1).long()
            outputs = model(x)
            loss = criterion(outputs, y)
            # Backprop and perform Adam optimisation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Track the accuracy
            total = y.size(0)
            _, predicted = torch.max(outputs.data, 1)
            if(predicted.item() == target.item()):
                tot = tot+1
        totP = tot*100/train_loader.__len__()
        print("accuracy: ", tot, "/", train_loader.__len__(), " (",totP,"%)")
        
        #validation
        tot=0
        model = model.eval()
        for i, (data, target) in enumerate(test_loader):
            x = data
            result = model(x)
            _, predicted = torch.max(result, 1)
            if(predicted.item() == target.item()):
                tot = tot+1
        totP = tot*100/test_loader.__len__()
        print("accuracy TEST: ", tot, "/", test_loader.__len__(), " (",totP,"%)")
    
    return totP