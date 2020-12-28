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
    running = True
    space = False
    drawOn = False
    erase = False
    pickStart = False
    pickEnd = False
    algoritmNeAplicat = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space = True
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
                drawOn = False
                pickStart = pickEnd = False
                if event.key == pygame.K_s:
                    pickStart = True
                elif event.key == pygame.K_e:
                    pickEnd = True
                elif event.key == pygame.K_SPACE:
                    if algoritmNeAplicat:
                        if (m.canStart()):
                            m.startSolve()
                            while(m.continueSolve()):
                                m.showMatrix()
                                pygame.display.update()
                        algoritmNeAplicat = False
                    else:
                        m.minPath()
                        pygame.display.update()
                elif event.key == pygame.K_g:
                    m.saveMatrix()
                elif event.key == pygame.K_f:
                    algoritmNeAplicat = True
                    m.getMatrixFromFile()
            elif event.type == pygame.KEYUP:
                pickStart = False
                pickEnd = False
        if algoritmNeAplicat:
            if drawOn:
                if erase:
                    m.erase(*getMousePos())
                else:
                    m.draw(*getMousePos())
        m.showMatrix()
        #screen.blit(font.render("69", True, (255, 255, 0)), (420, 420))
        pygame.display.update()
        #com