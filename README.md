Group Practical Proposal
Target User
A football manager / coach looking to improve their team by using our project.
Main Features
Lineup helper - which players should you choose to play, and which should you buy
Lineup comparison - Which lineup performs best against an opposing team
Simple stats view - comparing player and team stats such as pass success, goals scored per match
Heatmap of player positions when scoring / passing / defending
Sources of data
https://datahub.io/dataset?tags=football

http://www.bbc.co.uk/sport/football/results

https://github.com/openfootball/eng-england

http://api.football-data.org/index

http://www.football-data.co.uk/data.php

https://www.whoscored.com/




















Database
Player: goals scored, scoring attempts, attempts on target, through balls, key passes, successful passes in the attack scale, total tackles, clearances, interceptions, duels won (I will want to include these in the analysis. Everything can be found in whoscored.com)


Teams
Database details:
Host: football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com
Port: 5432
Database name: postgres
Master Username: coxswain
Password: (see comment in facebook group)


Analysis
Goals per team in match are estimated quite well by a poisson distribution. This was the basis of the Dixon and Coles model (1997)


A simple model of prediction can be based on solely on goal data from a team. The outcome of a game can be predicted by a bi-variate poisson distribution. The parameter from the home team is a combination of home teams average goals scored and away teams goals conceded and the parameter for the away team is found similarly. We can adjust the parameters to incorporate home advantage and form.

Instead of just using the team data for goals we can find the contribution per player and combine these in an appropriate way to find the basis for the poisson parameter. This will allow predicted performance of a given line-up.

However this model is very simplistic and ideally we will try to implement something based on the following paper:
·      http://www.diva-portal.org/smash/get/diva2:751709/FULLTEXT01.pdf
      It predicts match outcome for different lineups using Bayesian networks. (includes suggestions for how to set up database as well):


Predicting player’s market value (linear regression). Based on paper:
·     https://www.stat.berkeley.edu/~aldous/Research/Ugrad/Yuan_He.pdf

    Referee analysis

    Tactical Analysis
Do formation analysis to find average goals scored, conceded, possession etc for different formations (Helps manager to pick a formation to suit their philosophy)
Is the possession based game a good idea or is it better to sit back and hit them on the counter? Investigate the correlation between possession and points per game.
Lots of different stats we could compare to see the correlation between them. Can analyse correlation between any two of shots, goals, possesion, passing accuracy...etc. Some we would expect very high correlation eg shots/goals but others might be less obvious eg shots/passing accuracy.






Frontend
There should be a list of teams and each team should have a page with players, stats, interesting facts (found from analysis, if any).

Each player will have a page with basic info and relevant stats.

The lineup comparison will be a drag and drop interface to place players on a football field, and see the predicted score. It should look something like this:

http://uk.soccerway.com/matches/2016/03/05/england/premier-league/tottenham-hotspur-football-club/arsenal-fc/2043446/?ICID=PL_MS_01

We will also display heatmaps such as the in the picture below, for the most active areas of the pitch for shooting / passing on each player’s page. This can be achieved by using multivariate KDEs (https://en.wikipedia.org/wiki/Multivariate_kernel_density_estimation).


















                   
User-Task: Line-Up Manager
                   
Requirements:
- View and choose line-up: Be able to view the line-up in a nice visual manner with the ability to change the line-up easily.
- Assess Line-Up: After choosing a line-up receive analysis of the line-up in terms of an attack and a defence score.
- Suggested Line-Up: After inputting restrictions on formation and the pool of players to choose from, receive suggestions for what line-up to play.

                   
User-Task: Player-Analysis
                   
Requirements:
- Player Statistics: View detailed player specific details eg. goals per game,
- Comparison: Compare players side by side
- Transfer Info: View basic transfer information for the player eg. Current market value

                   
User Task: Team Analysis
                   
Requirements:
- Team Statistics: View team statistics such as goals per game, possession per game etc.
- Player List: List of players on the team along with links to their individual statistics pages.
- Compare Teams: Compare teams side by side
- Interesting Facts: Any interesting statistical outliers about this specific team Eg. This team scores 30% of its goals in the last ten minutes of the game.


                   
User-Task: Tactical Advice
                   
Requirements:
- Formation Analysis: Average goals scored, goals conceded and possesion for different formations. (A manager could use these statistics to pick a formation that suited his philosophy eg possesion based game).
- Possession: Analyse the correlation between possession and success. Is it better to play a possession based game or to sit back and hit on the counter attack?

                   

User Task: Transfer Advice
                   
Requirements:
- Market Value: View current market value of a given player
- Expected Growth: View expected market value of a player over time
- Search Facility: Specify the kind of player you want and get suggestions (Eg. Central defenders who are under 25)



                   
Time Line:
                   
Week 1:
Back-End: Start putting data from whoscored.com into a database.
Analysis: Read paper on player prediction to try and understand the model
Front-End: Player Pages

Week 2:
Back-End: Continue putting data into database.
Analysis: Start line-up analysis
Front-End: Team Pages

Week 3:
Analysis: Continue work on line-up analysis
Front-End: Start work on line-up pages

Week 4:
Analysis: Tactical analysis/ Start transfer analysis
Front-End: Continue work on line-up pages

Week 5:
Analysis: Finish transfer Analysis
Front-End: Transfer pages


