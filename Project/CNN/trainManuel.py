import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from numpy import genfromtxt
import matplotlib as plt
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable

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
class SignalDataset(Dataset):
    """ Signal dataset."""
    # Initialize your data, download, etc.

    def __init__(self):
        signals = pd.read_csv("C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\chb01_03\\chn0.csv",
                              header=None, dtype=np.float64)
        self.len = signals.shape[0]
        self.x_data = torch.from_numpy(signals.values)
        results = pd.read_csv("C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\chb01_03\\target.csv",
                              header=None, dtype=np.float64)
        self.y_data = torch.from_numpy(results.values)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len


dataset = SignalDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=1,
                          shuffle=True)


class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv1d(5, 30, kernel_size=2, stride=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer2 = nn.Sequential(
            nn.Conv1d(30, 15, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        # self.layer3 = nn.Sequential(
        #     nn.Conv1d(32, 64, kernel_size=9, stride=1),
        #     nn.ReLU(),
        #     nn.MaxPool1d(kernel_size=2, stride=2)
        # )
        # self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(45, 10)
        self.fc2 = nn.Linear(10, 2)
        self.soft = nn.Softmax(1)
        # self.fc2 = nn.Linear(256, 2)

    def forward(self, x):
        out = self.layer1(x)
        # print(out)
        out = self.layer2(out)
        # print(out)
        # out = self.layer3(out)
        # out = out.reshape(out.size(0), -1)
        # out = self.drop_out(out)
        out = out.reshape(1, 45)
        out = self.fc1(out)
        # print(out)
        out = self.fc2(out)
        # print(out)
        out = self.soft(out)
        # out = self.fc2(out)
        # print(out.shape)
        return out


model = ConvNet()

num_epochs = 40

num_classes = 2
# batch_size = 5
learning_rate = 0.001

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
total_step = train_loader.__len__()
loss_list = []
acc_list = []
for epoch in range(num_epochs):
    for i, (data, target) in enumerate(train_loader):
        x = data.reshape((1,  5, 20)).float()
        # print(i)
        # Run the forward pass
        outputs = model(x)
        y = target.reshape(1).long()

        loss = criterion(outputs, y)
        loss_list.append(loss.item())

        # Backprop and perform Adam optimisation
        optimizer.zero_grad()
        # print(optimizer)
        loss.backward()
        # print(loss)
        optimizer.step()
       # print(optimizer)

        # Track the accuracy
        total = y.size(0)
        _, predicted = torch.max(outputs.data, 1)
        # numero di cose corrette che ha predetto
        # print(_)
        # print(predicted)
        correct = (predicted == y).sum().item()

        # print(f"output {outputs.data}")
        # print(f"predicted {predicted}")
        # print(f"correct {correct}")
        acc_list.append(correct / total)

        if (i + 1) % 100 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}, Accuracy: {:.2f}%'
                  .format(epoch + 1, num_epochs, i + 1, total_step, loss.item(),
                          (correct / total) * 100))


# print(x_signals[1])
# print(train_loader)

for i, (data, target) in enumerate(train_loader):

    x = data.reshape((1,  5, 20)).float()
    _, predicted = torch.max(model(x), 1)

    print(f"predicted: {predicted.item()} ==> actual {target.item()}")
