import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader, random_split, ConcatDataset
import os


class SignalDataset(Dataset):
    """ Signal dataset."""

    def __init__(self, directoryPath):
        signals = getSignalTensor(directoryPath)
        
        self.len = signals.shape[0]
        self.x_data = signals

        results = pd.read_pickle(os.path.join(directoryPath,"target.pkl"))
        self.y_data = torch.from_numpy(results.values).squeeze(1)

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

    return combineAllTensor(all_signals)


def combineAllTensor(channels_tensors_list):
    """[Prende una lista di tensori, ognuno contenente le finestre di segnali di un singolo canale.
    Le combina in un tensore 3D, diviso in finestre contenenti tutti i canali ]
    
    Arguments:
        channels_tensors_list {[list of tensor]} -- [lista di tensori, uno per canale]
    """
    #unisco tutti i canali in un unico tensore (3d)
    signals_tensor = torch.stack(channels_tensors_list, dim=0)
    #trasposta lungo dimensione 0 -> da una faccia per canale a una faccia per finestra
    signals_tensor = signals_tensor.transpose(0,1)
    #ora ho un "cubo", ogni faccia contiene una finestra, con una riga per ogni canale
    return signals_tensor

class ConvNet(nn.Module):
    def __init__(self, channels, windowSize):
        super(ConvNet, self).__init__()
        if(windowSize < 1662):
            raise Exception("Increase window size")
        self.layer1 = nn.Sequential(
            nn.Conv1d(channels, 10, kernel_size=10, stride=5, padding=10-1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=15, stride=10)
        )
        outL1 = int(((windowSize - 10 + 9*2)/5 + 1)) #conv
        outL1 = int(((outL1 - 15)/10) +1 ) #pool

        self.layer2 = nn.Sequential(
            nn.Conv1d(10, 5, kernel_size=5, stride=4, padding= 4),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=10, stride=5)
        )

        # self.layer3 = nn.Sequential(
        #     nn.Conv1d(10, 30, kernel_size=2, stride=1),
        #     nn.ReLU(),
        #     nn.MaxPool1d(kernel_size=2, stride=2)
        # )

        
        
        outL2 = int(((outL1 - 5 + 4*2)/4 + 1)) #conv
        outL2 = int(((outL2-10)/5) + 1) #pool
    
        self.linearInput = outL2*5

        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(self.linearInput, 15)
        # self.fc2 = nn.Linear(100, 10)
        self.fc3 = nn.Linear(15, 2)
        #softmax dim=1 -> normalizza riga per riga (?)
        self.soft = nn.Softmax(1)


    def forward(self, x):
        x = x.float()
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(-1, self.linearInput)
        out = self.drop_out(out)
        out = self.fc1(out)
        # out = self.fc2(out)
        out = self.fc3(out)
        out = self.soft(out)

        return out


def k_win_train(model, dataset_list, num_epochs):
    dataset = ConcatDataset(dataset_list)
    if (dataset.__len__() < 2):
        raise Exception("Dataset is too small")
    learning_rate = 0.001
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        print(f'Epoch [{epoch+1}/{num_epochs}]')
        #split the dataset into train and test
        
        train_lenght = int(dataset.__len__() * 0.8)
        test_lenght = dataset.__len__() - train_lenght

        train_dataset, test_dataset = random_split(dataset, (train_lenght, test_lenght))

        train_loader = DataLoader(dataset=train_dataset,
                                batch_size=10,
                                shuffle=True)
        
        test_loader = DataLoader(dataset=test_dataset,
                                batch_size=10,
                                shuffle=True)
        
        #training
        train_step(model, train_loader, learning_rate, criterion, optimizer)
        
        #validation
        totP = validation_step(model, test_loader)
    
    return totP


def k_fold_train(model, dataset_list, num_epochs):
    learning_rate = 0.001
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    if (dataset_list.__len__() < 2):
        raise Exception("Database is too small")
    train_loader_list = []
    for d in dataset_list:
        train_loader = DataLoader(dataset=d,
                                batch_size=10,
                                shuffle=True)
        train_loader_list.append(train_loader)

    for epoch in range(num_epochs):
        print(f'Epoch [{epoch+1}/{num_epochs}]')
        #cross-validation
        temp = train_loader_list.copy()
        index = epoch % len(train_loader_list)
        test_loader = train_loader_list[index]
        temp.remove(test_loader)    
        
        for train_loader in temp:
            train_step(model, train_loader, learning_rate, criterion, optimizer )

        totP = validation_step(model, test_loader)
    return totP


def train_step(model, train_loader, learning_rate, criterion, optimizer):
    model = model.train()
    tot = 0
    n = 0
    for i, (data, target) in enumerate(train_loader):
        x = data
        y = target.long()
        outputs = model(x)
        #calculate the loss
        loss = criterion(outputs, y)
        # set old gradients to zero
        optimizer.zero_grad()
        # calculate new gradients (backpropagation) and add to the .grad attribute 
        loss.backward()
        # update weights
        optimizer.step()

        # Track the accuracy

        tot = tot + outputs.argmax(dim=1).eq(target).sum().item()
        n = n + outputs.__len__()
    totP = tot*100/n
    print("accuracy: ", tot, "/", n, " (%.2f"%totP,"%)")
    return totP


def validation_step(model, test_loader):
    tot=0
    n = 0
    model = model.eval()
    for i, (data, target) in enumerate(test_loader):
        x = data
        outputs = model(x)
        tot = tot + outputs.argmax(dim=1).eq(target).sum().item()
        n = n + outputs.__len__()
    totP = tot*100/n
    print("accuracy TEST: ", tot, "/", n, " (%.2f"%totP,"%)")
    return totP


class EvalDataset(Dataset):
    # Initialize your data, download, etc.

    def __init__(self, tensor):
        self.len = tensor.shape[0]
        self.x_data = tensor

    def __getitem__(self, index):
        return self.x_data[index]

    def __len__(self):
        return self.len


class ModularConv(nn.Module):
    def __init__(self, conv_list, linear_input, linear_list):
        # self.layer_list = []
        super(ModularConv, self).__init__()
 
        self.conv = nn.Sequential(*conv_list)

        self.drop_out = nn.Dropout()
        #roba layer lineare
        self.linear_input = linear_input
        self.linear = nn.Sequential(*linear_list)

        self.soft = nn.Softmax(1)

    def forward(self, x):
        x = x.float()
        x = self.conv(x)
        
        #roba layer lineare
        x = x.reshape(-1, self.linear_input)
        x = self.drop_out(x)
        x = self.linear(x)

        x = self.soft(x)
        return x
