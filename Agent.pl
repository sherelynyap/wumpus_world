hasarrow(agent, shotArrow).

%% reborn/0 - implements Agent reset after meeting wumpus
reborn:-
  % make sure to clear any previous facts stored
  /*
  retractall(wumpus(_)),
  retractall(noPit(_)),
  retractall(noWumpus(_)),
  retractall(maybeVisitLater(_,_)),
  retractall(goldPath(_)),
  */

  % initializations
  init_board,
  init_agent,
  init_wumpus.

init_agent :-
    assert(position(Agent, [0,0])). /* position(Object, [X,Y]) => record object position in database */

init_board :-

