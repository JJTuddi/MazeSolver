import pygame
import maze
import time
imgSize = 32
size = (704, 704)
width, height = size
rows = height // imgSize
columns = width // imgSize

pygame.init()
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont("Calibri.ttf", 16)

def getMousePos():
    mx, my = pygame.mouse.get_pos()
    return mx // imgSize, my // imgSize

if __name__ == '__main__':
    m = maze.Maze(rows, columns, screen, font)
    # algorith states
    running = True # state for app window
    # state for algorithm runnin
    space = False
    algoritmNeAplicat = True
    # states for drawing
    drawOn = False
    erase = False
    pickStart = False
    pickEnd = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    m.initializeMatrix()
                    algoritmNeAplicat = True
                else:
                    drawOn = True
                    if event.button == 1:
                        erase = False
                        if pickStart:
                            drawOn = False
                            m.setStart(*getMousePos())
                        if pickEnd:
                            drawOn = False
                            m.setEnd(*getMousePos())
                    elif event.button == 3:
                        erase = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawOn = False
            if event.type == pygame.KEYDOWN:
                drawOn = False # you can't draw while you pick the starting point and ending point
                pickStart = pickEnd = False
                if event.key == pygame.K_s:
                    pickStart = True
                elif event.key == pygame.K_e:
                    pickEnd = True
                elif event.key == pygame.K_SPACE:
                    space = True # if you press space, the algorithm starts
                    if algoritmNeAplicat:
                        if (m.canStart()): # canStart() is true if you fixed the starting point and ending point
                            m.startSolve()
                            while(m.continueSolve()): # can continue is true iff you can apply LEE/BFS algorithm (the queue isn't empty or you didn't reached the ending point)
                                pygame.display.update()
                        algoritmNeAplicat = False # you can't draw anymore after you ran the algorithm
                    else:
                        m.minPath() # if the algorithm was applied, now you can draw the minimum path
                        pygame.display.update()
                elif event.key == pygame.K_g:
                    m.saveMatrix() # the key g saves the drawed map on secondary memory
                elif event.key == pygame.K_f:
                    algoritmNeAplicat = True
                    m.getMatrixFromFile() # if you press f, the algorithm restart with map from map.txt
            elif event.type == pygame.KEYUP:
                pickStart = False
                pickEnd = False
        if algoritmNeAplicat: # you can t draw while algorithm is working, this is just for lock drawing mode
            if drawOn:
                if erase:
                    m.erase(*getMousePos())
                else:
                    m.draw(*getMousePos())
        m.showMatrix()
        #screen.blit(font.render("69", True, (255, 255, 0)), (420, 420))
        pygame.display.update()
        #com