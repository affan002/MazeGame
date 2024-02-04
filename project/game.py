# importing libraries 
import pygame
import random
import os
# Initializing pygame and it's modules
pygame.init() 
pygame.font.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 50)

WIDTH, HEIGHT = 750, 550  #set dimensions of the main window
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a game window
pygame.display.set_caption("welcome to the maze!") # creates WIN's title

# Defining RGB color constants in tuples for later use
WHITE = (225, 225, 225)
DARK_BLUE = (0, 0, 139)
CHARCOAL_GREY = (47, 79, 79)
YELLOW = (255, 165, 0)

def win_display(): #function for displaying winning screen
    text_surface = font.render('You won!', True, (0, 0, 0))
    WIN.blit(text_surface, ((WIDTH // 2) - 80, (HEIGHT // 2) - 50))
    s = "sound"
    winsound = pygame.mixer.Sound("success-fanfare-trumpets-6185.mp3") #initialises win sound 
    pygame.mixer.Sound.play(winsound) # plays the winning sound
    pygame.display.update()
    pygame.time.wait(2700)

#uses DEPTH FIRST SEARCH algorithm to create a solvable maze
def dfs(maze, x, y, width, height): 
    maze[y][x] = 0 #set starting value to visited 
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)
    for dx, dy in directions:
        newcoordx = x + dx * 2
        newcoordy = y + dy * 2 #moves two cells ahead and assigns new coordinates
        if 0 <= newcoordx < width and 0 <= newcoordy < height:
          if maze[newcoordy][newcoordx] == 1: 
              #checks if the new x and y values are valid
              maze[y + dy][x + dx] = 0 #marks new coordinate as visited
              dfs(maze, newcoordx, newcoordy, width, height)
#use dfs to randomely generate a maze
def generate_random_maze(width, height):
    maze = [] # generates a maze where all values are unvisited
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(1)
        maze.append(row)

    #randomly selects a starting point
    start_x = random.randint(0, width - 1) 
    start_y =  random.randint(0, height - 1)

    maze[start_y][start_x] = 3  # Set the starting point as player
    dfs(maze, start_x, start_y, width, height)
    end_x = random.randint(0, width - 1)
    end_y = random.randint(0, height - 1) 

    while maze[end_y][end_x] != 0:
        end_x = random.randint(0, width - 1)
        end_y = random.randint(0, height - 1)
    maze[end_y][end_x] = 2  # Set the end point as destination

    # returns a random maze, coordinates for player and destination 
    return maze, [start_x, start_y], [end_x, end_y] 

# defining function for maze rendering
def render_maze(maze):
    # to assign player, destination, path and walls to items in maze matrix
    mazedict = {"path": 0, "wall": 1, "player": 3, "destination": 2}
  
    x, y = 0, 0  # initializes x and y for rendering
    for row in maze:
        for block in row:
            if block == mazedict["path"]: # path rendered as white
                pygame.draw.rect(WIN, WHITE, (x, y, 50, 50))
            elif block == mazedict["wall"]: # walls rendered as dark_blue
                pygame.draw.rect(WIN, DARK_BLUE, (x, y, 50, 50))
            elif block == mazedict["destination"]: # destinations rendered as grey 
                pygame.draw.rect(WIN, CHARCOAL_GREY, (x, y, 50, 50))
            elif block == mazedict["player"]: # player rendered as yellow
                pygame.draw.rect(WIN, YELLOW, (x, y, 50, 50))               
            x += 50
        y += 50 
        x = 0
    pygame.display.update()


def main():
    width = 15
    height = 11
    maze, player, destination = generate_random_maze(width, height)
    maze[player[1]][player[0]] = 3
    maze[destination[1]][destination[0]] = 2
    x = player[0]
    y = player[1]
    run = True
    while run:
        keys = pygame.key.get_pressed()
        render_maze(maze)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:# sets run to false if the user closes the window
                run = False
        if keys[pygame.K_UP] and 0 <= (y-1) < height: 
            block = maze[y-1][x]
            if block == 0:
                maze[y-1][x] = 3 #moves player 
                maze[y][x] = 0
                y = y - 1
            elif block == 2:
                maze[y-1][x] = 0
                maze[y][x] = 0
                win_display()
                run = False # if destination (2) is reached sets run to false

        elif keys[pygame.K_DOWN] and 0 <= (y+1) < height:
            block = maze[y+1][x]
            if block == 0:
                maze[y+1][x] = 3
                maze[y][x] = 0
                y = y + 1
            elif block == 2:
                maze[y+1][x] = 0
                maze[y][x] = 0
                win_display()
                run = False

        elif keys[pygame.K_LEFT] and 0 <= (x-1) < width:
            block = maze[y][x-1]
            if block == 0:
                maze[y][x-1] = 3
                maze[y][x] = 0
                x = x - 1
            elif block == 2: 
                maze[y][x-1] = 0
                maze[y][x] = 0
                win_display()
                run = False   

        elif keys[pygame.K_RIGHT] and 0 <= (x+1) < width:
            block = maze[y][x+1]
            if block == 0:
                maze[y][x+1]=3
                maze[y][x]=0
                x = x + 1
            elif block == 2:
                maze[y][x+1] = 0 
                maze[y][x] = 0       
                win_display()
                run = False

        pygame.time.delay(100)
    pygame.quit()

main()