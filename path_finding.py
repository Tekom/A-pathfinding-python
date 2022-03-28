import pygame
import math
import time
import sys

sys.setrecursionlimit(100000)

ANCHO = 600 

VERDE = (31, 241, 10)
ROJO = (241, 31, 10) 
visitado = []
casillaDisponible = []
nodoPadre = {}
padresNoVisitados = {}

def main():
    global VENTANA, tamBloque, pared
    VENTANA = pygame.display.set_mode((ANCHO,ANCHO))
    VENTANA.fill((255,255,255))

    run = True
    tamBloque = 20
    tipoCuadro = 0
    pared = []

    Cuadricula(tamBloque)
    pygame.display.set_caption("Path Finding Algorithm")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                Dibujar(pos, tamBloque, tipoCuadro)

                if tipoCuadro < 2:
                    tipoCuadro+=1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                   Algoritmo()

    pygame.quit()

def Cuadricula(tamBloque):
    for i in range(0, ANCHO, tamBloque):
        pygame.draw.line(VENTANA, (0,0,0), (0,i), (ANCHO,i))

    for i in range(0, ANCHO, tamBloque):
       pygame.draw.line(VENTANA, (0,0,0), (i,0), (i,ANCHO))

    pygame.display.update()

def Dibujar(pos, tamBloque, tipoCuadro):
    global posInicial, posFinal, nodoActual, nodoAnterior

    if tipoCuadro == 0:
        color = (42, 214, 203)
        posInicial = (pos[0] // tamBloque, pos[1] // tamBloque)
        nodoAnterior = (pos[0] // tamBloque, pos[1] // tamBloque)
        nodoActual = [pos[0] // tamBloque, pos[1] // tamBloque]

    if tipoCuadro == 1:
        color = (254, 231, 36)
        posFinal = [pos[0] // tamBloque, pos[1] // tamBloque]

    if tipoCuadro == 2:
        color = (0,0,0)
        pared.append((pos[0] // tamBloque, pos[1] // tamBloque))

    x = pos[0] // tamBloque
    y = pos[1] // tamBloque

    cuadrado = pygame.Rect(x*tamBloque+1, y*tamBloque+1, tamBloque-1, tamBloque-1)
    pygame.draw.rect(VENTANA, color, cuadrado)
    pygame.display.update()

def distanciaPuntos(casillaDisponibles):
    x2,y2 = posFinal
    x3,y3 = posInicial
    distanciaF = []

    for i in casillaDisponibles:
        x1,y1 = i
        a = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        b = math.sqrt((x3-x1)**2 + (y3-y1)**2)
        distanciaF.append(a + b)

    xVisitado, yVisitado = casillaDisponibles[distanciaF.index(min(distanciaF))] 
    nodoPadre[(xVisitado, yVisitado)] = padresNoVisitados[(xVisitado, yVisitado)] #asignar a la posicion asignada su padre

    return (xVisitado, yVisitado)

def calcularPath():
    camino2 = []
    padres = list(nodoPadre.keys())
    primerPadre = list(nodoPadre.values())[::-1][0]
    primerNodo = padres[::-1][0]

    camino2.append(primerNodo)
    camino2.append(primerPadre)
    asd = 0

    while True:
        for son, father in nodoPadre.items():
            if son == primerPadre:
                camino2.append(nodoPadre[son])
                primerPadre = nodoPadre[son]
        asd+=1
        if asd == 100:
            break

    for i in camino2:
        x,y = i
        cuadrado = pygame.Rect((x)*tamBloque+1, (y)*tamBloque+1, tamBloque-1, tamBloque-1)
        pygame.draw.rect(VENTANA, (34,78,232), cuadrado)
        pygame.display.update()

def Algoritmo():
    global casillaDisponible, nodoAnterior

    vecinoInicialx = nodoActual[0]
    vecinoInicialy = nodoActual[1]-1

    if nodoActual == posFinal:
        return True

    for i in range(5):
        if i == 0 and (vecinoInicialx, vecinoInicialy) not in visitado and (vecinoInicialx, vecinoInicialy) not in pared:
            cuadrado = pygame.Rect((vecinoInicialx)*tamBloque+1, (vecinoInicialy)*tamBloque+1, tamBloque-1, tamBloque-1)
            casillaDisponible.append((vecinoInicialx, vecinoInicialy))
            padresNoVisitados[(vecinoInicialx, vecinoInicialy)] = (vecinoInicialx, vecinoInicialy+1)
            pygame.draw.rect(VENTANA, VERDE, cuadrado)

        elif i == 1 and (vecinoInicialx-1, vecinoInicialy+1) not in visitado and (vecinoInicialx-1, vecinoInicialy+1) not in pared:
            cuadrado = pygame.Rect((vecinoInicialx-1)*tamBloque+1, (vecinoInicialy+1)*tamBloque+1, tamBloque-1, tamBloque-1)
            casillaDisponible.append((vecinoInicialx-1, vecinoInicialy+1))
            padresNoVisitados[(vecinoInicialx-1, vecinoInicialy+1)] = (vecinoInicialx, vecinoInicialy+1)
            pygame.draw.rect(VENTANA, VERDE, cuadrado)
            
        elif i == 2:
            cuadrado = pygame.Rect((vecinoInicialx)*tamBloque+1, (vecinoInicialy+1)*tamBloque+1, tamBloque-1, tamBloque-1)
            visitado.append((vecinoInicialx, vecinoInicialy+1))
            pygame.draw.rect(VENTANA, ROJO, cuadrado)
            
        elif i == 3 and (vecinoInicialx+1, vecinoInicialy+1) not in visitado and (vecinoInicialx+1, vecinoInicialy+1) not in pared: 
            cuadrado = pygame.Rect((vecinoInicialx+1)*tamBloque+1, (vecinoInicialy+1)*tamBloque+1, tamBloque-1, tamBloque-1)
            casillaDisponible.append((vecinoInicialx+1, vecinoInicialy+1))
            padresNoVisitados[(vecinoInicialx+1, vecinoInicialy+1)] = (vecinoInicialx, vecinoInicialy+1)
            pygame.draw.rect(VENTANA, VERDE, cuadrado)
            
        elif i == 4 and (vecinoInicialx, vecinoInicialy+2) not in visitado and (vecinoInicialx, vecinoInicialy+2) not in pared:
            cuadrado = pygame.Rect((vecinoInicialx)*tamBloque+1, (vecinoInicialy+2)*tamBloque+1, tamBloque-1, tamBloque-1)
            casillaDisponible.append((vecinoInicialx, vecinoInicialy+2))
            padresNoVisitados[(vecinoInicialx, vecinoInicialy+2)] = (vecinoInicialx, vecinoInicialy+1)
            pygame.draw.rect(VENTANA, VERDE, cuadrado)

    pygame.display.update() 
    casillaDisponible = list(set(casillaDisponible))
    distanciaObjetivo = distanciaPuntos(casillaDisponible)
    casillaDisponible.remove(distanciaObjetivo)

    nodoActual[0] = distanciaObjetivo[0]
    nodoActual[1] = distanciaObjetivo[1]

    if Algoritmo():
        calcularPath()
        cuadrado = pygame.Rect(posInicial[0]*tamBloque+1, posInicial[1]*tamBloque+1, tamBloque-1, tamBloque-1)
        pygame.draw.rect(VENTANA, (42, 214, 203), cuadrado)

        cuadrado = pygame.Rect(posFinal[0]*tamBloque+1, posFinal[1]*tamBloque+1, tamBloque-1, tamBloque-1)
        pygame.draw.rect(VENTANA, (254, 231, 36), cuadrado)

        pygame.display.update()

if __name__ == '__main__':
    main()
