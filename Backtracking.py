from turtle import TurtleScreen, RawTurtle, TK
from time import sleep
import os.path as path


def widerror(Terror):
    wid2 = TK.Tk()
    wid2.title("ERROR")
    wid2.geometry("350x100")
    wid2["bg"] = "black"
    bsc2 = TK.Label(wid2,text=Terror)
    bsc2["fg"] = "white"
    bsc2["bg"] = "black"
    bsc2.place(x=70, y=20)
    TK.Button(wid2, text='OK', 
                   command=wid2.destroy).place(x=150, y=50)

def info():
    var=entry.get()
    file=var+".txt"
    
    if path.exists(file):
        try:
            NXM=claberinto(var)
            x,y=ubicacion(NXM)
            z=setearlab(NXM)
            #wid.withdraw()
            principal(z,x,y)
        except:
            widerror("Formato del archivo no valido")

    else:
        widerror("nombre de archivo no valido")
class Ventana():
    """ Esta clase permite crear ventanas en las cuales
        existe un TurtleScreen  llamado 'fondo_ventana' 
        y una tortuga llamada 'pencil'.

        La ventana tiene las siguientes características:
        - Tiene un solo cuadrante.
        - Todos los valores en el eje 'x' son positivos
          y van hacia la derecha.
        - Todos los valores en el eje 'y' son positivos
          y van hacia abajo.
        - La posición (0, 0) se ubica en la esquina
          superior izquierda.
        - La posición (ancho, alto) se ubica en la
          esquina inferior derecha.

        Nota 1: para cambiar el sistema de coordenadas se
        utilizó el método setworldcoordinates(x1,y1,x2,y2).

        Nota 2: cuando se cambia el sistema de coordinadas
        los 'puntos cardinales' o la 'izquierda' o 'derecha'
        pueden cambiar.
          
        Por ejemplo el siguiente código ilustra el uso de
        esta clase:
           >>
           >> mi_ventana = Ventana("Dibujo", 400, 600)
           >> mi_ventana.pencil.fd(50)
           >> mi_ventana.pencil.left(90)
           >> mi_ventana.pencil.fd(25)
           >>
    """

    def __init__(self, titulo, alto, ancho):
        """ Crea una ventana para dibujar el laberinto.
            Entradas:
                titulo : título de la ventana.
                alto   : alto de la ventana en pixeles.
                ancho  : ancho de la ventna en pixeles.
            Salidas:
                Ninguna.
            Restricciones:
                titulo es una tira, alto y ancho son enteros positivos.
        """
        assert isinstance(titulo, str)
        assert isinstance(alto, int) and alto > 0
        assert isinstance(ancho, int) and ancho > 0

        ## Crea la ventana y un canvas para dibujar
        self.root = TK.Tk()
        self.root.title(titulo)
        self.canvas = TK.Canvas(self.root, width=ancho, height=alto)
        self.canvas.pack()
        
        ## Crea un TurtleScreen y la tortuga para dibujar
        self.fondo_ventana = TurtleScreen(self.canvas)
        self.fondo_ventana.setworldcoordinates(0, alto, ancho, 0)

        ## Establece el color de fondo
        self.canvas["bg"] = "black"
        self.canvas.pack()

        ## Crea una tortuga para dibujar
        self.pencil = RawTurtle(self.fondo_ventana)
        self.pencil.pencolor("white")
class Laberinto():
    """ Esta clase implementa un laberinto el cual
        se configura a partir de una tira de caracteres.
    """

    ## Atributos de clase que define a partir de que
    ## coordenadas en el eje horizontal(x) y vertical(y)
    ## se empieza a dibujar el laberinto.
    Xdis = 10
    Ydis = 10

    ## Atributos de clase que define el alto y el ancho
    ## de cada casilla del laberinto.
    Alto = 12
    Ancho= 12

    ## Método de clase.
    ## Los métodos de clase son métodos globales a todas
    ## las instancias de una clase y se invocan utilizando
    ## Nombre_clase.nombre_método(argumentos).
    ## Los métodos de clase deben estar precedidos de la
    ## directiva @staticmethod.
    @staticmethod
    def deme_posicion(i, j):
        """ Retorna la posicion superior izquierda en eje x, eje y
            de un casilla i,j del laberinto.
            Entradas:
                i     : Fila del laberinto.
                j     : Columna del laberinto.
            Salidas:
                (x,y) : Posición de la esquina superior izquierda
                        en donde se encuentra la entrada (i,j)
            Supuesto:
                (i,j) es una posición válida en el laberinto.
        """
        x = Laberinto.Xdis + j * (Laberinto.Ancho + 1)
        y = Laberinto.Ydis + i * (Laberinto.Alto  + 1)
        return (x, y)
    def __init__(self, area_dibujo, laberinto):
        """ Constructor para la creación de un laberinto.
            Entradas:
                 area_dibujo : TurtleScreen en donde se dibujará
                               el laberinto.
                 laberinto   : tira que contiene el diseño del
                               laberinto.
            Salidas:
                 Instancia de la clase.
                 Laberinto representado por una matriz, tal que
                 la entrada i,j contiene: 0 - si la casilla está
                 libre, 1 - si hay pared, 3 - posición en donde
                 está el queso.
            Restricciones:
                 Todas las entradas de la tira son 0, 1 o 3. Las
                 filas se representan por un cambio de línea.
                 No hay líneas vacías.
        """
        ## Construye una lista de listas a partir de la
        ## tira que se recibe como parámetro.
        lista = laberinto.split()
        lista = [ x[:-1] if x[-1] == "\n" else x for x in lista]
        lista = [[int(ch) for ch in x] for x in lista]


        ## Crea los atributos.
        self.laberinto = lista
        self.lienzo = area_dibujo

        ## Dibuja el laberinto.
        self.dibuja_laberinto()

    def dibuja_laberinto(self):
        """ Dibuja el laberinto.
        Entradas:
            Ninguna.
        Salidas:
            Dibujo del laberinto.
        """

        self.lienzo.fondo_ventana.tracer(False)
        self.lienzo.pencil.pencolor("white")

        ## Dibuja el laberinto.

        for i in range(len(self.laberinto)):

            for j in range(len(self.laberinto[i])):

                if self.laberinto[i][j] == 1:
                    self.casilla("yellow", i, j)
                elif self.laberinto[i][j] == 3:
                    self.casilla("red", i, j)
                elif self.laberinto[i][j] == 0:
                    self.casilla("black", i, j)

        self.lienzo.fondo_ventana.tracer(True)

    def casilla(self, color, i, j):
        """ Dibuja la casilla i, j con el color
            indicado.
        Entradas:
            color : Color de la casilla a dibujar.
            (i,j) : Ubicación de la casilla.
        Salidas:
            Dibujo de la casilla con el color indicado en
            la posición (i,j) del laberinto.
        Supuesto:
            El color es uno válido en Tkinter.
            (i,j) es una posición válida en el
            laberinto.
        """

        ## Determina la posición en los ejes
        ## reales de la posición (i,j) de la
        ## casilla.
        x, y = Laberinto.deme_posicion(i, j)

        ## Prepara el lápiz para dibujar
        ## un rectánculo relleno.
        self.lienzo.pencil.fillcolor(color)
        self.lienzo.pencil.pu()
        self.lienzo.pencil.setpos(x, y)
        self.lienzo.pencil.seth(0)
        self.lienzo.pencil.pd()
        self.lienzo.pencil.begin_fill()

        ## Dibuja la casilla con 4
        ## movimientos !!!
        for i in range(2):
            self.lienzo.pencil.fd(Laberinto.Ancho+1)
            self.lienzo.pencil.left(90)
            self.lienzo.pencil.fd(Laberinto.Alto+1)
            self.lienzo.pencil.left(90)

        ## Cierra el relleno.
        self.lienzo.pencil.end_fill()

    def recorrido(self, i, j):
        """ Dado un laberinto en donde se ubica un queso,
            retorna en una lista de pares ordenados (x,y)
            que indican el camino desde una posición inicial
            (i,j) hasta la posición en que se encuentra el
            queso.
            Entradas:
                 (i, j) : posición inicial a partir de donde
                          se realizará la búsqueda de un camino
                          hasta la posición del queso.
            Salidas:
                 Lista con las casillas, expresadas como pares
                 ordenados, que llevan desde la posición inicial
                 hasta la posición en que se encuentra el queso.
                 Si no existe un camino retorna la lista vacía.
        """

        if self.laberinto[i][j] == 3:
            return [(i, j)]

        if self.laberinto[i][j] == 1:
            return []

        self.laberinto[i][j] = -1

        sleep(0.10)
        self.lienzo.fondo_ventana.tracer(False)
        self.casilla("green", i, j)
        self.lienzo.fondo_ventana.tracer(True)

        if i > 0 and self.laberinto[i - 1][j] in [0, 3]:     # Norte
            camino = self.recorrido(i - 1, j)
            if camino: return [(i, j)] + camino

        if j < len(self.laberinto[i]) - 1 and \
           self.laberinto[i][j + 1] in [0, 3]:               # Este
            camino = self.recorrido(i, j + 1)
            if camino: return [(i, j)] + camino

        if i < len(self.laberinto) - 1 and \
           self.laberinto[i + 1][j] in [0, 3]:               # Sur
            camino = self.recorrido(i + 1, j)
            if camino: return [(i, j)] + camino

        if j > 0 and self.laberinto[i][j - 1] in [0, 3]:     # Oeste
            camino = self.recorrido(i, j - 1) 
            if camino: return [(i, j)] + camino

        sleep(0.10)
        self.lienzo.fondo_ventana.tracer(False)
        self.casilla("black", i, j)
        self.lienzo.fondo_ventana.tracer(True)

        return []

    def reset(self):
        """ Re-establece el laberinto luego de que
            se efectúa un recorrido.

            Entradas:
                Ninguna.

            Salidas:
                Actualiza el laberinto.
        """

        for i in range(len(self.laberinto)):
            for j in range(len(self.laberinto[i])):
                if self.laberinto[i][j] == -1:
                    self.laberinto[i][j] = 0
#crear laberinto
def claberinto (narray):
    f = open(narray+".txt", "r")
    row=0
    NXM=[[]]
    while(True):
        linea = f.readline()
        for letra in linea:
            if(letra == "\n"):
                NXM.append([])
                row+=1
            else:
                NXM[row].append(letra)
        if not linea:
            break
    f.close()
    return NXM

def ubicacion (NXM):
    try:
        col=0
        row=0
        ant=len(NXM[col])
        col+=(len(NXM))
        for y in range(col):
            if "*" in NXM[y]:
                x=NXM[y].index("*")
                return x,y
            else:
                None
    except:
        widerror("archivo no valido favor revisar")
def setearlab(NXM):
    z=""
    lineas=len(NXM)
    for i in range(lineas):
        
        x = "".join(NXM[i])
        x=x.replace("#", "1")
        x=x.replace(" ","0")
        x=x.replace("*","0")
        x=x.replace("S","3")
        z=z+x+"\n"
    return z

def principal(z,x,y):
    """ Función principal del módulo.
    """
    ll = Laberinto(Ventana("Laberinto", 500, 500), z)
    ll.recorrido(y,x)
    ll.reset()

if __name__ == "__main__":
    wid = TK.Tk()
    wid.title("Buscar")
    wid.geometry("380x300")
    wid["bg"] = "black"
    entry = TK.Entry(wid)
    entry.place(x=120, y=50)
    bsc = TK.Label(text="Ingrese nombre del archivo (sin extension)")
    bsc["fg"] = "white"
    bsc["bg"] = "black"
    bsc.place(x=70, y=20)

    TK.Button(wid, text='Buscar', 
                   command=info).place(x=300, y=80)
    TK.Button(wid, text='Salir', 
                   command=wid.destroy).place(x=20, y=80)
    wid.mainloop()
    
    #principal()