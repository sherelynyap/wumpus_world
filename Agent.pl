:- dynamic([
    reborn/0, % indicate game start - on Driver's end "assert(reborn)"
  hasArrow/0, % indicate presence of arrow
  coinsObtained/1, % indicates number of coins obtained
  wall/2,
  wumpus/2,
  confundus/2,
  current/3, % current stores current position of agent(that is constantly changing) - SINGLETON (only can have 1)
  visited/2, % visited can be reset start/end/portal of game
  tingle/2,
  glitter/2,
  stench/2,
  wumpusAlive/0,
  cell/2
]).

% Removes all objects and knowledge from world
clearWorld :-
    %objects
    retractall(coinsObtained(_)),
    retractall(hasArrow(_,_)),
    %knowledge
    retractall(current(_,_,_)),
    retractall(wumpus(_,_)),
    retractall(confundus(_,_)),
    retractall(visited(_,_)),
    retractall(tingle(_,_)),
    retractall(glitter(_,_)),
    retractall(wall(_,_)),
    retractall(stench(_,_)),
    retractall(cell(_,_)).

% Removes all knowledge when enter portal
clearKnowledge :-
    retractall(wall(_,_)),
    retractall(current(_,_,_)),
    retractall(wumpus(_,_)),
    retractall(confundus(_,_)),
    retractall(visited(_,_)),
    retractall(tingle(_,_)),
    retractall(glitter(_,_)),
    retractall(stench(_,_)),
    retractall(cell(_,_)).

initializeWorld :-
    setCurrent(0,0,"rnorth"),
    assert(safe(0,0)),
    assert(visited(0,0)),
    % set cells surrounding agent
    setCell(-1,-1),setCell(0,-1),setCell(1,-1),
    setCell(-1,0),setCell(0,0),setCell(1,0),
    setCell(-1,1),setCell(0,1),setCell(1,1).

% implements agent reset due to arriving into a cell inhabited by WUmpus
reborn:-
    current(Xw,Yw,_),
    wumpus(Xw,Yw),
    clearWorld,
    initializeWorld,
    assert(hasArrow),
    assert(coinsObtained(0)),
    assert(wumpusAlive).

% implements agent reset due to game start or arrival to a cell with Confundus Portal
reposition(L):-
    reborn,updateSensors(L); % initialization within reborn
    (current(Xp,Yp,_), confundus(Xp,Yp), clearKnowledge, initializeWorld,updateSensors(L)).

% current(X,Y,D) is set by this
setCurrent(X,Y,D) :-
    retractall(current(_,_,_)),
    asserta(current(X,Y,D)).
% to find unvisited cell = \+visited(X,Y), cell(X,Y)
setCell(X,Y):- \+cell(X,Y) -> assert(cell(X,Y)).

% GUESS
safe(X, Y):- \+wumpus(X,Y);\+confundus(X,Y),cell(X,Y),\+wall(X,Y).

% GUESS alt- getAdjacentCells for stench, mark unvisited cells as wumpus(x,y)
wumpus(X,Y) :- stench(X+1,Y),stench(X,Y+1), stench(X,Y-1), stench(X-1,Y).

% GUESS alt- getAdjacentCells for tingle, mark unvisited cells as confundus(x,y)
confundus(X, Y) :- tingle(X+1,Y),tingle(X,Y+1), tingle(X,Y-1), tingle(X-1,Y).

%updateSensors percept = [Confounded, stench, tingle, glitter, bump, scream]
updateSensors(L) :-
    (L = ['on',_,_,_,_,_] -> reposition(L) ); % confounded - trigger reposition
    (current(X,Y,_),L = [_,'on',_,_,_,_] -> stench(X,Y) );
    (current(X,Y,_),L = [_,_,'on',_,_,_] -> tingle(X,Y) );
    (current(X,Y,_),L = [_,_,_,'on',_,_] -> glitter(X,Y) ).

% Transitory-detected based on movements(shoot,moveforward) in direction of wall)
perceiveBump(move("moveforward",L)) :- (L = [_,_,_,_,'on',_] ->
  (current(X,Y,"rnorth") -> wall(X,Y-1) );
  (current(X,Y,"reast") -> wall(X+1,Y) );
  (current(X,Y,"rsouth") -> wall(X,Y+1) );
  (current(X,Y,"rwest") -> wall(X-1,Y) ) ).

perceiveScream(move("shoot",L)) :- (L = [_,_,_,_,_,'on'] -> retractall(wumpusAlive)).

% return List L [shouldn’t be too long] of action sequence to (priority):
%Pick up Coin
%Shoot Wumpus
%Move to Safe, unvisited cell

move(A,L) :-
    (A = "turnleft" -> current(X,Y,D), turnLeft(X,Y,D), updateSensors(L));
    (A = "turnright" -> current(X,Y,D), turnRight(X,Y,D), updateSensors(L));
    (A = "moveforward" -> current(X,Y,D),getForwardCell((X,Y),D,(X1,Y1)), setCurrent(X1,Y1,D) assert(visited(X1,Y1)), updateSensors(L));
    (A = "shoot", retractall(hasArrow), updateSensors(L));
    (A = "pickup", pickup_gold, updateSensors(L)).

explore(L):-
    heuristic(H),
    append([], H, L).

% List L of sensory indicators , H for recommended action
heuristic(H) :-
    (current(X,Y,_),glitter(X,Y) -> H is ["pickup"]); % pickup
    (current(X,Y,D),wumpus(X,Yw);wumpus(Xw,Y),isFacing((X,Y),D,(Xw,Yw))-> H is ["shoot"]); % in same column/row as wumpus shoot
    % moveforward if agent is facing safe,unvisited cell
    (current(X,Y,D),getForwardCell((X,Y),D,(X1,Y1)),safe(X1,Y1),\+visited(X1,Y1) -> H is ["moveforward"]);
    (current(X,Y,D),getRightCell((X,Y),D,(X1,Y1)),safe(X1,Y1),\+visited(X1,Y1) -> H is ["turnright"]);
    (current(X,Y,D),getLeftCell((X,Y),D,(X1,Y1)),safe(X1,Y1),\+visited(X1,Y1) -> H is ["turnleft"]).

% DEFINING AGENT’S ACTIONS
turnLeft(X,Y,D):-
    (D="rnorth" -> D1="rwest",setCurrent(X,Y,D1));
    (D="rwest" -> D1="rsouth",setCurrent(X,Y,D1));
    (D="rsouth" -> D1="reast",setCurrent(X,Y,D1));
    (D="reast" -> D1="rnorth",setCurrent(X,Y,D1)).

turnRight(X,Y,D):-
    (D="rnorth" -> D1="reast",setCurrent(X,Y,D1));
    (D="reast" -> D1="rsouth",setCurrent(X,Y,D1));
    (D="rsouth" -> D1="rwest",setCurrent(X,Y,D1));
    (D="rwest" -> D1="rnorth",setCurrent(X,Y,D1)).

moveForward(X,Y,D):-
    (D="rnorth" -> Y1 is (Y-1), X1 is X,setCurrent(X1,Y1,D));
    (D="reast" -> Y1 is Y, X1 is (X+1),setCurrent(X1,Y1,D));
    (D="rsouth" -> Y1 is (Y+1), X1 is X,setCurrent(X1,Y1,D));
    (D="rwest" -> Y1 is Y, X1 is (X-1),setCurrent(X1,Y1,D)).

pickup_gold :-
  current(X,Y,_),
  glitter(X,Y), !,  % checks whether there is gold in this square
  coinsObtained(NGold),
  NGold1 is NGold + 1, % these 2 sentences increment the number of gold coins
  retract(coinsObtained(NGold)),  % remove the old value in the coinsobtained
  assert(coinsObtained(NGold1)), % add it again with the new value of the coins
  format("You have ~d gold coins!~n",NGold1),
  retract(glitter(X,Y)).

getForwardCell((X0,Y0),D0,(XN,YN)) :-
    (D0 = "rnorth", XN is X0, YN is Y0-1);
    (D0 = "reast", XN is X0+1, YN is Y0);
    (D0 = "rsouth", XN is X0, YN is Y0+1);
    (D0 = "rwest", XN is X0-1, YN is Y0).

getLeftCell((X0,Y0),D0,(XN,YN)) :-
    (D0 = "rnorth", XN is X0-1, YN is Y0);
    (D0 = "reast", XN is X0, YN is Y0-1);
    (D0 = "rsouth", XN is X0+1, YN is Y0);
    (D0 = "rwest", XN is X0, YN is Y0+1).

getRightCell((X0,Y0),D0,(XN,YN)) :-
    (D0 = "rnorth", XN is X0+1, YN is Y0);
    (D0 = "reast", XN is X0, YN is Y0+1);
    (D0 = "rsouth", XN is X0-1, YN is Y0);
    (D0 = "rwest", XN is X0, YN is Y0-1).

getBehindCell((X0,Y0),D0,(XN,YN)) :-
    (D0 = "rnorth", XN is X0, YN is Y0+1);
    (D0 = "reast", XN is X0-1, YN is Y0);
    (D0 = "rsouth", XN is X0, YN is Y0-1);
    (D0 = "rwest", XN is X0+1, YN is Y0).

isAdjacent((X,Y),(XT,YT)) :-
    (X =:= XT, Y =:= YT+1);
    (X =:= XT, Y =:= YT-1);
    (X =:= XT+1, Y =:= YT);
    (X =:= XT-1, Y =:= YT).

isFacing((X,Y),D,(XT,YT)) :-
    (D = "rnorth", X =:= XT, YT < Y);
    (D = "rsouth", X =:= XT, YT > Y);
    (D = "reast", Y =:= YT, XT > X);
    (D = "rwest", Y =:= YT, XT < X).


% - getting the list of adjacent rooms
getAdjacentCells(X,Y,L) :-
    XL is X-1,
    XR is X+1,
    YD is Y-1,
    YU is Y+1,
    append([(XL,Y), (XR,Y), (X,YU), (X,YD)],[],L).


