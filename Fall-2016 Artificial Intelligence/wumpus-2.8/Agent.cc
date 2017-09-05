// Agent.cc
#include <iostream>
#include "Agent.h"

using namespace std;

Agent::Agent ()
{

}

Agent::~Agent ()
{

}

void Agent::Initialize ()
{
	HasGold = false;
	HasArrow = true;
	orientation = RIGHT;
	cLoc.X = 0;
	cLoc.Y = 0;
	WLocatioin.X = 0;
	WLocatioin.Y = 0;
}

void Agent::updateLocationStatus(Percept& percept)
{
	worldStatus[cLoc.X][cLoc.Y].Visited = true;
	if(percept.Scream == true)
	{
		for(int i = 0;i < WORLD_SIZE; i++)
		{
			for(int j = 0;j < WORLD_SIZE; j++)
			{
				worldStatus[i][j].Wumpus = NO;
			}
		}
	}
	if(WLocatioin.X==0 && WLocatioin.Y==0)
	{
		if(percept.Stench == false)
		{
			if(cLoc.Y>0)worldStatus[cLoc.X][cLoc.Y-1].Wumpus = NO;
			if(cLoc.X>0)worldStatus[cLoc.X-1][cLoc.Y].Wumpus = NO;
			if(cLoc.Y<3)worldStatus[cLoc.X][cLoc.Y+1].Wumpus = NO;
			if(cLoc.X<3)worldStatus[cLoc.X+1][cLoc.Y].Wumpus = NO;
		}
		else 
		{
			for(int i = 0; i < WORLD_SIZE; i++)
			{
				for(int j = 0; j < WORLD_SIZE; j++)
				{
					if(worldStatus[i][j].Wumpus == UNCERTAIN)
					{
						if(abs(i-cLoc.X)+abs(j-cLoc.Y)!=1)//adjacent
						{
							worldStatus[i][j].Wumpus = NO;
						}
					}
				}
			}
		}
		int uncertaincount = 0;
		for(int i = 0; i < WORLD_SIZE; i++)
		{
			for(int j = 0; j < WORLD_SIZE; j++)
			{
				if(worldStatus[i][j].Wumpus == UNCERTAIN)
				{
					uncertaincount++;
					WLocatioin.X = i;
			        WLocatioin.Y = j;
				}					
			}
		}
		if(1 == uncertaincount)
		{
			worldStatus[WLocatioin.X][WLocatioin.Y].Wumpus = YES;
		}
		else
		{
			WLocatioin.X = 0;
			WLocatioin.Y = 0;
		}
	}
	if(percept.Breeze == false)
	{
		if(cLoc.Y>0)worldStatus[cLoc.X][cLoc.Y-1].Pit = NO;
		if(cLoc.X>0)worldStatus[cLoc.X-1][cLoc.Y].Pit = NO;
		if(cLoc.Y<3)worldStatus[cLoc.X][cLoc.Y+1].Pit = NO;
		if(cLoc.X<3)worldStatus[cLoc.X+1][cLoc.Y].Pit = NO;
	}
}

Action Agent::Process (Percept& percept)
{
	//char c;
	Action action;
	
	updateLocationStatus(percept);
	//cin >> c;
    //cout << "actionqueue.size = " << actionqueue.size() << endl;
	//cout << "actionqueue.empty = " << actionqueue.empty() << endl;
	if(actionqueue.empty() == false)
	{
		//cout << "if 1" << endl;
		action = actionqueue.front();
		actionqueue.pop();
		//cout << "actionqueue.size = " << actionqueue.size() << endl;
	    //cout << "actionqueue.empty = " << actionqueue.empty() << endl;
	}
	
	else if(percept.Stench == true && (WLocatioin.X != 0 || WLocatioin.Y !=0) && HasArrow == true)//find wumpus
	{
		gotolast = true;
		//cout << "if 2" << endl;
		cout << "I find wumpus location, I can shoot it!" << endl;
		cout << "HasArrow = " << HasArrow << endl;
		//RIGHT 0, UP 1, LEFT 2, DOWN 3
		Orientation wumpusOri;
		if(WLocatioin.X - cLoc.X == 1)wumpusOri = UP;
		if(WLocatioin.X - cLoc.X == -1)wumpusOri = DOWN;
		if(WLocatioin.Y - cLoc.Y == 1)wumpusOri = RIGHT;
		if(WLocatioin.Y - cLoc.Y == -1)wumpusOri = LEFT;
		
		//cout << "wumpusOri = " << wumpusOri << endl;
		//cout << "orientation = " << orientation << endl;
		
		if((wumpusOri-orientation+4)%4==2)
		{
			actionqueue.push(TURNLEFT);
			actionqueue.push(TURNLEFT);
			actionqueue.push(SHOOT);
			actionqueue.push(TURNLEFT);
			actionqueue.push(TURNLEFT);
		}
		else if(wumpusOri == orientation)
		{
			actionqueue.push(SHOOT);
		}
		else if((wumpusOri-orientation+4)%4==1)
		{
			actionqueue.push(TURNLEFT);
			actionqueue.push(SHOOT);
			actionqueue.push(TURNRIGHT);
		}
		else if((wumpusOri-orientation+4)%4==3)
		{
			actionqueue.push(TURNRIGHT);
			actionqueue.push(SHOOT);
			actionqueue.push(TURNLEFT);
		}
		action = actionqueue.front();
		actionqueue.pop();
		//cout << "actionqueue.size = " << actionqueue.size() << endl;
	}

	
	else if(percept.Glitter == true)
	{
		//cout << "if 3" << endl;
		cout<<"I find the gold, I will grab it and then go back!"<<endl;
		gotolast = false;
        action = GRAB;
		HasGold = true;
		for(int i=0;i<WORLD_SIZE;i++)
		{
			for(int j=0;j<WORLD_SIZE;j++)
			{
				worldStatus[i][j].Visited = false;
			}
		}
		goBack();
    }
	
	else
	{
		//cout << "if 3" << endl;
		gotolast = false;
		//cout << "before check move in else" << endl;
		check_move(percept);
		if(move[0] == true)
		{
			action = GOFORWARD;
		}
		else if(move[1] == true)
		{
			action = TURNLEFT;
			actionqueue.push(GOFORWARD);
		}
		else if(move[3] == true)
		{
			action = TURNRIGHT;
			actionqueue.push(GOFORWARD);
		}
		else if(cLoc.X==0 && cLoc.Y==0)
		{			
			action = CLIMB;
			cout << "I have determinded, I cannot safely snatch the gold!" << endl;
		}
		else
		{
			//go to last location
			gotolast = true;
			actionqueue.push(TURNLEFT);
			actionqueue.push(TURNLEFT);
			int n = actionlist.size();
			//cout << "actionlist.size = " << n << endl;
			Action lastaction;
			while(n>0)
			{
				lastaction = actionlist.back();
				if(lastaction == TURNLEFT)
				{
					cout << "lastaction == TURNLEFT" << endl;
					actionqueue.push(TURNRIGHT);
				}
				else if(lastaction == TURNRIGHT)
				{
					cout << "lastaction == TURNRIGHT" << endl;
					actionqueue.push(TURNLEFT);
				}
				else if(lastaction == GOFORWARD)
				{
					cout << "lastaction == GOFORWARD" << endl;
					actionqueue.push(GOFORWARD);
					actionlist.pop_back();
					lastaction = actionlist.back();
					if(lastaction==GOFORWARD)
					{
						cout << "lastaction == GOFORWARD 2 " << endl;
						actionqueue.push(TURNLEFT);
			            actionqueue.push(TURNLEFT);
					}
					else
					{						
						while(lastaction!=GOFORWARD)
						{
							if(lastaction == TURNRIGHT)
							{
								cout << "lastaction == TURNRIGHT 2 " << endl;
								actionqueue.push(TURNRIGHT);
							}
						    else if(lastaction == TURNLEFT)
							{
								cout << "lastaction == TURNLEFT 2 " << endl;
								actionqueue.push(TURNLEFT);
							}							
						    actionlist.pop_back();
                           lastaction = actionlist.back();							
						}
					}					
					break;
				}				
				actionlist.pop_back();
				n = actionlist.size()-1;
			}			
			action = actionqueue.front();
		    actionqueue.pop();			
		}
	}

//	cout << "actionqueue.size = " << actionqueue.size() << endl;
//	cout << "actionqueue.empty = " << actionqueue.empty() << endl;
	if(gotolast == false) actionlist.push_back(action);
	if(action == GOFORWARD) 
	{
		//locationlist.push_back(cLoc);
		if(orientation == RIGHT)
		{
			cLoc.Y++;
		}
		else if(orientation == LEFT)
		{
			cLoc.Y--;
		}
		else if(orientation == UP)
		{
			cLoc.X++;
		}
		else if(orientation == DOWN)
		{
			cLoc.X--;
		}
	}

	else if(action == TURNLEFT)
	{
		orientation = (Orientation)((orientation + 1)%4);
	}

	else if(action == TURNRIGHT)
	{
		orientation = (Orientation)((orientation + 3)%4);
	}

	else if(action == SHOOT)
	{
		cout << "SHOOTING!" << endl;
		//cout << "actionqueue.size = " << actionqueue.size() << endl;
	    //cout << "actionqueue.empty = " << actionqueue.empty() << endl;
		HasArrow = false;
        worldStatus[WLocatioin.X][WLocatioin.Y].Wumpus = NO;
	}
	
	//	cout << "WLocatioin.X = " << WLocatioin.X << endl;
    //  cout << "WLocatioin.Y = " << WLocatioin.Y << endl;
	//	cout << "cLoc.X = " << cLoc.X << endl;
	//  cout << "cLoc.Y = " << cLoc.Y << endl;
	//cout << "actionqueue.size = " << actionqueue.size() << endl;
	//cout << "actionqueue.empty = " << actionqueue.empty() << endl;
	return action;
}

void Agent::check_move(Percept percept)
{
	for(int i=0;i<4;i++)
	{
		move_dir[i] = true;
	}
	
	//cout << "orientation = " << orientation << endl;

	//RIGHT 0, UP 1, LEFT 2, DOWN 3
	
	if (percept.Breeze)
	{
		if(cLoc.Y >= 3 || worldStatus[cLoc.X][cLoc.Y+1].Pit != NO) move_dir[0] = false;
		if(cLoc.X >= 3 || worldStatus[cLoc.X+1][cLoc.Y].Pit != NO) move_dir[1] = false;
		if(cLoc.Y <= 0 || worldStatus[cLoc.X][cLoc.Y-1].Pit != NO) move_dir[2] = false;
		if(cLoc.X <= 0 || worldStatus[cLoc.X-1][cLoc.Y].Pit != NO) move_dir[3] = false;
	}
	
	if(percept.Stench)
	{
		if(cLoc.Y >= 3 || worldStatus[cLoc.X][cLoc.Y+1].Wumpus != NO) move_dir[0] = false;
		if(cLoc.X >= 3 || worldStatus[cLoc.X+1][cLoc.Y].Wumpus != NO) move_dir[1] = false;
		if(cLoc.Y <= 0 || worldStatus[cLoc.X][cLoc.Y-1].Wumpus != NO) move_dir[2] = false;
		if(cLoc.X <= 0 || worldStatus[cLoc.X-1][cLoc.Y].Wumpus != NO) move_dir[3] = false;
	}
	
	if(cLoc.Y >= 3 || worldStatus[cLoc.X][cLoc.Y+1].Visited == true) move_dir[0] = false;
	if(cLoc.X >= 3 || worldStatus[cLoc.X+1][cLoc.Y].Visited == true) move_dir[1] = false;
	if(cLoc.Y <= 0 || worldStatus[cLoc.X][cLoc.Y-1].Visited == true) move_dir[2] = false;
	if(cLoc.X <= 0 || worldStatus[cLoc.X-1][cLoc.Y].Visited == true) move_dir[3] = false;
	
	for(int i=0;i<4;i++)
	{
		move[i] = move_dir[(i+ (int)orientation)%4];
		//cout << "move[" << i << "] = " << move[i] << endl;
	}
}


void Agent::goBack()
{	
	actionqueue.push(TURNLEFT);
	actionqueue.push(TURNLEFT);
	Action lastaction;
	while(actionlist.size() > 0)
	{
		lastaction = actionlist.back();
		if(lastaction==TURNLEFT)
		{
			actionqueue.push(TURNRIGHT);
		}
		else if(lastaction==TURNRIGHT)
		{
			actionqueue.push(TURNLEFT);
		}
		else if(lastaction==GOFORWARD)
		{
			actionqueue.push(GOFORWARD);
		}
		actionlist.pop_back();
	}
	actionqueue.push(CLIMB);
}

void Agent::GameOver (int score)
{

}





