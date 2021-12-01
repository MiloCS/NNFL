import torch
import torch.nn as nn

class SimpleFLNet(nn.Module):
	def __init__(self, input_size, hidden_size):
		super(SimpleFLNet, self).__init__()
		self.fc1 = nn.Linear(input_size, hidden_size)
		self.fc2 = nn.Linear(hidden_size, 1)

		self.sig = nn.Sigmoid()

	def forward(self, x):
		hidden = self.sig(self.fc1(x))
		final = self.fc2(hidden)
		final = self.sig(final)
		return final


class SimpleFLReluNet(nn.Module):
	def __init__(self, input_size, hidden_size):
		super()
		self.fc1 = nn.Linear(input_size, hidden_size)
		self.fc2 = nn.Linear(hidden_size, 1)

		self.relu = nn.ReLU()
		self.sig = nn.Sigmoid()

	def forward(self, x):
		hidden = self.relu(self.fc1(x))
		final = self.fc2(hidden)
		final = self.sig(final)
		return final


"""
the paper I looked at had a variable number of hidden layers
depending on how complex the project they were attempting to FL in
was, therefore there is a list of hidden sizes here.
"""
class DeepFLNet(nn.Module):
	def __init__(self, input_size, hidden_sizes):
		super()
		self.relu = nn.ReLU()
		self.bns = []
		self.fcs = []

		hidden_sizes.append(1)
		fcs.append(nn.Linear(input_size, hidden_sizes[0]))
		bns.append(nn.BatchNorm1d(hidden_sizes[0]))

		for i in range(len(hidden_sizes) - 1):
			fcs.append(nn.Linear(hidden_sizes[i], hidden_sizes[i+1]))
			if i != len(hidden_sizes) - 1:
				bns.append(nn.BatchNorm1d(hidden_sizes[i+1]))

		self.num_layers = len(fcs)

	def forward(self, x):
		hidden_val = x
		for i in range(self.num_layers):
			fc = self.fcs[i]
			hidden_val = fc(hidden_val)
			if i != self.num_layers:
				bn = self.bns[i]
				hidden_val = self.relu(bn(hidden_val))
		return hidden_val