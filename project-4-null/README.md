# project-4-null
project-4-null created by GitHub Classroom
## website
### how to start
* ./webpage/index.html is our homepage, our story begin here.
## network.py
* build network graph based on the rules below 
   Network rules :   Each node represents one state. If the difference between the
   hospital capacity of the state A and state B is within a specific value,
   then regard them as similar states and draw a edge from node A to node B.
   The weight of each edge is determined by the difference of two nodes' willingness.
 * needed file : ../dataset/labeled.csv  
### how to run
* python network.py [date]
[date]: build the network based on this date (2021-1-15 ~ 2021-10-14)
expample python network.py 2021-10-14
### outputs 
* network.csv : store network graph, edges 
* Console : 
  * network information : betweeness, degree, and density
  * Clustering information: clustering coefficient, modularity.
  
## interactive_visualization.py
* draw four interactive visualization graph about the distribution of (vaccination, death, infected people) map 

### how to run
* python interactive_visualization.py [date]
[date]: build the network based on this date (2021-1-15 ~ 2021-10-14)
expample python interactive_visualization.py 2021-10-14

### outputs 
* four html files 
