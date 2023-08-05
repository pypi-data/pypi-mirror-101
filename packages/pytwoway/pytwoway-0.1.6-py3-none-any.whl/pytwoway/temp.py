import pytwoway as tw
import networkx as nx
import copy

data = tw.SimTwoWay({'p_move': 0.005}).sim_network()
data2 = copy.deepcopy(data)

# Run HE on non-biconnected set
tw_net = tw.TwoWay(data)
tw_net.fit_fe({'h2': True, 'out': 'fe_biconnected_false'})

# Run HE on biconnected set
tw_net = tw.TwoWay(data2)
tw_net.b_net.clean_data()
G = tw_net.b_net.bd.conset()
Gc = max(nx.biconnected_components(G), key=len)
tw_net.b_net.bd.data = tw_net.b_net.bd.data[tw_net.b_net.bd.data['fid'].isin(Gc)].reset_index(drop=True)

# Data cleaning
tw_net.b_net.bd.data = tw_net.b_net.bd.data.dropna()
tw_net.b_net.bd.conset()
tw_net.b_net.bd.contiguous_ids('fid')
tw_net.b_net.bd.contiguous_ids('wid')
tw_net.b_net.long_to_es()

# Fit HE
fe_params = tw.update_dict(tw_net.default_fe, {'h2': True, 'out': 'fe_biconnected_true'})
fe_params['data'] = tw_net.b_net.get_cs()
fe_solver = tw.FEEstimator(fe_params)
fe_solver.fit_1()
fe_solver.construct_Q()
fe_solver.fit_2()
