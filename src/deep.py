import torch
import torch.nn as nn

class FLFeatureNet(nn.Module):
	def __init__(self, spec_feats, complex_feats, full_feats=100):
		self.sf = spec_feats
		self.cf = complex_feats
		comb_f = spec_feats + complex_feats
		f = comb_f + 1
		spec_lin = nn.Linear(spec_feats, spec_feats)
		spec_complex_lin = nn.Linear(comb_f, comb_f)

		relu = nn.ReLU()
		bn1 = nn.BatchNorm1d(spec_feats)
		bn2 = nn.BatchNorm1d(comb_f)
		bn3 = nn.BatchNorm1d(full_feats)

		full_lin = nn.Linear(f, full_feats)
		final_lin = nn.Linear(full_feats, 1)

	def forward(self, x):
		s = x[0:self.sf]
		c = x[self.sf, self.cf]
		r = x[-1]

		result = relu(bn1(spec_lin(s)))
		result = torch.cat((result, c))
		result = relu(bn2(spec_complex_lin(result)))
		result = torch.cat((result, r))
		result = relu(bn3(full_lin(result)))
		result = final_lin(result)

		return result