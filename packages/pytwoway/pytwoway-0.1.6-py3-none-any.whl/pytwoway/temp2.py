'''
Test qpsolvers
'''

import numpy as np
from qpsolvers import solve_qp
from matplotlib import pyplot as plt
from blm import *
from matplotlib import pyplot as plt

##### Test QP solver and constraints #####
# an ols minimizes
#  ( Y - X' beta)' W ( Y - X' beta) 
# W is n *n 

# beta X W X' beta  + Y' W Y - 2* Y' W X' beta 
# quadprog takes 1/2 x'P x + q'x
#  P = X W X'
#  q = - Y' W X'

# -------  simulate an OLS -------
n = 100
k = 10
# parameters

x = np.random.normal(size=k)
# regressors
M = np.random.normal(size=(n, k))
# dependent
Y = M @ x 

# =-------- map to quadprog ---------
cons = QPConstrained(k, 1)
P = M.T @ M
q = - M.T @ Y

# y = (1 / 2) * x.T @ P @ x + q.T @ x

cons.solve(P=P, q=q)
x_sln1 = cons.res

# Add constraint x > -1
cons.add_constraint_builtin('biggerthan', {'gap_bigger': - 1})
cons.solve(P=P, q=q)
x_sln2 = cons.res

# Add constraint x < 1
cons.clear_constraints()
cons.add_constraint_builtin('lessthan', {'gap_smaller': 1})
cons.solve(P=P, q=q)
x_sln3 = cons.res

# Add constraint -1 < x < 1
cons.clear_constraints()
cons.add_constraint_builtin('biggerthan', {'gap_bigger': - 1})
cons.add_constraint_builtin('lessthan', {'gap_smaller': 1})
cons.solve(P=P, q=q)
x_sln4 = cons.res

##### Test qi matrix #####
# Set parameter values
nl = 3
nk = 4
mmult = 1
# Initiate BLMModel object
blm = BLMModel({'nl': nl, 'nk': nk, 'simulation': True, 'return_qi': True})
# Make variance of worker types small
blm.S1 /= 10
blm.S2 /= 10
jdata = blm._m2_mixt_simulate_movers(blm.NNm * mmult)
# Update BLM class attributes to equal model's
# Estimate qi matrix
qi_estimate = blm.fit_movers(jdata)
max_qi_col = np.argmax(qi_estimate, axis=1)
n_correct_qi = np.sum(max_qi_col == jdata['l'])
print(n_correct_qi / len(max_qi_col))

##### Test QPConstrained class #####
nl = 2
nk = 3
a = QPConstrained(nl, nk)
a.add_constraint_builtin('lin')
a.add_constraint_builtin('akmmono')
a.add_constraint_builtin('mono_k')
a.add_constraint_builtin('fixb')
a.add_constraint_builtin('biggerthan')
a.add_constraint_builtin('stationary')
a.add_constraint_builtin('none')
a.add_constraint_builtin('sum')

a.pad()
a.clear_constraints()

##### Test monotonic likelihoods #####
# Set parameter values
nl = 6
nk = 10
mmult = 100
smult = 100
# Initiate BLMModel object
blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# Make variance of worker types small
blm_true.S1 /= 4
blm_true.S2 /= 4
jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
sdata = blm_true._m2_mixt_simulate_stayers(blm_true.NNs * smult)
blm_fit = BLMModel({'nl': nl, 'nk': nk, 'maxiters': 30})
blm_fit.fit_movers(jdata)
blm_fit.fit_stayers(sdata)
liks1 = blm_fit.liks1[2:] - blm_fit.liks1[1: - 1] # Skip first
liks0 = blm_fit.liks0[2:] - blm_fit.liks0[1: - 1] # Skip first
print('Monotonic liks1:', liks1.min() > 0)
print('Monotonic liks0:', liks0.min() > 0)

##### Test BLMModel class #####
##### First test updating only A #####
# Set parameter values
nl = 6
nk = 10
mmult = 100
# Initiate BLMModel object
blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# Make variance of worker types small
blm_true.S1 /= 4
blm_true.S2 /= 4
jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
blm_fit = BLMModel({'nl': nl, 'nk': nk, 'maxiters': 200})
# blm_fit.A1 = blm_true.A1
# blm_fit.A2 = blm_true.A2
blm_fit.S1 = blm_true.S1
blm_fit.S2 = blm_true.S2
blm_fit.pk1 = blm_true.pk1
blm_fit.fit_A(jdata)

plt.plot(blm_true.A1.flatten(), blm_fit.A1.flatten(), '.', label='A1', color='red')
plt.plot(blm_true.A2.flatten(), blm_fit.A2.flatten(), '.', label='A2', color='green')
plt.legend()
plt.show()

##### Second test updating only S #####
# Set parameter values
nl = 6
nk = 10
mmult = 100
# Initiate BLMModel object
blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# Make variance of worker types small
# blm_true.S1 /= 4
# blm_true.S2 /= 4
jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
blm_fit = BLMModel({'nl': nl, 'nk': nk, 'maxiters': 20})
blm_fit.A1 = blm_true.A1
blm_fit.A2 = blm_true.A2
# blm_fit.S1 = blm_true.S1
# blm_fit.S2 = blm_true.S2
blm_fit.pk1 = blm_true.pk1
blm_fit.fit_S(jdata)

plt.plot(blm_true.S1.flatten(), blm_fit.S1.flatten(), '.', label='S1', color='red')
plt.plot(blm_true.S2.flatten(), blm_fit.S2.flatten(), '.', label='S2', color='green')
plt.legend()
plt.show()

##### Third test updating only pk1 #####
# Set parameter values
nl = 6
nk = 10
mmult = 100
# Initiate BLMModel object
blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# Make variance of worker types small
blm_true.S1 /= 10
blm_true.S2 /= 10
jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
blm_fit = BLMModel({'nl': nl, 'nk': nk, 'maxiters': 20})
blm_fit.A1 = blm_true.A1
blm_fit.A2 = blm_true.A2
blm_fit.S1 = blm_true.S1
blm_fit.S2 = blm_true.S2
# blm_fit.pk1 = blm_true.pk1
blm_fit.fit_pk(jdata)

plt.plot(blm_true.pk1.flatten(), blm_fit.pk1.flatten(), '.', label='pk1', color='red')
plt.legend()
plt.show()

##### Fourth test standard fit function #####
# Set parameter values
nl = 6
nk = 10
mmult = 100
# Initiate BLMModel object
blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# Make variance of worker types small
blm_true.S1 /= 4
blm_true.S2 /= 4
jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
blm_fit = BLMModel({'nl': nl, 'nk': nk, 'maxiters': 100})
blm_fit.fit_movers(jdata)

plt.plot(blm_true.S1.flatten(), blm_fit.S1.flatten(), '.', label='S1', color='red')
plt.plot(blm_true.S2.flatten(), blm_fit.S2.flatten(), '.', label='S2', color='green')
plt.legend()
plt.show()

plt.plot(blm_true.A1.flatten(), blm_fit.A1.flatten(), '.', label='A1', color='red')
plt.plot(blm_true.A2.flatten(), blm_fit.A2.flatten(), '.', label='A2', color='green')
plt.legend()
plt.show()

plt.plot(blm_true.pk1.flatten(), blm_fit.pk1.flatten(), '.', label='pk1', color='red')
plt.legend()
plt.show()

##### Fifth test full fit function #####
# Set parameter values
nl = 6
nk = 10
mmult = 100
# Initiate BLMModel object
blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# Make variance of worker types small
blm_true.S1 /= 4
blm_true.S2 /= 4
jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
blm_fit = BLMModel({'nl': nl, 'nk': nk, 'maxiters': 100})
blm_fit.fit_movers_cstr_uncstr(jdata)

plt.plot(blm_true.S1.flatten(), blm_fit.S1.flatten(), '.', label='S1', color='red')
plt.plot(blm_true.S2.flatten(), blm_fit.S2.flatten(), '.', label='S2', color='green')
plt.legend()
plt.show()

plt.plot(blm_true.A1.flatten(), blm_fit.A1.flatten(), '.', label='A1', color='red')
plt.plot(blm_true.A2.flatten(), blm_fit.A2.flatten(), '.', label='A2', color='green')
plt.legend()
plt.show()

plt.plot(blm_true.pk1.flatten(), blm_fit.pk1.flatten(), '.', label='pk1', color='red')
plt.legend()
plt.show()

# ##### New test #####
# # Set parameter values
# nl = 6
# nk = 10
# mmult = 100
# # Initiate BLMModel object
# blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# # Make variance of worker types small
# blm_true.S1 /= 4
# blm_true.S2 /= 4
# jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
# blm_fit = BLMModel({'nl': nl, 'nk': nk, 'maxiters': 100, 'simulation': False})

# blm_fit.params['update_a'] = False # First run fixm = True, which fixes A but updates S and pk
# blm_fit.params['update_s'] = True
# blm_fit.params['update_pk1'] = True
# print('Running fixm movers')
# blm_fit.fit_movers(jdata)
# ##### Loop 2 #####
# blm_fit.params['update_a'] = True # Now update A
# blm_fit.params['update_s'] = True
# blm_fit.params['update_pk1'] = True
# blm_fit.params['cons_a'] =  (['lin'], {'n_periods': 2}) # Set constraints (['biggerthan'], {'gap_bigger': 0})
# print('Running constrained movers')
# blm_fit.fit_movers(jdata)
# ##### Loop 3 #####
# blm_fit.params['cons_a'] = () # Remove constraints
# print('Running unconstrained movers')
# blm_fit.fit_movers(jdata)
# ##### Compute connectedness #####
# blm_fit.compute_connectedness_measure()

##### Test BLMModel class #####``
##### Test fit function #####
# Set parameter values
nl = 2
nk = 3
mmult = 100
smult = 100
# Initiate BLMModel object
blm_true = BLMModel({'nl': nl, 'nk': nk, 'simulation': True})
# Make variance of worker types small
blm_true.S1 /= 4
blm_true.S2 /= 4
jdata = blm_true._m2_mixt_simulate_movers(blm_true.NNm * mmult)
sdata = blm_true._m2_mixt_simulate_stayers(blm_true.NNs * smult)
blm_fit = BLMEstimator({'nk': nk, 'nl': nl, 'maxiters': 100})
blm_fit.fit(jdata, sdata, n_init=10, ncore=1)

blm_true.sort_matrices()
blm_fit.model.sort_matrices()

plt.plot(blm_true.S1.flatten(), blm_fit.model.S1.flatten(), '.', label='S1', color='red')
plt.plot(blm_true.S2.flatten(), blm_fit.model.S2.flatten(), '.', label='S2', color='green')
plt.legend()
plt.show()

plt.plot(blm_true.A1.flatten(), blm_fit.model.A1.flatten(), '.', label='A1', color='red')
plt.plot(blm_true.A2.flatten(), blm_fit.model.A2.flatten(), '.', label='A2', color='green')
plt.legend()
plt.show()

plt.plot(blm_true.pk1.flatten(), blm_fit.model.pk1.flatten(), '.', label='pk1', color='red')
plt.legend()
plt.show()

# ----- run on Italian data -----
import pandas as pd
import pytwoway as tw
it_jdata = pd.read_feather('/Volumes/GoogleDrive/.shortcut-targets-by-id/1iN9LApqNxHmVCOV4IUISMwPS7KeZcRhz/ra-adam/data/English/jdata.ftr')
# it_jdata = it_jdata.rename({'f1i': 'j1', 'f2i': 'j2'}, axis=1)
it_jdata = it_jdata.rename({'year_end_1': 'year_1', 'year_end_2': 'year_2'}, axis=1)
# it_jdata['wid'] = it_jdata['wid'] - 1

it_jdata = tw.BipartiteData(it_jdata, formatting='es', collapsed=False)
it_jdata.clean_data()
it_jdata.cluster()

nl = 6 # len(it_jdata['wid'].unique())
nk = 10 # len(set(list(it_jdata['j1'].unique()) + list(it_jdata['j2'].unique())))
blm_fit = BLMEstimator({'nk': nk, 'nl': nl, 'maxiters': 100})
blm_fit.fit(it_jdata.data, sdata=None, n_init=10, ncore=1)
