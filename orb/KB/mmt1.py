import numpy as np
import pandas as pd
from pprint import pprint




states = ['howling','waving','jumping']

#probability values of event
pi_1 = [45,35,20]
state_space =pd.Series(pi_1, index=states, name ='States')
print(state_space)
print(state_space.sum())


#state transition matrix
q_df = pd.DataFrame(columns=states, index=states)
q_df.loc[states[0]]=[60 ,25 ,15]
q_df.loc[states[1]]=[40 ,30 ,30]
q_df.loc[states[2]]=[35 ,40 ,25]
#print the matrix
print(q_df)

#print contents
q=q_df.values
print('\n',q, q.shape, '\n')
print(q_df.sum(axis=1))

#print state translations

def _get_markov_edges(Q):
    edges = {}
    for col in Q.columns:
        for idx in Q.index:
            edges[(idx,col)] =Q.loc[idx,col]
    return edges

edges_t = _get_markov_edges(q_df)
print(edges_t)

# hidden states of angry and happy

hidden_states = ['Angry','Happy']
pi = [50,50]
state_space = pd.Series(pi, index=hidden_states, name='states')
print(state_space)
print('\n', state_space.sum())

mood = pd.DataFrame(columns=hidden_states, index=hidden_states)
mood.loc[hidden_states[0]]=[30 ,70]
mood.loc[hidden_states[1]]=[20 ,80]

#print the matrix
print(mood)

#print contents
a=mood.values
print('\n',a, a.shape, '\n')
print(mood.sum(axis=1))

#current mood
observable_states = states
new_mood = pd.DataFrame(columns=observable_states, index=hidden_states)
new_mood.loc[hidden_states[0]]=[30 ,20, 50]
new_mood.loc[hidden_states[1]]=[20 ,70, 10]

#print the matrix
print(new_mood)

#print contents
b=new_mood.values
print('\n',b, b.shape, '\n')
print(new_mood.sum(axis=1))

hidden_edges_wts = _get_markov_edges(mood)
pprint(hidden_edges_wts)
emission_edges_wts = _get_markov_edges(new_mood)
pprint(emission_edges_wts)

obs_map = {'howling':0, 'waving':1, 'jumping':2}
obs = np.array([1,1,2,1,0,1,2,1,0,2,2,0,1,0,1])
inv_obs_map = dict((v,k) for k, v in obs_map.items())
obs_seq = [inv_obs_map[v] for v in list(obs)]
print( pd.DataFrame(
np.column_stack([obs, obs_seq]),
columns=['Obs_code', 'Obs_seq']))

def viterbi(pi, mood, new_mood, obs):
    nStates = np.shape(b)[0]
    T = np.shape(obs)[0]
    # make an array of zeros of size 1 x T
    path = np.zeros(T)
    # make a matrix of zeros of size nStates x T delta(i.e. setting a blank table as in Slide 39)
    delta = np.zeros((nStates, T))
    # phi --> argmax by time step for each state
    phi = np.zeros((nStates, T))
    # initialzise delta and phi
    # Initial values multiplied by the emission probs for first observation(e.g. slide 37)
    delta[:, 0] = pi * b[:, obs[0]]
    phi[:, 0] = 0
    # the forward algorithm extension
    for t in range(1, T):
        #T is the number of times steps in the sequence i.e. 15
        for s in range(nStates):
        #nStates is the number of hidden states i.e. 2 (Angry, Happy)
        #now you need to populate the table in this loop, but firstsee Slide 38
        # you need to take the maximum (using np.max) between the product of the deltas in the
        #previous time step with the hidden state transitions for state s then multiply by the
        #emission probabilities for state s, look through what is happening in slide 38 first.
        delta[s, t] = np.max(XXXXXXX)*(XXXXXXX)
        phi[s, t] = np.argmax(XXXXXXX)
        # <this is the same as the first term above
        print('s={s} and t={t}: phi[{s}, {t}] = {phi}'.format(s=s, t=t, phi=phi[s, t]))
    # find optimal path
    print('-'*50)
    print('Start Backtrace\n')path[T-1] = np.argmax(delta[:, T-1])
    for t in range(T-2, -1, -1):
        path[t] = phi[int(path[t+1]), [t+1]]
    #p(' '*4 + 't={t}, path[{t}+1]={path}, [{t}+1]={i}'.format(t=t, path=path[t+1], i=[t+1]))
    print('path[{}] = {}'.format(t, path[t]))
    return path, delta, ph