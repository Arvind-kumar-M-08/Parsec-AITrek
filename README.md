# AITREK



![image](https://user-images.githubusercontent.com/79975787/226158229-1a5abb35-7591-4366-9d82-b9368b1d3e70.png)

## Table of Contents
1. [Overview](#overview)
2. [Winning Criteria](#winning)
3. [Documentation](https://github.com/Arvind-kumar-M-08/Parsec-AITrek/blob/main/Documentation.md)
4. [Instructions for running](#instructions)
5. [Whatsapp group link for support](#whatsapp)

## Overview <a name="overview"></a>
In the vast and uncharted reaches of space, the AITREK tournament has begun. The most daring and skilled crews have embarked on this grand adventure, with their sights set on glory and conquest.
Each team brings with them a formidable fleet of five starships, each crewed by the bravest and most skilled adventurers in the galaxy. Armed with the latest in advanced technology and weaponry, these crews are ready to face any challenge and overcome any obstacle.
Their mission is to conquer the region, to vanquish all who stand in their way and emerge victorious as the last team standing. The stakes are high, the competition fierce, and the outcome uncertain.
As the starships converge upon the region, they must navigate treacherous asteroid fields and overcome other perils of deep space. The battle is intense and unrelenting, with the starships maneuvering and firing with deadly accuracy. The crews communicate with each other in a flurry of strategy and coordination, seeking to gain an advantage over their opponents. 
In the end, only one team remains, triumphant and victorious. Their starships stand tall, having vanquished all who stood in their way, leaving behind a legacy of bravery, skill, and adventure.

### Battle Arena:
This game features a continuous 2D map with coordinates ranging from  [-200, 200] in both x and y directions. There are two teams, namely red and blue. Each team will start their game with 5 starships. The entire arena is filled with stationary, polygon-shaped asteroids of varying sizes. This map can be chosen from 3-4 pre-generated maps. 
Your objective is to take down the enemy starships by gliding through the empty vacuum of space and shooting plasma shells at your enemy starships while avoiding asteroids in your way.
You could make a truce and not consider attacking at all. But there is a catch! There is a dark energy vortex consuming the space around you. Your starships will continuously take damage if it crosses into the vortex. Your only chance of escape is to kill all the enemy starships before the vortex converges and kills everyone.. 


### Starships (Agents):

![Screenshot 2023-03-15 234938](https://user-images.githubusercontent.com/79975787/226156681-a6086046-30b1-46d3-8597-de2d71b3e2e8.png)


The starship (Agent) is a circular object with a radius of 5 units. The agents can view in a semicircular range with a radius of 50 units in the agent's orientation.
Orientation() is with respect to the positive X-axis represented as a point 
(cos theta, sin theta). In the above image red agent’s orientation is (1,0), and that of the blue is (cos(pi/4), sin(pi/4)).

### Health
Each agent starts with a health of 100 units, and it decreases in the following cases:
Hit by bullet: 10 units
Outside zone for 1-time unit: 1 unit

### Firing
The location of the bullet is represented by a Point(x,y) and moving direction (cos , sin ). The bullet disappears after 10 time units, and the bullet speed is 5 times that of the agent.
The agent cannot fire in consecutive time units. 

### Vortex (Zones)
We define two types of zones one is the current zone (white border), another one is the safe zone (red border). The current zone is the current play area, i.e., all of the region that the agent can move in without loosing health. If the agent is outside the current zone, the health decreases as mentioned in the health section. Safe zone is the zone that the current zone will converge to in the immediate future after specified time intervals Each zone type is defined by four Points in clockwise direction the first one being the top-right.

The zone-shrinking times will be given as a list of time units. When the game reaches the ith time unit, the current zone linearly converges to the safe zone. The convergence happens by time unit (time[i] + time[i+1]) / 2. After immediately after full convergence, the new safe zone coordinates are given

The current zone is converged to a square of side 10 units in the final time interval.

For example if the Zone shrink times are [100, 200, 300, 500], At the start of the game, safe zone is given. The current zone starts shrinking at the 100th time unit and shrinks to the safe zone at 150th time unit. At this time, you will be given the next safe zone. Again the zone shrinking starts at 200 and this repeats.  Since 300-500 is the final time interval, the zone shrinks to a square of side 10 units by 500th time unit.

### Astroids(Obstacles)
The obstacles are polygons identified by vertices of the polygon in order. If the starship (Agent) collides with the asteroid, you will stay in the same place. Agents cannot see the other agents hiding behind the astroids.
If the plasma shell (bullet) collides with the obstacle, the plasma shell(bullet) dies.

### Scores
The scores of a team are the sum of the health lost by the other team.
If the score of a team reaches 500, they win. I.e., if all the agents in the opponent team die, your team wins. If all the agents of both teams die simultaneously, the run is considered a draw and not considered in the final score.


## Winning Criteria  <a name="winning"></a>
The match will be best of 3 runs. The team which wins 2 runs first will be considered the winner.

## Documentation <a name="documenation"></a>
You can view documenation [here](https://github.com/Arvind-kumar-M-08/Parsec-AITrek/blob/main/Documentation.md)

## Instructions for Running  <a name="instructions"></a>
### Installation
1. Clone the repository using the following command

```git clone https://github.com/Arvind-kumar-M-08/Parsec-AITrek.git```

2. Change directory to Parsec-AITrek:
```cd Parsec-AITrek```

3. Install the requirements using

```pip install -r requirements.txt```

### Running
Edit the ```tick()``` function in players/player_red.py and players/player_blue.py

We have given a random bot in players/player_red.py while players/player_blue is an empty bot.

YOU SHOULD NOT MODIFY ANY OTHER FUNTION OTHER THAN ```tick()```. YOU MAY WRITE NEW FUNCTIONS OR CLASSES BUT DO NOT MODIFY OTHER PRE-WRITTEN CODE.

In case you are running on a windows environment, run the following command in ***git bash***. *DO NOT USE WSL*

1. Run ```bash start.sh``` to start env and players.
2. players are in playes folder


Note: 

1. Windows users  should use ***git bash*** to run the bash script (.sh)
2. The instructions to install ***git bash*** can be found [here](https://git-scm.com/downloads) 
3. You need to submit both player_red.py and player_blue.py


## WhatsApp Link for Support <a name="whatsapp"></a>
[WhatsApp Invite Link](https://chat.whatsapp.com/E8JfBWU0YWEFvdku345XLw)

