import torch
import torch.nn as nn

class FLFeatureNet(nn.Module):
	def __init__(spec_feats, complex_feats):
		comb_f = spec_feats + complex_feats
		f = comb_f + 1
		spec_lin = nn.Linear(spec_feats, spec_feats)
		spec_complex_lin = nn.Linear(comb_f)

		relu = nn.ReLU()
		bn1 = nn.BatchNorm1d(spec_feats)
		bn2 = nn.BatchNorm1d(comb_f)
		bn3 = nn.BatchNorm1d(f)

		full_lin = nn.Linear(f, 100)
		final_lin = nn.Linear(100, 1)

	def forward()