import torch.optim as optim
import torch.nn.functional as F
import torch
from torch.utils.data import Dataset

"""
TODO:
define train loader so that data can be loaded in a
pytorch compatible format
"""


def train_fl(model, epochs, train_loader):
	optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

	for e in range(epochs):
		for t, (x, y) in enumerate(train_loader):
			model.train()

			scores = model.forward(x)
			loss = F.cross_entropy(scores, y)

			# zeroing gradients and then
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()

			if t % 100 == 0 and e % 10 == 0:
				print('Iteration %d, loss = %.4f' % (t, loss.item()))


class CoverageDataset(Dataset):
	def __init__(self, data):
		super()

	def __len__(self):
		return 0
