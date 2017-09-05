// Agent.h

#ifndef AGENT_H
#define AGENT_H

#include <stdio.h>
#include <stdlib.h>
#include <queue>
#include <list>
#include "Action.h"
#include "Percept.h"
#include "Orientation.h"
#include "Location.h"

#define WORLD_SIZE 4

enum StatusType { YES, NO, UNCERTAIN };

typedef struct LocationStatus
{
	bool Visited;
	StatusType Wumpus;
	StatusType Pit;

    LocationStatus()
	{
		Visited = false;
		Wumpus = UNCERTAIN;
		Pit = UNCERTAIN;
	}
	
}LocationStatus;


class Agent
{
public:
	Agent ();
	~Agent ();
	void Initialize ();
	Action Process (Percept& percept);
	void GameOver (int score);

private:
    Location cLoc;// current location
	Location WLocatioin;
	//RIGHT 0, UP 1, LEFT 2, DOWN 3
	Orientation orientation;// current orientation
	bool HasGold;
	bool HasArrow;
	bool move[4];//forward, left, backword, right
	bool move_dir[4];//right, up, left, down
	LocationStatus worldStatus[WORLD_SIZE][WORLD_SIZE];
	void goBack();
	void updateLocationStatus(Percept& percept);
	void check_move(Percept percept);
	queue<Action> actionqueue;
	list<Action> actionlist;
	bool gotolast;//whether in the process of go to parent node
};

#endif // AGENT_H
