import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from numpy import genfromtxt
import matplotlib as plt
from torch.utils.data import Dataset, DataLoader, random_split
from torch.autograd import Variable
import os


path = ["C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_03\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_04\\", #
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_15\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_16\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_18\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_21\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_26\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_01\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_02\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_34\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_35\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_36\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_06\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_13\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_16\\",
        #     "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_17\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_22\\",
    ]

def getSignalTensor(path):
    all_signals = []
    #leggo il file relativo ad ogni canale
    for i in range(23):
        sig = pd.read_csv(path+"chn"+str(i)+".csv",
                            header = None, dtype= np.float64)
        all_signals.append(torch.tensor(sig.values))

    #unisco tutti i canali in un unico tensore (3d)
    signals_tensor = torch.stack(all_signals, dim=0)
    #trasposta lungo dimensione 0 -> da una faccia per canale a una faccia per finestra
    signals_tensor = signals_tensor.transpose(0,1)
    #ora ho un "cubo", ogni faccia contiene una finestra, con una riga per ogni canale
    print("dim ", signals_tensor.shape)
    return signals_tensor




class SignalDataset(Dataset):
    """ Signal dataset."""
    # Initialize your data, download, etc.

    def __init__(self, directoryPath):
        # signals = pd.read_csv(path+"chn0.csv",
        #                       header=None, dtype=np.float64)
        signals = getSignalTensor(directoryPath)
        
        self.len = signals.shape[0]
        # self.x_data = torch.from_numpy(signals.values)
        self.x_data = signals
        results = pd.read_csv(directoryPath+"target.csv",
                              header=None, dtype=np.float64)
        self.y_data = torch.from_numpy(results.values)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len


class EvalDataset(Dataset):
    """ Dataset for prediction dataset."""
    # Initialize your data, download, etc.

    def __init__(self, directoryPath):
        signals = getSignalTensor(directoryPath)
        self.len = signals.shape[0]
        self.x_data = signals
        # results = pd.read_csv(directoryPath+"target.csv",
        #                       header=None, dtype=np.float64)
        # self.y_data = torch.from_numpy(results.values)

    def __getitem__(self, index):
        return self.x_data[index]

    def __len__(self):
        return self.len



class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv1d(23, 10, kernel_size=10, stride=5, padding=9),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=15, stride=10)
        )

        self.layer2 = nn.Sequential(
            nn.Conv1d(10, 5, kernel_size=5, stride=4, padding= 4),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=10, stride=5)
        )

        self.layer3 = nn.Sequential(
            nn.Conv1d(10, 30, kernel_size=2, stride=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )
        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(35, 15)
        self.fc2 = nn.Linear(100, 10)
        self.fc3 = nn.Linear(15, 2)
        self.soft = nn.Softmax(1)
        # self.fc2 = nn.Linear(256, 2)

    def forward(self, x):
        x = x.float()
        out = self.layer1(x)
        out = self.layer2(out)
        # out = self.layer3(out)
        out = out.reshape(1,-1)
        out = self.drop_out(out)
        # out = out.reshape(1, 45)
        out = self.fc1(out)
        # out = self.fc2(out)
        out = self.fc3(out)
        # out = self.soft(out)
        return out


def train():
    model = ConvNet()

    num_epochs = 10
    num_classes = 2
    # batch_size = 10
    learning_rate = 0.001

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    # optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

    # Train the model

    for epoch in range(num_epochs):
        #cross-validation
        temp = path.copy()
        index = epoch % len(path)
        test_file = path[index]
        temp.remove(test_file)
        model = model.train()
        for p in temp:
            dataset = SignalDataset(p)
            train_loader = DataLoader(dataset=dataset,
                            batch_size=1,
                            shuffle=True)
            total_step = train_loader.__len__()
            loss_list = []
            acc_list = []
            for i, (data, target) in enumerate(train_loader):

                x = data

                y = target.reshape(1).long()
                outputs = model(x)
                loss = criterion(outputs, y)
                loss_list.append(loss.item())
                # Backprop and perform Adam optimisation
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                # Track the accuracy
                total = y.size(0)
                _, predicted = torch.max(outputs.data, 1)
                # numero di cose corrette che ha predetto
                correct = (predicted == y).sum().item()
                acc_list.append(correct / total)

                if (i + 1) % 100 == 0:
                    print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Accuracy: {:.2f}%'
                        .format(epoch + 1, num_epochs, i + 1, total_step, loss.item(),
                                (correct / total) * 100))
        
        dataset = SignalDataset(test_file)
        train_loader = DataLoader(dataset=dataset,
                                batch_size=1,
                                shuffle=False)
        tot=0
        model = model.eval()
        for i, (data, target) in enumerate(train_loader):
            x = data
            result = model(x)
            _, predicted = torch.max(result, 1)
            # print("predicted: ",predicted.item()," actual:", target.item())
            if(predicted.item() == target.item()):
                tot = tot+1
        print("accuracy: ", tot, "/", train_loader.__len__())





    path = [#"C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_04\\",
            "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_16\\",
            # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_17\\",
        ]

    for p in path:
        dataset = SignalDataset(p)
        train_loader = DataLoader(dataset=dataset,
                                batch_size=1,
                                shuffle=False)

        tot=0
        for i, (data, target) in enumerate(train_loader):
            x = data
            result = model(x)
            _, predicted = torch.max(result, 1) #modifica -> deve essere 0 solo se p(0) > 60%
            print("predicted: ",predicted.item()," actual:", target.item())
            if(predicted.item() == target.item()):
                tot = tot+1
        # try:
        #     acc.append("accuracy: "+ str(tot)+ "/"+ str(train_loader.__len__()))
        print("accuracy: ", tot, "/", train_loader.__len__())

    # torch.save(model, 'traindedModel.pth')
    torch.save(model.state_dict(), 'trained_statedict.pth')