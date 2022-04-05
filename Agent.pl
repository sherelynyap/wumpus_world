
% set dynamic predicates - Informs the interpreter that the definition of the predicate(s) may change during execution
:- dynamic([
  world_size/1,	% Size of the world as [X, Y]
  position/2,		% position as (A, [X, Y]) implying location of A is [X, Y] 
  wumpus/1,		% Possible position of Wumpus to be inferred from smell
  noPit/1,		% noPit([X, Y]) means agent is sure there is no pit on [X, Y] cell, inferred from no breeze on adjacent cell(s)
  noWumpus/1,		% noWumpus([X, Y]) means agent is sure there is no Wumpus on [X, Y] cell, inferred from no smell on adjacent cell(s)
  maybeVisitLater/2,	% if no adjacent cell to go to, add the current cell as a probable point to visit later and backtrack
  goldPath/1		% agent stores each path from [1, 1] cell to the Gold retrieved
]).
hasarrow(agent, shotArrow).

% reborn/0 - implements Agent reset after meeting wumpus 
reborn:-
  /* make sure to clear any previous facts stored - retractall function in-built Prolog
  
  retractall(wumpus(_)),
  retractall(noCoins(_)),
  retractall(hasArrow(_)),
  retractall(portals(_,_)),
  */

  % initializations 
  init_relativeMap,
  init_agent,
  init_wumpus.

init_agent :-
  % position(Object, [X,Y]) => change object position in database 
  assert(position(Agent, [0,0])). 

init_relativeMap :-
  assert(world_size([7, 6]))


