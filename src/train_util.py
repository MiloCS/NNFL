import torch.optim as optim
import torch.nn.functional as F


"""
TODO:
define train loader so that data can be loaded in a
pytorch compatible format
"""

train_loader = None

def train_fl(model, epochs):
	optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

	for e in range(epochs):
	    for t, (x, y) in enumerate(train_loader):
	        model.train()
	        
	        scores = model(x)
	        loss = F.cross_entropy(scores, y)

	        #zeroing gradients and then
	        optimizer.zero_grad()
	        loss.backward()
	        optimizer.step()

	        if t % print_every == 0:
	            print('Iteration %d, loss = %.4f' % (t, loss.item()))