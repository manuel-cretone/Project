import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from numpy import genfromtxt
import matplotlib as plt
from torch.utils.data import Dataset, DataLoader, random_split
from torch.autograd import Variable
import os

# train_signals = pd.read_csv("chn0.csv")
# train_target = pd.read_csv("target.csv")
# x_train = train_signals.values
# y_train = train_target.values
# print(x_train.dtype)

# prova = pd.read_csv("prova.csv", dtype=float)

# prova2 = prova.values
# prova_tensor = torch.tensor(prova2).float()


# x_signals = torch.tensor(x_train).float()
# y_target = torch.tensor(y_train).float()

path = ["C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_03\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_04\\", #
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_15\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_16\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_18\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_21\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_26\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_01\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_02\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_34\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_35\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb03_36\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_06\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_13\\",
        # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_16\\",
            # "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_17\\",
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



class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv1d(23, 10, kernel_size=5, stride=1, padding=4),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3, stride=3)
        )

        self.layer2 = nn.Sequential(
            nn.Conv1d(10, 5, kernel_size=3, stride=1, padding= 2),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer3 = nn.Sequential(
            nn.Conv1d(10, 30, kernel_size=2, stride=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )
        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(90, 15)
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


model = ConvNet()

num_epochs = 15
num_classes = 2
# batch_size = 10
learning_rate = 0.001

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
# optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

# Train the model

for epoch in range(num_epochs):
    for p in path:
        dataset = SignalDataset(p)
        # print(dataset.__len__())
        # sp = random_split(dataset, (200,4))
        train_loader = DataLoader(dataset=dataset,
                          batch_size=1,
                          shuffle=True)
        total_step = train_loader.__len__()
        loss_list = []
        acc_list = []
        for i, (data, target) in enumerate(train_loader):
            
            # data, target = data.cuda(), target.cuda()
            # data, target = Variable(data), Variable(target)
            
            # Run the forward pass
            # x = data.reshape(( 1,  5, 20)).float()

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
            # print(outputs, loss, predicted)
            # numero di cose corrette che ha predetto
            correct = (predicted == y).sum().item()
            # print(f"correct {correct}")
            # print(f"output {outputs.data}")
            # print(f"predicted {predicted}")
            acc_list.append(correct / total)

            if (i + 1) % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Accuracy: {:.2f}%'
                    .format(epoch + 1, num_epochs, i + 1, total_step, loss.item(),
                            (correct / total) * 100))






path = ["C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_04\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb01_18\\",
        "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\csv_files\\chb05_17\\",
    ]
acc = []
for p in path:
    dataset = SignalDataset(p)
    train_loader = DataLoader(dataset=dataset,
                            batch_size=1,
                            shuffle=False)

    tot=0
    for i, (data, target) in enumerate(train_loader):
        # x = data.reshape((1,  5, 20)).float()
        x = data
        result = model(x)
        _, predicted = torch.max(result, 1)
        # print(model(x))
        print("predicted: ",predicted.item()," actual:", target.item())
        if(predicted.item() == target.item()):
            tot = tot+1
    # try:
    #     acc.append("accuracy: "+ str(tot)+ "/"+ str(train_loader.__len__()))
    print("accuracy: ", tot, "/", train_loader.__len__())
print(acc)