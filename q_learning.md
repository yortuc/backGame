## Q-learning

**Problem:** Making optimal sequental decisions.

- Agent oriented learning : learning by interacting with an environment to achieve a goal.
- Learning by trial and error with only delayed evaluative feedback (reward).

- Environment may be unknown, nonlinear,  stochastic and complex.
- Agent learns a policy to map states to actions. Seeking to maximize its cumulative reward in the long run.

**Challenges**
- Evaluative the feedback (reward)
- Need for trial and error, to explore as wall as to exploit.
- Non-stationrity.
- 

```
initialize Q[numstates,numactions] arbitrarily
observe initial state s
repeat
    select and carry out an action a
    observe reward r and new state s'
    Q[s,a] = Q[s,a] + α(r + γmaxa' Q[s',a'] - Q[s,a])
    s = s'
until terminated
```