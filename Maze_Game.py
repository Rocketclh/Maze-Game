def game(): #CLI game control
    global steps
    global Board
    global Size
    global Type_error
    global Difficulty
    global rec_step
    global Time_up
    if Type_error:
        Type_error=False
    else:
        print_board()
    temp=player_found() #Found player location
    x=int(temp[0:2])
    y=int(temp[2:4])
    if Difficulty == 5:
        if steps == rec_step:
            end(False)
    ans=input("System: Please enter the direction you want to move ")
    ans=ans.lower()
    if Difficulty != 5 or not(Time_up): #Time up check for Hard mode
        if ans == "w": #Move up
            if y < (Size-1) and Board[x][y+1] != "X":
                Board[x][y]=" "
                y=y+1
                steps=steps+1
                if Board[x][y] == "E":
                    end(True)
                else:
                    Board[x][y]="P"
            else:
                print("System: Invalid move!")
                print("System: You cannot move up")
                Type_error=True
                time.sleep(0.5)
        elif ans == "s": #Move down
            if y > 0 and Board[x][y-1] != "X":
                Board[x][y]=" "
                y=y-1
                steps=steps+1
                if Board[x][y] == "E":
                    end(True)
                else:
                    Board[x][y]="P"
            else:
                print("System: Invalid move!")
                print("System: You cannot move down")
                Type_error=True
                time.sleep(0.5)
        elif ans == "a": #Move left
            if x > 0 and Board[x-1][y] != "X":
                Board[x][y]=" "
                x=x-1
                steps=steps+1
                if Board[x][y] == "E":
                    end(True)
                else:
                    Board[x][y]="P"
            else:
                print("System: Invalid move!")
                print("System: You cannot move left")
                Type_error=True
                time.sleep(0.5)
        elif ans == "d": #Move right
            if x < (Size-1) and Board[x+1][y] != "X":
                Board[x][y]=" "
                x=x+1
                steps=steps+1
                if Board[x][y] == "E":
                    end(True)
                else:
                    Board[x][y]="P"
            else:
                print("System: Invalid move!")
                print("System: You cannot move right")
                Type_error=True
                time.sleep(0.5)
        elif len(ans) != 1:
            print("System: Out of Range!")
            print("System: Please enter single character")
            Type_error=True
            time.sleep(0.5)
        else:
            print("System: Invalid input!")
            print("System: Please enter 'W', 'A', 'S', or 'D'")
            Type_error=True
            time.sleep(0.5)
        game()

def end(win): #win output
    global steps
    global rec_step
    global mode
    global screen
    global pen
    global Time_up #Time up register
    global Timer_stop #Timer stop register
    global Exit_bt
    global Restart_bt
    global page
    global player
    global Minutes
    global Second
    if mode == 1: #CLI end output
        if win:
            print("System: Congratulations!")
            print("System: You have exited the maze!")
        else:
            print("System: Game Over")
            print("System: You have used all of the steps")
        print("System: Total steps taken:", steps)
        print("System: Maze recommended steps:", rec_step)
        print("System: Time spend:"+str(Minutes)+" minutes "+str(Second)+" seconds")
        time.sleep(0.5)
        ans=input("System: Press Enter to exit the game or type '/restart' to restart the game ")
        if ans.lower() == "/restart":
            for i in range(5):
                print("")
            Menu_CLI()
        else:
            sys.exit()
    elif mode == 2: #GUI end output
        Timer_stop=True
        page=5
        screen.clear() #Clear screen
        screen.setup(width=550, height=650)
        screen.tracer(0)
        screen.update()
        pen.clear() #Reset pen
        pen.penup()
        player.hideturtle()
        screen.update()
        style="Arial", 25, "bold"
        y=100
        if win:
            pen.goto(0,y)
            pen.write("Congratulations!", align="center", font=(style))
            y=y-50
            pen.goto(0,y)
            pen.write("You have exited the maze!", align="center", font=(style))
        else:
            pen.goto(0,y)
            pen.write("Game Over", align="center", font=(style))
            y=y-50
            pen.goto(0,y)
            if Time_up: #Times up
                pen.write("You ran out of time", align="center", font=(style))
            else:
                pen.write("You have used all of the steps", align="center", font=(style))
        y=y-50
        pen.goto(0,y)
        text="Total steps taken:"+str(steps)
        pen.write(text, align="center", font=(style))
        y=y-50
        pen.goto(0,y)
        text="Maze recommended steps:"+str(rec_step)
        pen.write(text, align="center", font=(style))
        y=y-50
        pen.goto(0,y)
        text="Time spend:"+str(Minutes)+" minutes "+str(Second)+" seconds"
        pen.write(text, align="center", font=(style))
        y=y-50
        pen.goto(-200,y)
        Restart_bt=Button(-175,y,200,50,"Restart",style)
        Restart_bt.draw()
        pen.goto(50,y)
        Exit_bt=Button(50,y,150,50,"Exit",style)
        Exit_bt.draw()
        screen.update()
        screen.onclick(button_click)
        movement_unblind()
        screen.listen()

def print_board(): # board
    global Board
    global Size
    print("")
    for y in range(Size): #0,0 at bottem left corner
        h=Size-y-1 #Height of the board
        if h<10:
            temp="0"+str(h)
        else:
            temp=str(h)
        print(temp, *[Board[x][h] for x in range(Size)])
    print("")

def build_maze():
    global Board
    global Size
    global mode
    global mn
    global Difficulty
    mn=str(random.randint(1,999)) #Random generate maze ID
    if mode == 1:
        print("System: Loading Maze 0"+mn+"...")
    temp=Difficulty
    if Difficulty == 5:
        temp=4
    Size=(temp+1)*10+1 #Calculate board size
    Method=2 #Maze generation method using
    if Method == 1: #Loop-erased random walk method
        #Maze format: node only
        #Board format: node, path and wall
        #Grid format: Location vector in "0519" form, x=5 y=19
        Board=[["X"] * Size for z in range(Size)]
        x=1
        y=1
        Board[x][y]=" "
        Maze=[["F"] * int((Size-1)/2) for n in range(int((Size-1)/2))] #Store the cells that are part of the maze, stored in Maze format
        x=int((x+1)/2-1) #Converting location vector from Board format to Maze format
        y=int((x+1)/2-1)
        Maze[x][y]="T"
        Done=False #Register maze is fully finished
        while not(Done): #Check is all node included in the maze
            Done=True
            Not_Maze=[] #The cells that are not part of the maze, 1D array, stored in maze format
            for h in range(0,len(Maze)): #x-axis
                for v in range(0,len(Maze)): #y-axis
                    if Maze[h][v] == "F": #Check is it part of maze
                        Done=False
                        Not_Maze.append(grid(h,v)) #Storing the Location vector in Grid format
            if not Done:
                temp=Not_Maze[random.randint(0,len(Not_Maze)-1)] #In Maze format
                x=int(temp[0:2])
                y=int(temp[2:4])
                x=2*x+1 #Converting location vector from Maze format to Board format
                y=2*y+1
                Path=[temp] #Store walked path, stored in Board format
                while Maze[int((x+1)/2-1)][int((y+1)/2-1)] != "T":
                    retry=False
                    Direction=random.randint(1,4) #1:Up 2:Down 3:Left 4:Right
                    Steps=random.randint(1,2)*2
                    if Direction == 1: #Move up
                        if y+Steps > Size-1:
                            retry=True
                        else:
                            for t in range(Steps):
                                y=y+1
                                found=False
                                for c in range(1,len(Path)):
                                    if Path[c] == grid(x,y):
                                        m=c
                                        found=True
                                if found:
                                    Path = Path[:(m-1)] #Remove the path cycle
                                else:
                                    Path.append(grid(x,y)) #Storing the Location vector in Grid format
                    elif Direction == 2: #Move down
                        if y-Steps <= 0:
                            retry=True
                        else:
                            for t in range(Steps):
                                y=y-1
                                found=False
                                for c in range(1,len(Path)):
                                    if Path[c] == grid(x,y):
                                        m=c
                                        found=True
                                if found:
                                    Path = Path[:(m-1)] #Remove the path cycle
                                else:
                                    Path.append(grid(x,y)) #Storing the Location vector in Grid format
                    elif Direction == 3: #Move left
                        if (x-Steps) <= 0:
                            retry=True
                        else:
                            for t in range(Steps):
                                x=x-1
                                found=False
                                for c in range(1,len(Path)):
                                    if Path[c] == grid(x,y):
                                        m=c
                                        found=True
                                if found:
                                    Path = Path[:(m-1)] #Remove the path cycle
                                else:
                                    Path.append(grid(x,y)) #Storing the Location vector in Grid format
                    elif Direction == 4: #Move right
                        if x+Steps > Size-1:
                            retry=True
                        else:
                            for t in range(Steps):
                                x=x+1
                                found=False
                                for c in range(1,len(Path)):
                                    if Path[c] == grid(x,y):
                                        m=c
                                        found=True
                                if found:
                                    Path = Path[:(m-1)] #Remove the path cycle
                                else:
                                    Path.append(grid(x,y)) #Storing the Location vector in Grid format
                for n in range(0, len(Path)-1): #Register paths into maze
                    temp=Path[n] #Load grid into temp, in Board format
                    x=int(temp[0:2])
                    y=int(temp[2:4])
                    Board[x][y]=" "
                    if n%2 == 0 :
                        x=int((x+1)/2-1) #Converting location vector from Board format to Maze format
                        y=int((y+1)/2-1)
                        Maze[x][y]="T"
                check_state(Maze,Not_Maze,Done)
                for k in range(Size): #Redraw the edge
                    Board[0][k] = "X"
                    Board[Size-1][k] = "X"
                    Board[k][0] = "X"
                    Board[k][Size-1] = "X"
    elif Method == 2: #Recursive division method
        #Grid format: Location vector in "0519" form, x=5 y=19
        Board=[[" "] * Size for z in range(Size)]
        for k in range(Size): #Draw the edge
            Board[0][k] = "X"
            Board[Size-1][k] = "X"
            Board[k][0] = "X"
            Board[k][Size-1] = "X"
        Chunk=[] #Store the chunks, each chunk stored in order of Top left corner, Top right corner, Bottom left corner, Bottom right corner in Grid format
        Chunk_num=0 #Number of chunks
        Chunk_num_F=0 #Number of chunks that are fully finished
        for n in range(0,4):
            if n == 0: #Top left corner of the chunk
                x=1
                y=Size-2
            elif n == 1: #Top right corner of the chunk
                x=Size-2
                y=Size-2
            elif n == 2: #Bottom left corner of the chunk
                x=1
                y=1
            elif n == 3: #Bottom right corner of the chunk
                x=Size-2
                y=1
            Chunk.append(grid(x,y)) #Storing the Location vector in Grid format
        Chunk_num=Chunk_num+1
        Done = False #Register maze is fully finished
        while not(Done): #Check is the maze finished
            Chunk_TL=Chunk[0] #Top left corner of the chunk, stored in Grid format
            Chunk_TR=Chunk[1] #Top right corner of the chunk, stored in Grid format
            Chunk_BL=Chunk[2] #Bottom left corner of the chunk, stored in Grid format
            Chunk_BR=Chunk[3] #Bottom right corner of the chunk, stored in Grid format
            x_TL=int(Chunk_TL[0:2]) #Converting Grid format to location vector (x), path
            y_TL=int(Chunk_TL[2:4]) #Converting Grid format to location vector (y), path
            x_TR=int(Chunk_TR[0:2])
            y_TR=int(Chunk_TR[2:4])
            x_BL=int(Chunk_BL[0:2])
            y_BL=int(Chunk_BL[2:4])
            x_BR=int(Chunk_BR[0:2])
            y_BR=int(Chunk_BR[2:4])
            if (x_TL == x_TR) or (y_TL == y_BL): #Check is the chunk is too small
                Chunk_num_F=Chunk_num_F+1 #Update the number of chunks that are fully finished
                for n in range (0,4):
                    Chunk.pop(0) #Remove the completed chunk
            else:
                x_Cut=random.randint(x_TL,x_TR) #Randomize the cut point on x-axis
                if x_Cut%2 != 0 : #Check is the cut point is path
                    if x_Cut == x_TR:
                        x_Cut=x_Cut-1 #Making sure the cut point is even(wall) and within the chunk
                    else:
                        x_Cut=x_Cut+1 #Making sure the cut point is even(wall)
                x=x_Cut
                for y in range(y_BL,y_TL+1):
                    Board[x][y]="X" #Cut the chunk vertically
                y_Cut=random.randint(y_BL,y_TL) #Randomize the cut point on y-axis
                if y_Cut%2 != 0 : #Check is the cut point is path
                    if y_Cut == y_TL:
                        y_Cut=y_Cut-1 #Making sure the cut point is even(wall) and within the chunk
                    else:
                        y_Cut=y_Cut+1 #Making sure the cut point is even(wall)
                y=y_Cut
                for x in range(x_TL,x_TR+1):
                    Board[x][y]="X" #Cut the chunk horizontally
                Third_Hole=random.randint(0,1) #Randomize which axis will have two holes
                if Third_Hole == 0: #X-axis has two holes, Y-axis has one holes
                    x=x_Cut #Cut point on x-axis, vertical wall
                    y=y_Cut #Cut point on y-axis, horizontal wall
                    Punched = False
                    while not(Punched):
                        x=random.randint(x_TL,x_Cut) #Randomlize the hole point, even number is wall, odd number is path
                        if x%2 == 0 : #Check is the hole point is wall
                            if x == x_Cut:
                                x=x-1 #Making sure the hole point is path and within the chunk
                            else:
                                x=x+1 #Making sure the hole point is path
                        if Board[x][y] != " ":
                            Punched = True #Making sure the hole is not at the same position as previous hole
                            Board[x][y]=" " #Making the hole in the wall
                    x=x_Cut #Cut point on x-axis, vertical wall
                    y=y_Cut #Cut point on y-axis, horizontal wall
                    Punched = False
                    while not(Punched):
                        x=random.randint(x_Cut,x_TR) #Randomlize the hole point, even number is wall, odd number is path
                        if x%2 == 0 : #Check is the hole point is wall
                            if x == x_Cut:
                                x=x+1 #Making sure the hole point is path and within the chunk
                            else:
                                x=x-1 #Making sure the hole point is path
                        if Board[x][y] != " ":
                            Punched = True #Making sure the hole is not at the same position as previous hole
                            Board[x][y]=" " #Making the hole in the wall
                    x=x_Cut #Cut point on x-axis, vertical wall
                    y=y_Cut #Cut point on y-axis, horizontal wall
                    Punched = False
                    while not(Punched):
                        y=random.randint(y_BL,y_TL) #Randomlize the hole point, even number is wall, odd number is path
                        if y%2 == 0 : #Check is the hole point is wall
                            if y == y_Cut:
                                y=y-1 #Making sure the hole point is path and within the chunk
                            else:
                                y=y+1 #Making sure the hole point is path
                        if Board[x][y] != " ":
                            Punched = True #Making sure the hole is not at the same position as previous hole
                            Board[x][y]=" " #Making the hole in the wall
                elif Third_Hole == 1: #X-axis has one holes, Y-axis has two holes
                    x=x_Cut #Cut point on x-axis, vertical wall
                    y=y_Cut #Cut point on y-axis, horizontal wall
                    Punched = False
                    while not(Punched):
                        x=random.randint(x_TL,x_TR) #Randomlize the hole point, even number is wall, odd number is path
                        if x%2 == 0 : #Check is the hole point is wall
                            if x == x_Cut:
                                x=x-1 #Making sure the hole point is path and within the chunk
                            else:
                                x=x+1 #Making sure the hole point is path
                        if Board[x][y] != " ":
                            Punched = True #Making sure the hole is not at the same position as previous hole
                            Board[x][y]=" " #Making the hole in the wall
                    x=x_Cut #Cut point on x-axis, vertical wall
                    y=y_Cut #Cut point on y-axis, horizontal wall
                    Punched = False
                    while not(Punched):
                        y=random.randint(y_BL,y_Cut) #Randomlize the hole point, even number is wall, odd number is path
                        if y%2 == 0 : #Check is the hole point is wall
                            if y == y_Cut:
                                y=y-1 #Making sure the hole point is path and within the chunk
                            else:
                                y=y+1 #Making sure the hole point is path
                        if Board[x][y] != " ":
                            Punched = True #Making sure the hole is not at the same position as previous hole
                            Board[x][y]=" " #Making the hole in the wall
                    x=x_Cut #Cut point on x-axis, vertical wall
                    y=y_Cut #Cut point on y-axis, horizontal wall
                    Punched = False
                    while not(Punched):
                        y=random.randint(y_Cut,y_TL) #Randomlize the hole point, even number is wall, odd number is path
                        if y%2 == 0 : #Check is the hole point is wall
                            if y == y_Cut:
                                y=y+1 #Making sure the hole point is path and within the chunk
                            else:
                                y=y-1 #Making sure the hole point is path
                        if Board[x][y] != " ":
                            Punched = True #Making sure the hole is not at the same position as previous hole
                            Board[x][y]=" " #Making the hole in the wall
                Chunk_TL_N=Chunk_TL #Update the top left corner of the chunk
                x_TR=x_Cut-1 #Update the top right corner of the chunk
                Chunk_TR_N=grid(x_TR,y_TR)
                y_BL=y_Cut+1 #Update the bottom left corner of the chunk
                Chunk_BL_N=grid(x_BL,y_BL)
                x_BR=x_Cut-1 #Update the bottom right corner of the chunk
                y_BR=y_Cut+1
                Chunk_BR_N=grid(x_BR,y_BR)
                Chunk[0]=Chunk_TL_N #Store the updated chunk
                Chunk[1]=Chunk_TR_N
                Chunk[2]=Chunk_BL_N
                Chunk[3]=Chunk_BR_N
                x_TL=int(Chunk_TL[0:2]) #Restore the chunk location vector from Grid format
                y_TL=int(Chunk_TL[2:4])
                x_TR=int(Chunk_TR[0:2])
                y_TR=int(Chunk_TR[2:4])
                x_BL=int(Chunk_BL[0:2])
                y_BL=int(Chunk_BL[2:4])
                x_BR=int(Chunk_BR[0:2])
                y_BR=int(Chunk_BR[2:4])
                x_TL=x_Cut+1 #Store the top left corner of the new chunk
                Chunk_TL_N=grid(x_TL,y_TL)
                Chunk_TR_N=Chunk_TR #Store the top right corner of the new chunk
                x_BL=x_Cut+1 #Store the bottom left corner of the new chunk
                y_BL=y_Cut+1
                Chunk_BL_N=grid(x_BL,y_BL)
                y_BR=y_Cut+1 #Store the bottom right corner of the new chunk
                Chunk_BR_N=grid(x_BR,y_BR)
                Chunk.append(Chunk_TL_N) #Store the new chunk
                Chunk.append(Chunk_TR_N)
                Chunk.append(Chunk_BL_N)
                Chunk.append(Chunk_BR_N)
                Chunk_num=Chunk_num+1 #Update the number of chunks
                x_TL=int(Chunk_TL[0:2]) #Restore the chunk location vector from Grid format
                y_TL=int(Chunk_TL[2:4])
                x_TR=int(Chunk_TR[0:2])
                y_TR=int(Chunk_TR[2:4])
                x_BL=int(Chunk_BL[0:2])
                y_BL=int(Chunk_BL[2:4])
                x_BR=int(Chunk_BR[0:2])
                y_BR=int(Chunk_BR[2:4])
                y_TL=y_Cut-1 #Store the top left corner of the new chunk
                Chunk_TL_N=grid(x_TL,y_TL)
                x_TR=x_Cut-1 #Store the top right corner of the new chunk
                y_TR=y_Cut-1
                Chunk_TR_N=grid(x_TR,y_TR)
                Chunk_BL_N=Chunk_BL #Store the bottom left corner of the new chunk
                x_BR=x_Cut-1 #Store the bottom right corner of the new chunk
                Chunk_BR_N=grid(x_BR,y_BR)
                Chunk.append(Chunk_TL_N) #Store the new chunk
                Chunk.append(Chunk_TR_N)
                Chunk.append(Chunk_BL_N)
                Chunk.append(Chunk_BR_N)
                Chunk_num=Chunk_num+1 #Update the number of chunks
                x_TL=int(Chunk_TL[0:2]) #Restore the chunk location vector from Grid format
                y_TL=int(Chunk_TL[2:4])
                x_TR=int(Chunk_TR[0:2])
                y_TR=int(Chunk_TR[2:4])
                x_BL=int(Chunk_BL[0:2])
                y_BL=int(Chunk_BL[2:4])
                x_BR=int(Chunk_BR[0:2])
                y_BR=int(Chunk_BR[2:4])
                x_TL=x_Cut+1 #Store the top left corner of the new chunk
                y_TL=y_Cut-1
                Chunk_TL_N=grid(x_TL,y_TL)
                y_TR=y_Cut-1 #Store the top right corner of the new chunk
                Chunk_TR_N=grid(x_TR,y_TR)
                x_BL=x_Cut+1 #Store the bottom left corner of the new chunk
                Chunk_BL_N=grid(x_BL,y_BL)
                Chunk_BR_N=Chunk_BR #Store the bottom right corner of the new chunk
                Chunk.append(Chunk_TL_N) #Store the new chunk
                Chunk.append(Chunk_TR_N)
                Chunk.append(Chunk_BL_N)
                Chunk.append(Chunk_BR_N)
                Chunk_num=Chunk_num+1 #Update the number of chunks
            if Chunk_num_F == Chunk_num: #Check is all chunk is finished
                Done=True
    Deploy() #Plot player and exit position
    if mode == 1:
        print("System: Maze 0"+mn+" loaded successfully")
        time.sleep(0.1)
    maze_solve()

def check_state(Maze,Not_Maze,Done): #Loop-erased random walk method debug function
    global temp_Maze
    global temp_Not_Maze
    global temp_Done
    temp_Maze=Maze
    temp_Not_Maze=Not_Maze
    temp_Done=Done
    
def print_state(): #Loop-erased random walk method debug function
    print("")
    print_board()
    print("")
    print("System: Printing maze state...")
    print("Maze:")
    for y in range(int((Size-1)/2)):
        print(*[temp_Maze[x][int((Size-1)/2)-y-1] for x in range(int((Size-1)/2))])
    print("Not Maze:"+ str(temp_Not_Maze))
    print("Done:", temp_Done)

def grid(x,y): #Convert Location vector to Grid format
    #Grid format: Location vector in "0519" form, x=5 y=19
    if x<10:
        temp="0"+str(x)
    else:
        temp=str(x)
    if y<10:
        temp=temp+"0"+str(y)
    else:
        temp=temp+str(y)
    return temp

def Deploy(): #Plot player and exit position
    global Size
    global board
    y=Size-1
    Plot=False
    while not(Plot): #Randomize the player position
        x=random.randint(1,(Size-1))
        if x%2 == 0 :
            x=(x%2)+(x//2)+1
            x=x*random.randint(1,2)
            if x%2 == 0 :
                x=x+1
        if not(x >= Size):
            if Board[x-1][y-1] == "X" or Board[x+1][y-1] == "X": #Making sure the player is start at the end of the path
                Plot=True
    Board[x][y]="P" #Player starting point
    y=0
    Plot=False
    while not(Plot): #Randomize the exit position
        x=random.randint(1,(Size-1))
        if x%2 == 0 :
            x=(x%2)+(x//2)+1
            x=x*random.randint(1,2)
            if x%2 == 0 :
                x=x+1
        if not(x >= Size):
            if Board[x-1][y+1] == "X" or Board[x+1][y+1] == "X": #Making sure the exit is at the end of the path
                Plot=True
    Board[x][y]="E" #Exit point

def player_found(): #Automated relocate player position
    global Board
    global Size
    found=False #Register did the player position found
    x=0
    y=0
    try_n=0
    while found != True: #Automated relocate player position
        if Board[x][y] == "P":
            found=True
        else:
            y=y+1
            if y > (Size-1):
                x=x+1
                y=0
                if x > (Size-1):
                    if try_n != 3:
                        x=0
                        y=0
                        try_n=try_n+1
                    else:
                        print("System: ERROR")
                        print("System: Player position not found, please restart the game")
                        input("System: Press Enter to exit the game ")
                        sys.exit()
    coordinate=grid(x,y)
    return coordinate #Return player coordinate in Grid fromat

def maze_solve():
    global Board
    global Size
    global Difficulty
    global rec_step
    global mode
    global cycle
    global steps
    global timer
    global Minutes
    global Second
    retry_cycle=0
    passed = False
    if mode == 1:
        print("System: Calculating recommended steps...")
    while not (passed):
        rec_step=0
        Method=1
        if Method == 1: #Depth-First Search(DFS)
            Path=[] #Store the walked path in grid format
            Junctions=[] #Store the junctions in grid format
            Junction3=[] #Store the junctions that got 3 exit in grid format
            reach=False #Register did the exit reached
            temp=player_found() #Found player location
            x=int(temp[0:2])
            y=int(temp[2:4])
            y=y-1
            rec_step=rec_step+1
            Board[x][y]="0"
            Path.append(grid(x,y))
            while not(reach): #Check is the exit reached
                exit_way=[] #Direction of walkable path
                exit_num=0 #Number of walkable path
                direction=None #Direction of walk
                if Board[x][y-1] == "E": #Check is the bottom box the exit
                    rec_step=rec_step+1
                    reach=True
                elif Board[x][y-1] == " ": #Check is the bottom box the path
                    exit_num=exit_num+1
                    exit_way.append("down")
                if Board[x-1][y] == " ": #Check is the left box the path
                    exit_num=exit_num+1
                    exit_way.append("left")
                if Board[x][y+1] == " ": #Check is the top box the path
                    exit_num=exit_num+1
                    exit_way.append("up")
                if Board[x+1][y] == " ": #Check is the right box the path
                    exit_num=exit_num+1
                    exit_way.append("right")
                if exit_num == 1: #One-way path
                    direction=0
                elif exit_num == 2: #2-way junction
                    Junctions.append(grid(x,y))
                    direction=random.randint(0,1) #Random choose a way to walk
                elif exit_num == 3: #3-way junction
                    Junctions.append(grid(x,y))
                    Junction3.append(grid(x,y))
                    direction=random.randint(0,2) #Random choose a way to walk
                if reach != True:
                    if direction != None: #Move
                        if exit_way[direction] == "up": #Walk up
                            y=y+1
                            rec_step=rec_step+1
                            Board[x][y]="0"
                            Path.append(grid(x,y))
                        elif exit_way[direction] == "down": #Walk down
                            y=y-1
                            rec_step=rec_step+1
                            Board[x][y]="0"
                            Path.append(grid(x,y))
                        elif exit_way[direction] == "left": #Walk left
                            x=x-1
                            rec_step=rec_step+1
                            Board[x][y]="0"
                            Path.append(grid(x,y))
                        elif exit_way[direction] == "right": #Walk right
                            x=x+1
                            rec_step=rec_step+1
                            Board[x][y]="0"
                            Path.append(grid(x,y))
                    elif (direction == None) and (exit_num == 0): #Dead end
                        back=False
                        while not(back): #Check did it arrive at the previous junction
                            Board[x][y]="/"
                            Path.pop()
                            rec_step=rec_step-1
                            temp=Path[len(Path)-1] #Move back
                            x=int(temp[0:2])
                            y=int(temp[2:4])
                            if len(Junction3) != 0: #Check is there any 3-way junction
                                if temp == Junction3[len(Junction3)-1]: #Check is it at the 3-way junction
                                    Junction3.pop()
                                    back=True
                            if back != True:
                                if temp == Junctions[len(Junctions)-1]: #Check is it at the junction
                                    Junctions.pop()
                                    back=True
            x=1
            y=0
            while (x != Size-2) or (y != Size-2): #Cleaning up the board
                if y+1 == Size-1: #Check did it reach the top
                    y=1
                    x=x+1
                else:
                    y=y+1
                if Board[x][y] != "X": #Replace the path
                    Board[x][y]=" "
        elif Method == 2: #Breadth-First Search(BFS)
            None
        elif Method == 3: #A* Search
            None
        min_step=Size*Size*0.1 #Minimum steps to solve the maze depend on size
        if rec_step <= min_step: #Make sure the recommended steps is not too low
            for k in range(Size): #Redraw the top and bottom edge
                Board[k][0] = "X"
                Board[k][Size-1] = "X"
            Deploy()
            retry_cycle=retry_cycle+1
            if retry_cycle == 3: #Maximum number of retry
                build_maze() #Restart the maze generation if it exceed the maximum number of retry
        else:
            passed=True
    rec_step=rec_step+10 #Add some buffer to the recommended steps
    #quick_test() #Test
    cycle=cycle+1
    if cycle == 1:
        steps=0
        Minutes=0 #Timer minutes reset
        Second=0 #Timer second reset
        if mode == 1:
            print("System: Recommend steps for this maze:", rec_step)
            time.sleep(0.1)
            if Difficulty == 5:
                input("System: Press Enter to start ")
            timer.start()
            game()
        elif mode == 2:
            game_setup()
        else:
            print("System: ERROR")
            print("System: User interface not recognised, please restart the game")
            input("System: Press Enter to exit the game ")
            sys.exit()

def quick_test(): #Test
    global Board
    temp=player_found() #Found player location
    x=int(temp[0:2])
    y=int(temp[2:4])
    y=y-1
    Board[x][y]="E"

def Timer(): #10 minutes timer (Main thread/Sub-thread)
    global Minutes
    global Second
    global mode
    global screen
    global Time_up #Register time is up
    global Timer_stop #Register timer stop
    global Max_Minute #Maximum time minutes allowed in hardcore mode
    global Max_Second #Maximum time seconds allowed in hardcore mode
    Max_Minute=3
    Max_Second=0
    Timer_stop=False
    Time_up=False
    if mode == 1:
        time.sleep(1)
        tick()
    elif mode == 2:
        screen.ontimer(tick,1000)

def tick():
    global Minutes
    global Second
    global Difficulty
    global mode
    global screen
    global Time_up #Register time is up
    global Timer_stop #Register timer stop
    global Max_Minute #Maximum time minutes allowed in hardcore mode
    global Max_Second #Maximum time seconds allowed in hardcore mode
    Second=Second+1
    if Second == 60:
        Minutes=Minutes+1
        Second=0
    if Difficulty == 5:
        if (Minutes == Max_Minute) and (Second == Max_Second):
            Timer_stop=True
            Time_up=True
            if mode == 1:
                print("\nSystem: Times up")
            end(False)
    if not(Timer_stop):
        if mode == 1:
            time.sleep(1)
            tick()
        elif mode == 2:
            timer_upd()
            screen.ontimer(tick, 1000) #Call tick function every second

def Menu_CLI(): #CLI menu
    global root
    global Size
    global Board
    global Type_error
    global Difficulty
    global mode
    print("System: This game is for single players")
    time.sleep(1)
    print("System: The icon 'X' represent the wall, and icon ' ' represent the path")
    time .sleep(1)
    print("System: Icon 'P' is the player, and icon 'E' is the exit")
    time.sleep(1)
    print("System: You can move in four directions")
    time.sleep(1)
    print("System: Up(W), Down(S), Left(A), Right(D)")
    time.sleep(1)
    print("System: Single character is entered everytime")
    time.sleep(1)
    print("System: Press Enter to execute the action")
    time.sleep(1)
    print("System: Every steps you take will be recorded")
    time.sleep(1)
    print("System: Your goal is to exit the maze with shortest time")
    time.sleep(1)
    print("System: In Hardcore Mode your steps and time was limmited, think carefully before moving")
    time.sleep(1)
    print("System: You are not allow to use more steps and time than the system recommended in Hardcore Mode")
    time.sleep(1)
    ans=input("System: Press Enter to start the game or enter /GUI to switch to GUI manu")
    if ans.lower() == "/gui":
        root.deiconify() #Restores the turtle screen window
        mode=2
        menu_setup() #Switch to graphical user interface
    else:
        Type_error=False
        while not Type_error:
            try:
                ans=int(input("System: Please enter difficulty: 1(21*21 Board), 2(31*31 Board), 3(41*41 Board), 4(51*51 Board), 5(Hardcore Mode) "))
                if ans <=0 or ans > 5:
                    print("System: Out of bounds")
                else:
                    Type_error=True
                    Difficulty=ans
            except:
                print("System: Formet error")
        Type_error=False
        print("System: Good luck!")
        time.sleep(0.5)
        build_maze()

def menu_setup(): #GUI screen setup
    global screen
    global pen
    try:
        screen.clear() #Test do the screen still exist
    except:
        screen=t.Screen()
    screen.title("Maze Game")
    screen.bgcolor("White")
    screen.setup(width=550, height=650)
    screen.tracer(0)
    pen=t.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.shapesize(1,1)
    screen.update()
    def_set() #Setting options set to default
    if Pyg: #Pygame was imported
        volume_set() #Set audio volume
    Menu_GUI()

def Menu_GUI(): #GUI main menu
    global screen
    global page
    global pen
    global Instruction_bt
    global Start_bt
    global Setting_bt
    global Exit_bt
    global CLI_bt
    page=0 #Menu id
    pen.penup()
    pen.clear() #Clear the board
    pen.goto(0,200)
    pen.write("Maze Game", align="center", font=("Arial", 50, "bold")) #Game title
    Play_anime()
    style="Arial", 25, "bold"
    Instruction_bt=Button(-100,125,200,50,"Instruction",style)
    Instruction_bt.draw() #Draw instruction button
    Start_bt=Button(-100,25,200,50,"Start",style)
    Start_bt.draw() #Draw start button
    Setting_bt=Button(-100,-75,200,50,"Setting",style)
    Setting_bt.draw() #Draw setting button
    Exit_bt=Button(-250,-250,100,50,"Exit",style)
    Exit_bt.draw() #Draw exit button
    CLI_bt=Button(150,-250,100,50,"CLI",style)
    CLI_bt.draw() #Draw CLI button
    screen.update()
    screen.onclick(button_click)
    screen.listen()
    screen.mainloop() #Keep the window open

def button_click(x,y): #Mouse clicked
    global root
    global screen
    global page
    global Difficulty
    global mode
    global Size
    global Instruction_bt #Instruction button
    global Start_bt #Start button
    global Setting_bt #Setting button
    global Exit_bt #Exit button
    global Return_bt #Return button
    global CLI_bt #CLI button
    global Difficulty_set #Difficulty option set
    global Restart_bt #Restart button
    global cycle
    global Timer_stop #Register timer stop
    global Pause_bt #Pause button
    global Resume_bt #Resume button
    global Menu_bt #Back to main menu button
    global Paused #Register did game paused
    global PShape_set #Player shape option set
    global PShape #Player shape
    global PColour_set #Player colour option set
    global PColour #Player colour
    global Animation_set #Animation option set
    global Animation #Animation
    global AVolume_set #Audio volume option set
    global AVolume #Audio volume
    global Apply_bt #Apply button
    global Reset_bt #Reset button
    global RAM #Temporary setting
    screen.update()
    if page == 0: #From menu
        if Instruction_bt.get_x_min() < x < Instruction_bt.get_x_max() and Instruction_bt.get_y_min() < y < Instruction_bt.get_y_max(): #Instruction button pressed
            play_sound(1) #Play sound effect
            instruction()
        elif Start_bt.get_x_min() < x < Start_bt.get_x_max() and Start_bt.get_y_min() < y < Start_bt.get_y_max(): #Start button pressed
            play_sound(1) #Play sound effect
            Difficulty=1
            game_setting()
        elif Setting_bt.get_x_min() < x < Setting_bt.get_x_max() and Setting_bt.get_y_min() < y < Setting_bt.get_y_max(): #Setting button pressed
            play_sound(1) #Play sound effect
            RAM=[PShape,PColour,Animation,AVolume] #Store the currtent setting
            setting()
        elif Exit_bt.get_x_min() < x < Exit_bt.get_x_max() and Exit_bt.get_y_min() < y < Exit_bt.get_y_max(): #Exit button pressed
            play_sound(1) #Play sound effect
            screen.bye()
            sys.exit()
        elif CLI_bt.get_x_min() < x < CLI_bt.get_x_max() and CLI_bt.get_y_min() < y < CLI_bt.get_y_max(): #CLI button pressed
            play_sound(1) #Play sound effect
            screen.clear()
            root.iconify() #Minimizes the turtle screen window
            mode=1
            Menu_CLI() #Switch to command line interface
    elif page == 1: #From instruction
        if Return_bt.get_x_min() < x < Return_bt.get_x_max() and Return_bt.get_y_min() < y < Return_bt.get_y_max(): #Return button pressed
            play_sound(1) #Play sound effect
            Menu_GUI()
    elif page == 2: #From game_setting
        if Return_bt.get_x_min() < x < Return_bt.get_x_max() and Return_bt.get_y_min() < y < Return_bt.get_y_max(): #Return button pressed
            play_sound(1) #Play sound effect
            Menu_GUI()
        elif Difficulty_set.get_btL_x_min() < x < Difficulty_set.get_btL_x_max() and Difficulty_set.get_btL_y_min() < y < Difficulty_set.get_btL_y_max(): #Difficulty option set left arrow button pressed
            play_sound(1) #Play sound effect
            if Difficulty > 1: #Decrease difficulty
                Difficulty=Difficulty-1
                game_setting()
        elif Difficulty_set.get_btR_x_min() < x < Difficulty_set.get_btR_x_max() and Difficulty_set.get_btR_y_min() < y < Difficulty_set.get_btR_y_max(): #Difficulty option set right arrow button pressed
            play_sound(1) #Play sound effect
            if Difficulty < 5: #Increase difficulty
                Difficulty=Difficulty+1
                game_setting()
        elif Start_bt.get_x_min() < x < Start_bt.get_x_max() and Start_bt.get_y_min() < y < Start_bt.get_y_max(): #Start button pressed
            play_sound(1) #Play sound effect
            build_maze()
    elif page == 3: #From setting
        if Return_bt.get_x_min() < x < Return_bt.get_x_max() and Return_bt.get_y_min() < y < Return_bt.get_y_max(): #Return button pressed
            play_sound(1) #Play sound effect
            if Paused: #Go back to pause menu when game paused
                pause_game()
            else: #Go back to main menu
                Menu_GUI()
        elif PShape_set.get_btL_x_min() < x < PShape_set.get_btL_x_max() and PShape_set.get_btL_y_min() < y < PShape_set.get_btL_y_max(): #Player shape option set left arrow button pressed
            play_sound(1) #Play sound effect
            if RAM[0] > 1: #Change player shape
                RAM[0]=RAM[0]-1 #Update temporary setting
                setting()
        elif PShape_set.get_btR_x_min() < x < PShape_set.get_btR_x_max() and PShape_set.get_btR_y_min() < y < PShape_set.get_btR_y_max(): #Player shape option set right arrow button pressed
            play_sound(1) #Play sound effect
            if RAM[0] < PShape_set.get_text_list_length(): #Change player shape
                RAM[0]=RAM[0]+1 #Update temporary setting
                setting()
        elif PColour_set.get_btL_x_min() < x < PColour_set.get_btL_x_max() and PColour_set.get_btL_y_min() < y < PColour_set.get_btL_y_max(): #Player colour option set left arrow button pressed
            play_sound(1) #Play sound effect
            if RAM[1] > 1: #Change player colour
                RAM[1]=RAM[1]-1 #Update temporary setting 
                setting()
        elif PColour_set.get_btR_x_min() < x < PColour_set.get_btR_x_max() and PColour_set.get_btR_y_min() < y < PColour_set.get_btR_y_max(): #Player colour option set right arrow button pressed
            play_sound(1) #Play sound effect
            if RAM[1] < PColour_set.get_text_list_length(): #Change player colour
                RAM[1]=RAM[1]+1 #Update temporary setting
                setting()
        elif Animation_set.get_btL_x_min() < x < Animation_set.get_btL_x_max() and Animation_set.get_btL_y_min() < y < Animation_set.get_btL_y_max(): #Animation option set left arrow button pressed
            play_sound(1) #Play sound effect
            if RAM[2] == 2: #Turn animation on
                RAM[2]=1 #Update temporary setting
                setting()
        elif Animation_set.get_btR_x_min() < x < Animation_set.get_btR_x_max() and Animation_set.get_btR_y_min() < y < Animation_set.get_btR_y_max(): #Animation option set right arrow button pressed
            play_sound(1) #Play sound effec
            if RAM[2] == 1: #Turn animation off
                RAM[2]=2 #Update temporary setting 
                setting()
        elif Pyg: #Pygame was imported
            if AVolume_set.get_btL_x_min() < x < AVolume_set.get_btL_x_max() and AVolume_set.get_btL_y_min() < y < AVolume_set.get_btL_y_max(): #Audio volume option set left arrow button pressed
                play_sound(1) #Play sound effect
                if temp > 1: #Change audio volume
                    RAM[3]=RAM[3]-1 #Update temporary setting 
                    setting()
            elif AVolume_set.get_btR_x_min() < x < AVolume_set.get_btR_x_max() and AVolume_set.get_btR_y_min() < y < AVolume_set.get_btR_y_max(): #Audio volume option set right arrow button pressed
                play_sound(1) #Play sound effect
                if RAM[3] < AVolume_set.get_text_list_length(): #Change audio volume
                    RAM[3]=RAM[3]+1 #Update temporary setting
                    setting()
        elif Apply_bt.get_x_min() < x < Apply_bt.get_x_max() and Apply_bt.get_y_min() < y < Apply_bt.get_y_max(): #Apply button pressed
            play_sound(1) #Play sound effect
            PShape=RAM[0] #Apply setting
            PColour=RAM[1]
            Animation=RAM[2]
            if Pyg: #Pygame was imported
                AVolume=RAM[3]
                volume_set() #Apply audio volume setting
        elif Reset_bt.get_x_min() < x < Reset_bt.get_x_max() and Reset_bt.get_y_min() < y < Reset_bt.get_y_max(): #Reset button pressed
            play_sound(1) #Play sound effect
            def_set() #Reset setting options back to default
            RAM=[PShape,PColour,Animation,AVolume] #Update the current setting
            setting()
    elif page == 4: #From in-game menu
        if Pause_bt.get_x_min() < x < Pause_bt.get_x_max() and Pause_bt.get_y_min() < y < Pause_bt.get_y_max(): #Pause button pressed
            play_sound(1) #Play sound effect
            pause_game()
    elif page == 5: #From end menu
        if Exit_bt.get_x_min() < x < Exit_bt.get_x_max() and Exit_bt.get_y_min() < y < Exit_bt.get_y_max(): #Exit button pressed
            play_sound(1) #Play sound effect
            screen.bye()
            sys.exit()
        elif Restart_bt.get_x_min() < x < Restart_bt.get_x_max() and Restart_bt.get_y_min() < y < Restart_bt.get_y_max(): #Restart button pressed
            play_sound(1) #Play sound effect
            screen.reset()
            screen.ontimer(main,10) #Delay buffer
    elif page == 6: #From game pause menu
        if Resume_bt.get_x_min() < x < Resume_bt.get_x_max() and Resume_bt.get_y_min() < y < Resume_bt.get_y_max(): #Resume button pressed
            play_sound(1) #Play sound effect
            game_setup()
        elif Setting_bt.get_x_min() < x < Setting_bt.get_x_max() and Setting_bt.get_y_min() < y < Setting_bt.get_y_max(): #Setting button pressed
            play_sound(1) #Play sound effect
            RAM=[PShape,PColour,Animation,AVolume] #Store the currtent setting
            setting()
        elif Menu_bt.get_x_min() < x < Menu_bt.get_x_max() and Menu_bt.get_y_min() < y < Menu_bt.get_y_max(): #Back to main menu button pressed
            play_sound(1) #Play sound effect
            screen.reset()
            screen.ontimer(main,10) #Delay buffer
        elif Exit_bt.get_x_min() < x < Exit_bt.get_x_max() and Exit_bt.get_y_min() < y < Exit_bt.get_y_max(): #Exit button pressed
            play_sound(1) #Play sound effect
            screen.bye()
            sys.exit()

def instruction(): #GUI instruction
    global screen
    global page
    global pen
    global Return_bt
    page=1
    pen.clear() #Clear screen
    style="Arial", 15, "bold"
    y=275 #Fist row
    pen.goto(0,y)
    pen.write("- This game is for single players -", align="center", font=(style))
    Play_anime()
    y=y-50 #Second row
    pen.goto(0,y)
    pen.write("- The green curser is the player -", align="center", font=(style))
    Play_anime()
    y=y-50 #Third row
    pen.goto(0,y)
    pen.write("- And red box is the exit -", align="center", font=(style))
    Play_anime()
    y=y-50 #Fourth row
    pen.goto(0,y)
    pen.write("- You can move in four directions -", align="center", font=(style))
    Play_anime()
    y=y-50 #Fifth row
    pen.goto(0,y)
    pen.write("- Up(W), Down(S), Left(A), Right(D) -", align="center", font=(style))
    Play_anime()
    y=y-50 #Sixth row
    pen.goto(0,y)
    pen.write("- Every steps you take will be recorded -", align="center", font=(style))
    Play_anime()
    y=y-50 #Seventh row
    pen.goto(0,y)
    pen.write("- Your goal is to exit the maze with shortest time -", align="center", font=(style))
    Play_anime()
    y=y-50 #Eighth row
    pen.goto(0,y)
    pen.write("- In Hardcore Mode your steps and time was limmited -", align="center", font=(style))
    Play_anime()
    y=y-50 #Nineth row
    pen.goto(0,y)
    pen.write("- Think carefully before moving -", align="center", font=(style))
    Play_anime()
    y=y-50 #Tenth row
    pen.goto(0,y)
    pen.write("- You are not allow to use more steps and time than", align="center", font=(style))
    Play_anime()
    y=y-50 #Eleventh row
    pen.goto(0,y)
    pen.write("the system recommended in Hardcore Mode -", align="center", font=(style))
    Play_anime()
    style="Arial", 25, "bold"
    Return_bt=Button(-250,-250,125,50,"Return",style)
    Return_bt.draw() #Draw return button
    screen.update()
    screen.onclick(button_click)
    screen.listen()

def game_setting(): #GUI game setting
    global screen
    global page
    global pen
    global Difficulty
    global Difficulty_set
    global Start_bt
    global Return_bt
    page=2
    pen.clear() #Clear screen
    style="Arial", 25, "bold"
    try:
        Difficulty_set.set_n(Difficulty) #Update difficulty
    except:
        x=-170 #Difficulty text position
        y=25
        options=["1(21*21 Board)","2(31*31 Board)","3(41*41 Board)","4(51*51 Board)","5(Hardcore Mode)"] #Available difficulty
        Difficulty_set=Option_set(x, y, style, "Difficulty:", options, Difficulty)
    Difficulty_set.draw() #Draw difficulty option set
    Start_bt=Button(-50,-100,100,50,"Start",style)
    Start_bt.draw() #Draw start button
    Return_bt=Button(-250,-250,125,50,"Return",style)
    Return_bt.draw() #Draw return button
    screen.update()
    screen.onclick(button_click)
    screen.listen()

def load_audio(): #Load in all audio
    global BtCl_SoundEffect
    error=False
    audio=""
    try: #Try to load audio track
        BtCl_SoundEffect=mixer.Sound(r"Audio_pack\Button_Click.mp3")
    except: #Failed to load in
        error=True
        audio=audio+"Button_Click.mp3"+", "
    if error: #Error message
        print("System: ERROR")
        print("System: Failed to load "+audio[0:len(audio)-2])
        print("System: Please make sure full audio package was installed")
        input("System: Press Enter to exit the game ")

def volume_set(): #Audio volume set
    global AVolume
    global BtCl_SoundEffect #Button click sound effect
    volume=AVolume/100
    BtCl_SoundEffect.set_volume(volume)

def play_sound(i): #Play sound
    global BtCl_SoundEffect #Button click sound effect
    if Pyg: #Pygame was imported
        if i == 1: #ID one
            BtCl_SoundEffect.play()

def def_set(): #Setting default
    global PShape
    global PColour
    global Animation
    global AVolume
    PShape=1 #Classic
    PColour=1 #Green
    Animation=1 #On
    AVolume=3 #50

def setting(): #GUI setting
    global screen
    global page
    global pen
    global Return_bt
    global Apply_bt
    global Reset_bt
    global RAM
    global PShape_set
    global PColour_set
    global Animation_set
    global AVolume_set
    page=3
    pen.clear() #Clear screen
    PShape=RAM[0] #Load in temporary setting
    PColour=RAM[1]
    Animation=RAM[2]
    AVolume=RAM[3]
    style="Arial", 25, "bold"
    try:
        PShape_set.set_n(PShape) #Update player shape
    except:
        x=-100 #Player shape set position
        y=250 #Player shape section row
        options=["Classic","Turtle","Arrow","Circle","Square","Triangle"] #Available player shape
        PShape_set=Option_set(x, y, style, "Player Shape:  ", options,PShape)
    PShape_set.draw() #Draw player shape option set
    try:
        Colour_set.set_n(PColour) #Update player colour
    except:
        x=-75 #Player colour set position
        y=175 #Player colour section row
        options=["Green","Red","Blue","Yellow","White","Black"] #Available player colour
        PColour_set=Option_set(x, y, style, "Player Colour:  ", options,PColour)
    PColour_set.draw() #Draw player colour option set
    try:
        Animation_set.set_n(Animation) #Update animation
    except:
        x=-50 #Animation set position
        y=100 #Animation section row
        options=["On", "Off"] #Available option
        Animation_set=Option_set(x, y, style, "Animation:  ", options,Animation)
    Animation_set.draw() #Draw animation option set
    if Pyg: #Pygame was imported
        try:
            AVolume_set.set_n(AVolume) #Update audio volume
        except:
            x=-50 #Audio volume set position
            y=25 #Audio volume section row
            options=["0","25", "50", "75", "100"] #Available option
            AVolume_set=Option_set(x, y, style, "Volume:  ", options,AVolume)
        AVolume_set.draw() #Draw audio volume option set
    Apply_bt=Button(-112.5,-100,100,50,"Apply",style)
    Apply_bt.draw() #Draw apply button
    Reset_bt=Button(12.5,-100,100,50,"Reset",style)
    Reset_bt.draw() #Draw reset button
    Return_bt=Button(-250,-250,125,50,"Return",style)
    Return_bt.draw() #Draw return button
    screen.update()
    screen.onclick(button_click)
    screen.listen()

def game_setup(): #Game GUI setup
    global screen
    global Size
    global Ratio
    global page
    global player
    global system
    global step_pn
    global timer_pn
    global menu_width
    global Minutes
    global Second
    global PShape_set
    global PShape
    global PColour_set
    global PColour
    page=4
    screen.clear() #Clear screen
    Ratio=min(screen.cv.winfo_screenwidth()/Size,screen.cv.winfo_screenheight()/Size)*0.85 #Set screen size using monitor resolution
    menu_width=Size*Ratio/4 #In game menu width
    screen.setup(width=Size*Ratio+0.25*Ratio+menu_width, height=Size*Ratio+0.25*Ratio)
    screen.tracer(0)
    screen.update()
    pen.clear() #GUI drawing
    pen.shapesize((Ratio/20), (Ratio/20))
    pen.color("black")
    pen.hideturtle()
    pen.penup()
    pen.goto((Ratio/4),0) #Center
    player=t.Turtle() #Player character
    player.shapesize((Ratio/20), (Ratio/20))
    player.penup()
    try: #Set player shape
        player.shape(PShape_set.get_text_list_nth_item(PShape))
        if PShape != 1: #Size adjust
            player.shapesize((Ratio/30), (Ratio/30))
    except: #If user didn't open setting
        player.shape("classic")
    try: #Set player colour
        player.fillcolor(PColour_set.get_text_list_nth_item(PColour))
    except: #If user didn't open setting
        player.fillcolor("green")
    player.goto((Ratio/4),0)
    player.hideturtle()
    system=t.Turtle() #Output massage
    system.shapesize(1,1)
    system.penup()
    system.color("red")
    system.goto(0,0)
    system.hideturtle()
    step_pn=t.Turtle() #Steps count
    step_pn.shapesize(1,1)
    step_pn.penup()
    step_pn.color("black")
    step_pn.hideturtle()
    timer_pn=t.Turtle() #Timer count
    timer_pn.shapesize(1,1)
    timer_pn.penup()
    timer_pn.color("black")
    timer_pn.hideturtle()
    screen.update()
    draw_maze()

def draw_maze():
    global Board
    global pen
    global screen
    global Size
    global Ratio
    global player
    global menu_width
    i=0
    j=Size-1 #Board top left corner
    #Maze bottom-left corner setted
    maze_x0=-screen.window_width()/2-Ratio/1.25+menu_width
    maze_y0=-screen.window_height()/2+Ratio/1.25
    while (i < Size) and (j != -1):
        #Convert Board[i][j] location vecter to Screen x,y
        x=maze_x0+i*Ratio+Ratio/2
        y=maze_y0+j*Ratio+Ratio/2
        if Board[i][j] == "X": #Draw wall
            wall_block(x,y,"black")
        elif Board[i][j] == "E": #Draw exit
            wall_block(x,y,"red")
        elif Board[i][j] == "P": #Draw player start
            wall_block(x,y,"blue")
            player.goto(x+Ratio/2,y-Ratio/2)
            player.setheading(270)
        i=i+1
        if i == Size:
            i=0
            j=j-1
    player.showturtle()
    screen.update()
    draw_menu()

def draw_menu():
    global step_pn
    global timer_pn
    global pen
    global screen
    global Ratio
    global menu_width
    global mn
    global rec_step
    global steps
    global Pause_bt
    global Minutes
    global Second
    menu_x0=-screen.window_width()/2
    margin=screen.window_height()*0.05
    menu_height=screen.window_height()-(margin*2) #Menu available height
    bounds=menu_width*0.05
    menu_width=menu_width-bounds*2 #Menu available width
    items=5 #Maze ID, Recommend steps, Steps, Timer, Return button
    item_height=menu_height/(items+1) #Items height
    spacing=menu_height/(items+1)/(items-1) #Distance between items
    style="Arial", int(item_height*0.17), "bold" #Set text format
    text_font, text_size, text_weight=style #Unpack text style
    menu_center=menu_x0+menu_width/2+bounds #Menu horizontal center x coordinate
    y=screen.window_height()/2-margin/2-item_height/2 #First item y coordinate
    pen.goto(menu_center,y)
    text="Maze 0"+mn
    pen.write(text, align="center", font=(style))
    y=y-item_height/2-spacing-item_height/2+text_size*0.75 #Second item y coordinate
    pen.goto(menu_center,y)
    text="Recommend"
    pen.write(text, align="center", font=(style)) #Write first row
    y=y-text_size*2.25 #Second row y coordinate
    pen.goto(menu_center,y)
    text="steps: "+ str(rec_step)
    pen.write(text, align="center", font=(style)) #Write second row
    y=y-item_height/2-spacing-item_height/2+text_size*2.25 #Third item y coordinate
    step_pn.goto(menu_center,y)
    text="Steps: "+ str(steps)
    step_pn.write(text, align="center", font=(style))
    y=y-item_height/2-spacing-item_height/2 #Fourth item y coordinate
    timer_pn.goto(menu_center,y)
    temp=grid(Minutes,Second)
    text="Timer: "+temp[0:2]+":"+temp[2:4] #Concast minutes and seconds to timer format
    timer_pn.write(text, align="center", font=("Arial", text_size, "bold"))
    y=y-item_height/2-spacing #Fifth item y coordinate
    text="Pause"
    y=y-item_height/2+text_size*1.5 #Button top side y coordinate
    height=text_size*3 #Button height
    width=len(text)*1.5*text_size #Button width
    Pause_bt=Button(menu_x0+bounds/2+(menu_width-width)/2,y,width,height,text,style)
    Pause_bt.draw() #Draw Pause button
    screen.update()
    ready()

def ready(): #Ready to start the game
    global screen
    global system
    global Ratio
    global steps
    global Paused #Register did game paused
    style="Arial", int(25/min(screen.cv.winfo_screenwidth()/Size,screen.cv.winfo_screenheight()/Size)*Ratio*1.5), "bold"
    if not(Paused):
        text="Press Enter to start"
    elif Paused:
        text="Press Enter to resume"
    system.write(text, align="center", font=(style))
    screen.bgcolor("black")
    screen.update()
    screen.onkeypress(Start,"Return")
    screen.listen()
    screen.mainloop() #Keep the window open

def Start(): #Start the game
    global screen
    global system
    global cooldown
    system.clear()
    cooldown=False
    screen.bgcolor("white")
    screen.update()
    screen.onkeypress(None,"Return")
    movement_blind() #Set movement
    screen.onclick(button_click)
    screen.listen()
    Timer() #Start timer

def pause_game(): #Pause the game:
    global screen
    global pen
    global player
    global page
    global Timer_stop
    global Resume_bt #Resume button
    global Setting_bt #Setting button
    global Menu_bt #Back to main menu button
    global Exit_bt #Exit button
    global Paused #Register did game paused
    global Second
    Timer_stop=True
    Paused=True
    Second=Second-1 #Adjust timer
    page=6
    screen.clear()
    screen.setup(width=550, height=650)
    screen.tracer(0)
    screen.update()
    pen.penup() #Debug TKinter
    pen.goto(0,10)
    pen.pendown()
    pen.goto(0,-10)
    pen.penup()
    pen.clear() #Debug TKinter
    pen.shapesize(1,1)
    pen.goto(0,200)
    pen.write("Game Paused", align="center", font=("Arial", 50, "bold")) #Game state
    Play_anime()
    style="Arial", 25, "bold"
    Resume_bt=Button(-100,125,200,50,"Resume",style)
    Resume_bt.draw() #Draw resume button
    Setting_bt=Button(-100,25,200,50,"Setting",style)
    Setting_bt.draw() #Draw setting button
    Menu_bt=Button(-100,-75,200,50,"Main menu",style)
    Menu_bt.draw() #Draw Back to main menu button
    Exit_bt=Button(-100,-175,200,50,"Exit",style)
    Exit_bt.draw() #Draw exit button
    screen.update()
    screen.onclick(button_click)
    movement_unblind()

def steps_upd(): #Update steps count
    global step_pn
    global steps
    global screen
    global Pause_bt
    step_pn.clear()
    text="Steps: "+str(steps)
    step_pn.write(text, align="center", font=("Arial", Pause_bt.get_text_size(), "bold"))
    screen.update()

def timer_upd(): #Update timer count
    global timer_pn
    global Minutes
    global Second
    global Screen
    global Pause_bt
    global Max_Minute #Maximum time minutes allowed in hardcore mode
    global Max_Second #Maximum time seconds allowed in hardcore mode
    global Difficulty
    timer_pn.clear()
    if Difficulty == 5: #Convert to countdown
        minu=Max_Minute-Minutes-1
        seco=60-Second
        temp=grid(minu,seco)
    else:
        temp=grid(Minutes,Second)
    text="Timer: "+temp[0:2]+":"+temp[2:4] #Concast minutes and seconds to timer format
    timer_pn.write(text, align="center", font=("Arial", Pause_bt.get_text_size(), "bold"))
    screen.update()

def wall_block(x,y,color):
    global pen
    global screen
    global Ratio
    global Animation
    pen.color(color)
    pen.goto(x,y) #Top left
    pen.pendown()
    pen.begin_fill()
    pen.goto(x+Ratio,y) #Top right
    pen.goto(x+Ratio,y-Ratio)#Bottom right
    pen.goto(x,y-Ratio)#Bottom left
    pen.goto(x,y) #Top left
    pen.end_fill()
    pen.penup()
    Play_anime()

def Play_anime(): #Play animation
    global screen
    global Animation
    if Animation == 1: #Animation on
        screen.update()

def Invalid_move(direction): #Error massage output
    global system
    global screen
    global Ratio
    global Size
    global cooldown
    style="Arial", int(25/min(screen.cv.winfo_screenwidth()/Size,screen.cv.winfo_screenheight()/Size)*Ratio*1.5), "bold"
    text_font, text_size, text_weight=style #Unpack text style
    text="You Cannot Move "+direction
    system.clear()
    system.goto(-text_size*len(text)*0.4,text_size*3) #TL of the display
    system.pendown() #Start drawing the display
    system.begin_fill()
    system.fillcolor("white")
    system.goto(text_size*len(text)*0.4,text_size*3) #TR of the display
    system.goto(text_size*len(text)*0.4,-text_size*1.5) #BR of the display
    system.goto(-text_size*len(text)*0.4,-text_size*1.5) #BL of the display
    system.goto(-text_size*len(text)*0.4,text_size*3) #TL of the display
    system.end_fill()
    system.penup() #Finish drawing the display
    system.goto(0,text_size/1.25)
    system.write("Invalid Move", align="center", font=(style))
    system.goto(0,-text_size/1.75)
    system.write(text, align="center", font=(style))
    if not(cooldown): #Preventing Sys_wait_2_second procedure execute multiple times
        screen.ontimer(Sys_wait_2_second, 2000) #Execute after 2 second
        cooldown=True
    screen.update()

def Sys_wait_2_second(): #System massage clear after 2 second
    global system
    global cooldown
    cooldown=False
    system.clear()

def movement_unblind(): #Unblind keys to movement
    global screen
    screen.onkeypress(None,"w")
    screen.onkeypress(None,"s")
    screen.onkeypress(None,"a")
    screen.onkeypress(None,"d")
    screen.listen()

def movement_blind(): #Blind keys to movement
    global screen
    screen.onkeypress(move_up,"w")
    screen.onkeypress(move_down,"s")
    screen.onkeypress(move_left,"a")
    screen.onkeypress(move_right,"d")
    screen.listen()

def move_up():
    global Board
    global player
    global Size
    global Screen
    global Ratio
    global steps
    movement_unblind() #Prevent rapid calling
    temp=player_found() #Found player location
    x=int(temp[0:2])
    y=int(temp[2:4])
    player.setheading(90) #Curser turn toward up
    if y < (Size-1) and Board[x][y+1] != "X":
        Board[x][y]=" "
        y=y+1
        steps=steps+1
        steps_upd()
        if Board[x][y] == "E":
            Board[x][y]="P"
            end(True)
        else:
            Board[x][y]="P" #Change player postion in board
            x=player.xcor()
            y=player.ycor()
            y=y+Ratio
            player.goto(x,y) #Player curser move up
    else:
        Invalid_move("Up")
    screen.ontimer(movement_blind, 10) #Delay 0.01 second
    screen.update()

def move_down():
    global Board
    global player
    global Size
    global Screen
    global Ratio
    global steps
    movement_unblind() #Prevent rapid calling
    temp=player_found() #Found player location
    x=int(temp[0:2])
    y=int(temp[2:4])
    player.setheading(270) #Curser turn toward down
    if y > 0 and Board[x][y-1] != "X":
        Board[x][y]=" "
        y=y-1
        steps=steps+1
        steps_upd()
        if Board[x][y] == "E":
            Board[x][y]="P"
            end(True)
        else:
            Board[x][y]="P" #Change player postion in board
            x=player.xcor()
            y=player.ycor()
            y=y-Ratio
            player.goto(x,y) #Player curser move down
    else:
        Invalid_move("Down")
    screen.ontimer(movement_blind, 10) #Delay 0.01 second
    screen.update()

def move_left():
    global Board
    global player
    global Size
    global Screen
    global Ratio
    global steps
    movement_unblind() #Prevent rapid calling
    temp=player_found() #Found player location
    x=int(temp[0:2])
    y=int(temp[2:4])
    player.setheading(180) #Curser turn toward left
    if x > 0 and Board[x-1][y] != "X":
        Board[x][y]=" "
        x=x-1
        steps=steps+1
        steps_upd()
        if Board[x][y] == "E":
            Board[x][y]="P"
            end(True)
        else:
            Board[x][y]="P" #Change player postion in board
            x=player.xcor()
            y=player.ycor()
            x=x-Ratio
            player.goto(x,y) #Player curser move left
    else:
        Invalid_move("Left")
    screen.ontimer(movement_blind, 10) #Delay 0.01 second
    screen.update()

def move_right():
    global Board
    global player
    global Size
    global Screen
    global Ratio
    global steps
    movement_unblind() #Prevent rapid calling
    temp=player_found() #Found player location
    x=int(temp[0:2])
    y=int(temp[2:4])
    player.setheading(0) #Curser turn toward right
    if x < (Size-1) and Board[x+1][y] != "X":
        Board[x][y]=" "
        x=x+1
        steps=steps+1
        steps_upd()
        if Board[x][y] == "E":
            Board[x][y]="P"
            end(True)
        else:
            Board[x][y]="P" #Change player postion in board
            x=player.xcor()
            y=player.ycor()
            x=x+Ratio
            player.goto(x,y) #Player curser move right
    else:
        Invalid_move("Right")
    screen.ontimer(movement_blind, 10) #Delay 0.01 second
    screen.update()

def main(): #Start point
    global root
    global timer
    global mode
    global cycle
    global Paused #Register did game paused
    root=t.Screen()._root #Access the underlying Tk window
    timer=threading.Thread(target=Timer) #Setup sub-thread
    mode=2
    cycle=0 #Threshold
    Paused=False
    if mode == 1: #CLI
        Menu_CLI()
    elif mode == 2: #GUI
        menu_setup()
    else:
        print("System: ERROR")
        print("System: User interface initialize fail, please restart the game")
        input("System: Press Enter to exit the game ")
        sys.exit()

class Button:
    def __init__(self, x, y, width, height, text, style):
        self.x=x #Top left x coordinate
        self.y=y #Top left y coordinate
        self.width=width
        self.height=height
        self.text=text
        self.style=style
        text_font, text_size, text_weight=style #Unpack text style
        self.text_font=text_font #Text font
        self.text_size=text_size #Text size
        self.text_weight=text_weight #Text weight
    
    def get_x_min(self): #Return the x value bottom bound
        return self.x
    
    def get_x_max(self): #Return the x value upper bound
        return self.x+self.width
    
    def get_y_min(self): #Return the y value bottom bound
        return self.y-self.height
    
    def get_y_max(self): #Return the y value upper bound
        return self.y
    
    def get_text_size(self): #Return the text size
        return self.text_size

    def draw(self): #Draw button
        global pen
        global screen
        pen.goto(self.x,self.y) #TL of the button
        pen.pendown() #Start drawing the button
        pen.goto(self.x+self.width,self.y) #TR of the button
        pen.goto(self.x+self.width,self.y-self.height) #BR of the button
        pen.goto(self.x,self.y-self.height) #BL of the button
        pen.goto(self.x,self.y) #TL of the button
        pen.penup() #Finish drawing the button
        pen.goto(self.x+(self.width/2),self.y-(self.height/2)-(self.text_size*0.8))
        pen.write(self.text, align="center", font=(self.style)) #Write text
        Play_anime()

class Button_L: #Left arrow button
    def __init__(self, x, y, width, height):
        self.x=x #Top left x coordinate
        self.y=y #Top left y coordinate
        self.width=width
        self.height=height

    def get_x_min(self): #Return the x value bottom bound
        return self.x
    
    def get_x_max(self): #Return the x value upper bound
        return self.x+self.width
    
    def get_y_min(self): #Return the y value bottom bound
        return self.y-self.height
    
    def get_y_max(self): #Return the y value upper bound
        return self.y

    def draw(self): #Draw button
        global pen
        global screen
        pen.goto(self.x,self.y) #TL of the button
        pen.pendown() #Start drawing the button
        pen.goto(self.x+self.width,self.y) #TR of the button
        pen.goto(self.x+self.width,self.y-self.height) #BR of the button
        pen.goto(self.x,self.y-self.height) #BL of the button
        pen.goto(self.x,self.y) #TL of the button
        pen.penup()
        pen.goto(self.x+5,self.y-self.height/2) #Arrow left point
        pen.pendown() #Start drawing arrow
        pen.begin_fill()
        pen.fillcolor("black")
        pen.goto(self.x+self.width-5,self.y-5) #Arrow top right point
        pen.goto(self.x+self.width-5,self.y-self.height+5) #Arrow bottom right point
        pen.goto(self.x+5,self.y-self.height/2) #Arrow left point
        pen.end_fill()
        pen.penup() #Finish drawing the button
        Play_anime()

class Button_R: #Right arrow button
    def __init__(self, x, y, width, height):
        self.x=x #Top left x coordinate
        self.y=y #Top left y coordinate
        self.width=width
        self.height=height

    def get_x_min(self): #Return the x value bottom bound
        return self.x
    
    def get_x_max(self): #Return the x value upper bound
        return self.x+self.width
    
    def get_y_min(self): #Return the y value bottom bound
        return self.y-self.height
    
    def get_y_max(self): #Return the y value upper bound
        return self.y

    def draw(self): #Draw button
        global pen
        global screen
        pen.goto(self.x,self.y) #TL of the button
        pen.pendown() #Start drawing the button
        pen.goto(self.x+self.width,self.y) #TR of the button
        pen.goto(self.x+self.width,self.y-self.height) #BR of the button
        pen.goto(self.x,self.y-self.height) #BL of the button
        pen.goto(self.x,self.y) #TL of the button
        pen.penup()
        pen.goto(self.x+5,self.y-5) #Arrow top left point
        pen.pendown() #Start drawing arrow
        pen.begin_fill()
        pen.fillcolor("black")
        pen.goto(self.x+self.width-5,self.y-self.height/2) #Arrow right point
        pen.goto(self.x+5,self.y-self.height+5) #Arrow bottom leftight point
        pen.goto(self.x+5,self.y-5) #Arrow top left point
        pen.end_fill()
        pen.penup() #Finish drawing the button
        Play_anime()

class Option_set:
    def __init__(self, x, y, style, text, text_list ,n):
        self.x=x #Top left x coordinate
        self.y=y #Top left y coordinate
        self.style=style #Text style
        text_font, text_size, text_weight=style #Unpack text style
        self.text_font=text_font #Text font
        self.text_size=text_size #Text size
        self.text_weight=text_weight #Text weight
        self.text=text #Text
        self.text_list=text_list #List of text show on display
        self.n=n-1 #nth item of the list to diaplay

    def get_btL_x_min(self): #Return the x value bottom bound of the left arrow button
        return self.btL.get_x_min()

    def get_btL_x_max(self): #Return the x value upper bound of the left arrow button
        return self.btL.get_x_max()
    
    def get_btL_y_min(self): #Return the y value bottom bound of the left arrow button
        return self.btL.get_y_min()
    
    def get_btL_y_max(self): #Return the y value upper bound of the left arrow button
        return self.btL.get_y_max()
    
    def get_btR_x_min(self): #Return the x value bottom bound of the right arrow button
        return self.btR.get_x_min()
    
    def get_btR_x_max(self): #Return the x value upper bound of the right arrow button
        return self.btR.get_x_max()
    
    def get_btR_y_min(self): #Return the y value bottom bound of the right arrow button
        return self.btR.get_y_min()
    
    def get_btR_y_max(self): #Return the y value upper bound of the right arrow button
        return self.btR.get_y_max()

    def get_text_list_nth_item(self,n): #Return specific item from text list
        text=self.text_list[n-1]
        text=text.lower()
        return text

    def get_text_list_length(self): #Return list length
        return len(self.text_list)

    def set_n(self,n): #Change the display
        self.n=n-1

    def draw(self):
        global pen
        x=self.x #X coordinate of the pen
        pen.goto(x,self.y-(self.text_size+self.text_size/2+5)) #Text centre bottom position
        pen.write(self.text, align="center", font=(self.style))
        x=x+(len(self.text)*self.text_size/3.5) #Text to left arrow button TL position
        self.btL=Button_L(x,self.y,self.text_size,self.text_size*2) #Left arrow button setup
        self.btL.draw()
        x=x+self.text_size+5 #Left arrow button TL to display TL position
        max_length=0 #Longest string length
        for i in range(len(self.text_list)): #Found the longest string length
            length=len(self.text_list[i]) #String length of current string
            if length > max_length:
                max_length=length
        width=max_length*self.text_size/1.375
        self.dp=Button(x,self.y,width,self.text_size*2,self.text_list[self.n],self.style) #Display setup
        self.dp.draw() #Draw the display
        x=x+width+5 #Display to right arrow button TL position
        self.btR=Button_R(x,self.y,self.text_size,self.text_size*2) #Right arrow button setup
        self.btR.draw()

class Player: #Player character class, mainly used for 2 player mode. Development paused
    def __init__(self,Board,color,shape):
        self.Board=Board #Game board
        self.color=color #Character color
        self.shape=shape #Character shape
        self.steps=0 #Steps taken
        self.setup()

    def setup(self): #Character setup
        global Ratio
        self.character=t.Turtle() #Player character
        self.character.shapesize((Ratio/20), (Ratio/20))
        self.character.penup()
        self.character.color(self.color)
        self.character.shape(self.shape)
        self.character.goto((Ratio/4),0)
        self.character.hideturtle()

    def get_steps(self): #Return steps taken
        return self.steps

    def player_found(self): #Automated relocate player position
        global Size
        found=False #Register did the player position found
        x=0
        y=0
        try_n=0
        while found != True: #Automated relocate player position
            if self.Board[x][y] == "P":
                found=True
            else:
                y=y+1
                if y > (Size-1):
                    x=x+1
                    y=0
                    if x > (Size-1):
                        if try_n != 3:
                            x=0
                            y=0
                            try_n=try_n+1
                        else:
                            print("System: ERROR")
                            print("System: Player position not found, please restart the game")
                            input("System: Press Enter to exit the game ")
                            sys.exit()
        coordinate=grid(x,y)
        return coordinate #Return player coordinate in Grid fromat

    def move_up(self): #Character move up
        global Size
        global Screen
        global Ratio
        temp=self.player_found() #Found player location
        x=int(temp[0:2])
        y=int(temp[2:4])
        self.character.setheading(90) #Curser turn toward up
        if y < (Size-1) and self.Board[x][y+1] != "X":
            self.Board[x][y]=" "
            y=y+1
            self.steps=self.steps+1
            steps_upd()
            if self.Board[x][y] == "E":
                self.Board[x][y]="P"
                end(True)
            else:
                self.Board[x][y]="P" #Change player postion in board
                x=self.character.xcor()
                y=self.character.ycor()
                y=y+Ratio
                self.character.goto(x,y) #Player curser move up
        else:
            Invalid_move("Up")
        screen.update()

    def move_down(self): #Character move down
        global Size
        global Screen
        global Ratio
        temp=self.player_found() #Found player location
        x=int(temp[0:2])
        y=int(temp[2:4])
        self.character.setheading(270) #Curser turn toward down
        if y > 0 and self.Board[x][y-1] != "X":
            self.Board[x][y]=" "
            y=y-1
            self.steps=self.steps+1
            steps_upd()
            if self.Board[x][y] == "E":
                self.Board[x][y]="P"
                end(True)
            else:
                self.Board[x][y]="P" #Change player postion in board
                x=self.character.xcor()
                y=self.character.ycor()
                y=y-Ratio
                self.character.goto(x,y) #Player curser move down
        else:
            Invalid_move("Down")
        screen.update()

    def move_left(self): #Character move left
        global Size
        global Screen
        global Ratio
        temp=self.player_found() #Found player location
        x=int(temp[0:2])
        y=int(temp[2:4])
        self.character.setheading(180) #Curser turn toward left
        if x > 0 and self.Board[x-1][y] != "X":
            self.Board[x][y]=" "
            x=x-1
            self.steps=self.steps+1
            steps_upd()
            if self.Board[x][y] == "E":
                self.Board[x][y]="P"
                end(True)
            else:
                self.Board[x][y]="P" #Change player postion in board
                x=self.character.xcor()
                y=self.character.ycor()
                x=x-Ratio
                self.character.goto(x,y) #Player curser move left
        else:
            Invalid_move("Left")
        screen.update()

    def move_right(self): #Character move right
        global Size
        global Screen
        global Ratio
        temp=self.player_found() #Found player location
        x=int(temp[0:2])
        y=int(temp[2:4])
        self.character.setheading(0) #Curser turn toward right
        if x < (Size-1) and Board[x+1][y] != "X":
            self.Board[x][y]=" "
            x=x+1
            self.steps=self.steps+1
            steps_upd()
            if self.Board[x][y] == "E":
                self.Board[x][y]="P"
                end(True)
            else:
                self.Board[x][y]="P" #Change player postion in board
                x=self.character.xcor()
                y=self.character.ycor()
                x=x+Ratio
                self.character.goto(x,y) #Player curser move right
        else:
            Invalid_move("Right")
        screen.update()

import time
import random
import sys
import threading
import turtle as t
try: #Check did pygame installed
    import pygame
    pygame.init() #Initialise pygame
    if not(pygame.get_init()): #Check did pygame fully initialised
        print("System: ERROR")
        print("System: Failed to fully initialise pygame")
        print("System: Please restart the game or restore pygame")
        ans=input("System: Press Enter to exit the game or type '/Run' to continue without pygame ")
        if ans.lower() == "/run":
            Pyg=False
        else:
            sys.exit()
    else:
        from pygame import mixer #Import mixer
        mixer.init() #Pygame mixer initialised
        load_audio() #Load in audio
        Pyg=True
except:
    print("System: ERROR")
    print("System: Failed to import pygame")
    print("System: Please make sure pygame was installed")
    ans=input("System: Press Enter to exit the game or type '/Run' to continue without pygame ")
    if ans.lower() == "/run":
        Pyg=False
    else:
        sys.exit()
main()
