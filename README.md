# AI Algorithm for Reversi

### Report of CS303A Project-1 

### 11812520 张淘月

------

#### 1. Preliminary

##### 1.1. Problem&Target

Reversi is a kind of two person competitive chess game. Both sides use pieces of different colors to play chess on a square board in turn. The initial board will have two black pieces and two white pieces. You must choose the position where you can eat the opponent's pieces. When the chess pieces under one side and the pieces of its own color clamp the pieces of the other color, the other color chess pieces will be changed into their own colors. (including horizontal, vertical and oblique) When there is no place to go, the winning party is judged by the number of pieces with different colors on the current chessboard.

 The purpose of this project is to complete the intelligent game program according to the rules and search algorithm of Reversi. The criterion for judging whether this program is intelligent is whether it can win in the game.

##### 1.2. Software

This project uses Pycharm to write Python code, and tests the feasibility of the code and whether it has enough intelligence through the war platform Reversi.

##### 1.3. Algorithm

This project is based on Minimax and Alpha-Beta Pruning Algorithm. In addition, it also uses the evaluation function for the current chessboard and the function to find the executable point and the execution result according to the Reversi rules.

##### 1.4 Application

We can apply it in the teaching of Reversi, for each board can get the best choice to guide beginners.

The search algorithm used in the Reversi program is a general idea to solve this kind of chess problem. We can use the Minimax and Alpha-Beta Pruning Algorithm in Go and Chess to get more intelligent chess program. 

In addition, when we want to solve other problems in real life, we can also refer to this idea to list possible situations and evaluate them to make better decisions

------

#### 2. Methodology

##### 2.1. Notations

- **(x,y)** means the position of point at (x,y) 	
- **E** The advantage degree of the current chessboard for ourselves
- **k** The important coefficient for the mobility
- **N<sub>w</sub>** The number of point that white can choose
- **N<sub>b</sub>**  The number of point that black can choose
- **h** The height of the chess board
- **w** The width of the chess board
- **V(x,y)** The importance of point(x,y) depend on the assess matrix
- **C(x,y)** The color of the point(x,y) depend on chessboard

##### 2.2. Data Structures

- ```python
  COLOR_BLACK = -1 , COLOR_WHITE = 1 , COLOR_NONE = 0
  #In Reversi's chessboard we represent the white as 1 and black as -1 
  ```

- ```python
  chessboard_size
  #chessboard_size is the length of the square normally 8
  ```

- ```python
  color
  #represent the color of the player in the turn
  ```

- ```python
  candidate_list
  #A list of the optional points tuple (x,y), last one are the best choice 
  ```

- ```python
  chessboard
  #A 8*8 list represent the chessboard , white pieces are 1 ,black are -1
  ```

- ```python
  choice
  #The list of optional points tuple (x,y), meas the points in "choice" are legal
  ```

- ```python
  assess = [[2000,-60 ,  300, 200, 200,  300,  -60,  2000],
            [-60 ,-400 ,   1,  1,  1,   1,  -400,   -60],
            [300  ,   1,  10,  5,  5,  10,    1,    300],
            [200  ,   1,   5,  3,  3,   5,    1,    200],
            [200  ,   1,   5,  3,  3,   5,    1,    200],
            [300  ,   1,  10,  5,  5,  10,    1,    300],
            [-60 , -400,   1,  1,  1,   1,  -400,   -60],
            [2000, -60,  300, 200, 200,  300,  -60,  2000]]
  #Use this list to calculate the value of each points, used to calculate the degree of advantage for the chessboard
  ```

##### 2.3. Model design

###### 2.3.1. Functions

```python
class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        #The declare function 
        
    def go(self,chessboard):
        #The main function
        
    def search(self,color,board,deep,alpha,beta,t):
        #To do the search process, the return value are a point (x,y) when deep equals 1 otherwise return the max value or min value. The color means the color of player in the turn, board means the chessboard current, deep means the search layer current, t means the stop layer 
        
    def find_choice(self, chessboard, color):
        #Find all position that player can choice, return value are a list of tuple (x,y). Parameter chessboard are the current chessboard ,color are the color of player in the turn. 
        
    def find_change(self,chessboard,color,choice):
        #To find the board after a choice, return value are list: chessboard. Parameter chessboard means the chessboard before change ,the color means the color of player in the turn, choice is a point (x,y) means the player want to choice  
        
    def assess(self,board):
        #Find the degree of advantage for current chessboard for ourselves, return an interger. Board are the current chessboard.
```

###### 2.3.2. Program processing

Because the search time of different layers has a huge different, the search process of **layer 2**, **layer 4** and **layer 6** will be executed respectively during the execution of the whole program. 

The **search()** method is called recursively in each search process. In each layer, according to the parity of the deep of layers to determine whether the current maximum or minimum search. Then, according to the results of the method **find_choice()**, find the changed chessboard for each result by **find_change()**, and finally search the next layer according to the results of the previous results. When the current depth is equal to the specified maximum depth, the current chessboard is estimated by **assess()** and return the assess value. if deep equals to 1 return the (x,y). Finally the main method add the search result to candidate_list.

###### 2.3.3. Assess method

- **For self color equals to white**
  $$
  E =k*(N_w-N_b)+\sum_{x=0}^{h-1}\sum_{y=0}^{w-1} V(x,y)*C(x,y)
  $$
  
- **For self color equals to black**

  
  $$
  E =k*(N_b-N_w)-\sum_{x=0}^{h-1}\sum_{y=0}^{w-1} V(x,y)*C(x,y)
  $$
  **And the V(x,y) will change in many special condition , we will talk about it in detail.**

##### 2.4. Details of Algorithm

- **Go(self,chessboard):**

  Perform the search process in the main method **go**. Because the search process time of different layers is very different, executing the search process with fewer layers first will hardly affect the total number of search layers. Therefore, a two-level search is performed to ensure that the program has the most basic intelligence. In most cases, the four layer search can be performed smoothly. When there are few branches in the last few steps, six layers can be searched

  ```pseudocode
  Function go(chessboard)
  	candidate_list <- find_choice(chessboard, color)
      alpha <- -99999
      beta  <- 99999
      new_point <- search(color,chessboard,1,alpha,beta,2)
      candidate_list <- candidate_list + new_point
      /* Two layer search ensures basic intelligence*/
      new_point <- search(color,chessboard,1,alpha,beta,4)
      candidate_list <- candidate_list + new_point
      /* In general, four levels of search can be completed*/
      new_point <- search(color,chessboard,1,alpha,beta,6)
      candidate_list <- candidate_list + new_point
      /*The last few steps lead to layer 6*/
  ```

- **Search(color,board,deep,alpha,beta,t):**

  Alpha beta pruning optimization method based on minimax search. When the chessboard is evaluated at the deepest level and the evaluation results are returned, the coordinates of the point are returned at the depth of 1.

   When returning to the evaluation function, the valuation result is changed according to the difference of current action force.

  ```pseudocode
  Function Search(color,board,deep,alpha,beta,t)
  	if deep = t then
  		choice <- find_choice(board,self.color)
          un_choice <- find_choice(board,-self.color)
          return assess(board)+(len(choice)-len(un_choice))*220
          /*When the search depth is reached, the evaluation of mobility is completed and the current chessboard is returned*/
      else
          if deep is odd then /*Maximum search based on beta pruning*/
                  choice <- find_choice(board,color)
                  if len(choice)!=0 then
                      a <- -99999
                      b <- 0
                      for i <- 0 to len(choice)
                          newboard <- find_change(board,color,choice[i])
                          n <- search(-color,newboard,deep+1,alpha,beta,t)
                          if n is not None then
                              if n>a then
                                  a <- n
                                  b <- i
                              if a>=beta then
                                  if deep==1 then
                                      return choice[i]
                                  return a
                              alpha <- max(alpha,a)
                      if deep==1 then
                          return choice[b]
                      return a
          else /*Minimum search based on alpha pruning*/
                  choice = find_choice(board,color)
                  if len(choice)!=0 then
                      a <- 99999
                      b <- 0
                      for i <- 0 to len(choice)
                          newboard <- find_change(board,color,choice[i])
                          n <- search(-color,newboard,deep+1,alpha,beta,t)
                          if n is not None then
                              if n<a then
                                  a <- n
                                  b <- i
                              if a<=alpha then
                                  if deep==1 then
                                      return choice[i]
                                  return a
                              beta <- min(beta,a)
                      if deep==1 then
                              return choice[b]
                      return a
  ```

- **assess(board):**

  The evaluation is based on the valuation matrix defined in the data.

  Use status to represent the number of pieces on the current chessboard. When the last few steps are left, the strategy will be changed, instead of occupying edges and corners, to occupy more pieces. 

  Moreover, considering the factor of stabilizer, when the corner is occupied, the valuation of the pieces on the corner will be changed

  ```pseudocode
  Function assess(board)
          status = 0
          for i <- 0 to chessboard_size
              for j <- 0 to chessboard_size 
                  if board[i][j]!=0 then
                      status <- status+1
          /*status means whats the step No. current*/            
          if board[0][0]!=0 then
              if board[0][1] == board[0][0] then
                  assess[0][1] <- 400 
              if board[1][0] == board[0][0] then
                  assess[1][0] <- 400
              if board[0][1] == board[0][0] and board[1][0]==board[0][0] and board[1][1]==board[0][0] then
                  assess[1][1] <- 100
                  /*it means that at first the (0,1) or (1,0) are dangerous but when (0,0) and (0,1) are same color it will be more important and not dangerous*/
          if board[0][7]!=0 then
              if board[0][6] == board[0][7] then
                  assess[0][6] <- 400
              if board[1][7] == board[0][7] then
                  assess[1][7] <- 400
              if board[0][6] == board[0][7] and board[1][7]==board[0][7] and board[1][6]==board[0][7] then
                  assess[1][6] <- 100
                  /*same to other corner*/
          if board[7][0]!=0
              if board[6][0] == board[7][0] then
                  assess[6][0] <- 400
              if board[7][1] == board[7][0] then
                  assess[7][1] <- 400
              if board[6][0] == board[7][0] and board[7][1]==board[7][0] and board[6][1]==board[7][0] then
                  assess[6][1] <- 100
          if board[7][7]!=0 then
              if board[6][7] == board[7][7] then
                  assess[6][7] <- 400
              if board[7][6] == board[7][7] then
                  assess[7][6] <- 400
              if board[7][6] == board[7][7] and board[6][7]==board[7][7] and board[6][6]==board[7][7] then
                  assess[6][6] <- 100
          if status>60 then
              assess <- [[500, 500, 500, 500, 500, 500, 500, 500],
                        [500, 500, 500, 500, 500, 500, 500, 500],
                        [500, 500, 500, 500, 500, 500, 500, 500],
                        [500, 500, 500, 500, 500, 500, 500, 500],
                        [500, 500, 500, 500, 500, 500, 500, 500],
                        [500, 500, 500, 500, 500, 500, 500, 500],
                        [500, 500, 500, 500, 500, 500, 500, 500],
                        [500, 500, 500, 500, 500, 500, 500, 500]]
          /*it means at the last 5 step we will change the strategy we want more pieces not the corner or bridge*/              
  
          sum = 0
          for i <- 0 to chessboard_size
              for j <- 0 to chessboard_size
                sum <- sum + assess[i][j]*board[i][j]
          /*calculate the advantage degree for white*/      
          if self.color == -1 then
              sum <- -sum
          /*black are negitive to white*/    
          return sum
  ```

  

------

#### 3. Empirical Verification

##### 3.1. Dataset

In the first stage, I mainly use the course resource utility_test to confirm find in my code_ Whether the choice function is correct.

In the later stage, I mainly download the logs in reveri and input the key steps chessboard data in program to observe the execution steps and results of the code in the test. And i also make some special chessboard   that must occupy the border or corner to test the program. 

When I can't use Playto, I use the website Botzone to adjust the parameters. Botzone is a chess fighting platform with upload code. You can see the result of the fight, adjust your own parameters and learn other people's fighting ideas on the platform.

##### 3.2. Performance measure

I mainly judge the running time of the code by observing the times of timeout in the running log. My focus is on how to balance the number of search layers and runtime. When the number of search levels increases, the result is more reasonable, but if the time-out, it will return random results. When I initially set the number of search layers as three, I could only hit the 70th place in the ranking. Moreover, when the number of users is too large, the number of search layers the server can carry can only reach three. Later, I tried to use the code of searching 5 layers at the midnight while everyone was sleeping.  Then i got the rank 30 .But next day my code are always time out so i back to 70th place. 

Then I tried a new approach. In the end, I tried searched three times, because it can get better results within the specified time. Using two layers to protect the bottom, use four layers and six layers to get more reasonable results. In the end, I stabilized around 30.

##### 3.3. Hyper Parameters

- **Weight**

  The weight parameter is used to determine the importance of each point. And through the importance of each point to determine who is more favorable to the current situation, and finally find a way to achieve the most favorable situation.

- **status**

  According to the number of pieces on the board to determine the progress of the game, there will be different decisions in different stages. In the early stage, more emphasis will be placed on the occupation of corners and edges, and in the later stage, more emphasis will be placed on the number of simple pieces

- **deep**

  Use deep to control the number of layers to search, so that different levels can be searched according to the time the program can use

##### 3.4. Experimental results

- The test cases I pass in usability test is 10.
- My rank in the points race is 33<sup>th</sup>.
- My rank in the round robin is 49<sup>th</sup>.

##### 3.5. Conclusion

I think my algorithm for the weight of the corner and border in the early and mid-term is more reasonable, and the hierarchical search structure can also provide good computing power to search for more layers, so it is easy to get the corner and edge in the process of fighting with others. 

However, compared with the advantages in the early and mid-term, it is easy for my algorithm to choice the (1, 1) in the later stage because of too much emphasis on edges. Finally, the situation will be reversed after others occupy the corner.

Therefore, I think that if i can divide the stages into more detailed stages, i can adjust each stage to a more suitable strategy for that stage. In this way The algorithm will be better.

Through this project, I learned the principle of search algorithm and optimization, which can let me solve other similar chess problems. And i will apply this idea to my life, i can also solve other decision-making problems.

------

#### 4. References

[1] Shoham, Y., & Toledo, S. (2002). Parallel randomized best-first minimax search. \emph{Artificial Intelligence, 137}(1-2), 165-196.

[2] Olivito, J., Resano, J., & Briz, J. L. (2017). Accelerating board games through Hardware/Software codesign. \emph{IEEE Transactions on Computational Intelligence and AI in Games, 9}(4), 393-401

[3] Reversi. (2014, August 11). In . Retrieved November 1, 2020, from https://wiki.botzone.org.cn/index.php?title=Reversi&action=info

[4] M. Buro, Experiments with Multi-Probcut a new high-quality evaluation function for Othello, in: H.J.vanden Herik, H. Iida (Eds.), Games in AI Research, Proceedings of a Workshop on Game-Tree
Search Held in1997 at NECI in Princeton, NJ, Universiteit Maastricht, The Netherlands, 2000, pp. 77
–96.