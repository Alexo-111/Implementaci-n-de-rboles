from collections import deque


class Nodo:

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None


class Arbol:

    def __init__(self):
        self.raiz = None

    def __del__(self):
        self.podar_arbol(self.raiz)
        self.raiz = None

    def podar_arbol(self, nodo):
        if nodo is None:
            return
        self.podar_arbol(nodo.izquierdo)
        self.podar_arbol(nodo.derecho)
        nodo.izquierdo = None
        nodo.derecho = None

    def es_vacio(self):
        return self.raiz is None

    def regresa_raiz(self):
        return self.raiz

    def insertar_nodo(self, valor, nodo=None, _inicio=True):
        if _inicio:
            nodo = self.raiz
        if nodo is None:
            nuevo = Nodo(valor)
            if _inicio:
                self.raiz = nuevo
            return nuevo
        if valor < nodo.dato:
            nodo.izquierdo = self.insertar_nodo(valor, nodo.izquierdo, False)
        elif valor > nodo.dato:
            nodo.derecho = self.insertar_nodo(valor, nodo.derecho, False)
        else:
            if _inicio:
                print(f"  El valor {valor} ya existe; no se insertó.")
        return nodo

    def muestra_acostado(self, nivel=0, nodo="raiz"):
        if nodo == "raiz":
            nodo = self.raiz
            if nodo is None:
                print("  (árbol vacío)")
                return
        if nodo is None:
            return
        self.muestra_acostado(nivel + 1, nodo.derecho)
        print("      " * nivel + str(nodo.dato))
        self.muestra_acostado(nivel + 1, nodo.izquierdo)

    def graficar_arbol(self):
        if self.raiz is None:
            print("  (árbol vacío)")
            return

        ancho_celda = 4
        posiciones = {}
        contador = [0]

        def asignar(nodo, nivel):
            if nodo is None:
                return
            asignar(nodo.izquierdo, nivel + 1)
            posiciones[id(nodo)] = (contador[0] * ancho_celda, nivel)
            contador[0] += 1
            asignar(nodo.derecho, nivel + 1)

        asignar(self.raiz, 0)

        alto = self.altura(self.raiz)
        filas = alto * 2 - 1
        columnas = contador[0] * ancho_celda + ancho_celda
        lienzo = [[" "] * columnas for _ in range(filas)]

        def escribir(fila, col, texto):
            for i, c in enumerate(texto):
                if 0 <= col + i < columnas:
                    lienzo[fila][col + i] = c

        def dibujar(nodo):
            if nodo is None:
                return
            col, nivel = posiciones[id(nodo)]
            escribir(nivel * 2, col, str(nodo.dato))
            for hijo, simbolo in ((nodo.izquierdo, "/"), (nodo.derecho, "\\")):
                if hijo is not None:
                    ccol, _ = posiciones[id(hijo)]
                    ini, fin = sorted((col, ccol))
                    for x in range(ini + 1, fin):
                        if lienzo[nivel * 2 + 1][x] == " ":
                            lienzo[nivel * 2 + 1][x] = "-"
                    lienzo[nivel * 2 + 1][ccol] = simbolo
                    dibujar(hijo)

        dibujar(self.raiz)
        print()
        for fila in lienzo:
            print("  " + "".join(fila).rstrip())
        print()

    def buscar(self, valor, nodo="raiz"):
        if nodo == "raiz":
            nodo = self.raiz
        if nodo is None or nodo.dato == valor:
            return nodo
        if valor < nodo.dato:
            return self.buscar(valor, nodo.izquierdo)
        return self.buscar(valor, nodo.derecho)

    def nivel_de(self, valor):
        actual, nivel = self.raiz, 1
        while actual is not None:
            if valor == actual.dato:
                return nivel
            actual = actual.izquierdo if valor < actual.dato else actual.derecho
            nivel += 1
        return 0

    def pre_orden(self, nodo="raiz", resultado=None):
        if nodo == "raiz":
            nodo, resultado = self.raiz, []
            self.pre_orden(nodo, resultado)
            return resultado
        if nodo is None:
            return
        resultado.append(nodo.dato)
        self.pre_orden(nodo.izquierdo, resultado)
        self.pre_orden(nodo.derecho, resultado)

    def in_orden(self, nodo="raiz", resultado=None):
        if nodo == "raiz":
            nodo, resultado = self.raiz, []
            self.in_orden(nodo, resultado)
            return resultado
        if nodo is None:
            return
        self.in_orden(nodo.izquierdo, resultado)
        resultado.append(nodo.dato)
        self.in_orden(nodo.derecho, resultado)

    def post_orden(self, nodo="raiz", resultado=None):
        if nodo == "raiz":
            nodo, resultado = self.raiz, []
            self.post_orden(nodo, resultado)
            return resultado
        if nodo is None:
            return
        self.post_orden(nodo.izquierdo, resultado)
        self.post_orden(nodo.derecho, resultado)
        resultado.append(nodo.dato)

    def busca_menor(self, nodo):
        while nodo is not None and nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def busca_mayor(self, nodo):
        while nodo is not None and nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo

    def eliminar_predecesor(self, x):
        if self.buscar(x) is None:
            print(f"  El valor {x} no existe en el árbol.")
            return False
        self.raiz = self._eliminar_pred(x, self.raiz)
        return True

    def _eliminar_pred(self, x, nodo):
        if nodo is None:
            return None
        if x < nodo.dato:
            nodo.izquierdo = self._eliminar_pred(x, nodo.izquierdo)
        elif x > nodo.dato:
            nodo.derecho = self._eliminar_pred(x, nodo.derecho)
        else:
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            pred = self.busca_mayor(nodo.izquierdo)
            nodo.dato = pred.dato
            nodo.izquierdo = self._eliminar_pred(pred.dato, nodo.izquierdo)
        return nodo

    def eliminar_sucesor(self, x):
        if self.buscar(x) is None:
            print(f"  El valor {x} no existe en el árbol.")
            return False
        self.raiz = self._eliminar_suc(x, self.raiz)
        return True

    def _eliminar_suc(self, x, nodo):
        if nodo is None:
            return None
        if x < nodo.dato:
            nodo.izquierdo = self._eliminar_suc(x, nodo.izquierdo)
        elif x > nodo.dato:
            nodo.derecho = self._eliminar_suc(x, nodo.derecho)
        else:
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            suc = self.busca_menor(nodo.derecho)
            nodo.dato = suc.dato
            nodo.derecho = self._eliminar_suc(suc.dato, nodo.derecho)
        return nodo

    def recorrido_niveles(self):
        resultado = []
        if self.raiz is None:
            return resultado
        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()
            resultado.append(actual.dato)
            if actual.izquierdo is not None:
                cola.append(actual.izquierdo)
            if actual.derecho is not None:
                cola.append(actual.derecho)
        return resultado

    def altura(self, nodo="raiz"):
        if nodo == "raiz":
            nodo = self.raiz
        if nodo is None:
            return 0
        return 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))

    def contar_hojas(self, nodo="raiz"):
        if nodo == "raiz":
            nodo = self.raiz
        if nodo is None:
            return 0
        if nodo.izquierdo is None and nodo.derecho is None:
            return 1
        return self.contar_hojas(nodo.izquierdo) + self.contar_hojas(nodo.derecho)

    def contar_nodos(self, nodo="raiz"):
        if nodo == "raiz":
            nodo = self.raiz
        if nodo is None:
            return 0
        return self.contar_nodos(nodo.izquierdo) + self.contar_nodos(nodo.derecho) + 1

    def grado(self, nodo="raiz"):
        if nodo == "raiz":
            nodo = self.raiz
        if nodo is None:
            return 0
        g = (nodo.izquierdo is not None) + (nodo.derecho is not None)
        return max(g, self.grado(nodo.izquierdo), self.grado(nodo.derecho))

    def es_completo(self):
        if self.raiz is None:
            return True
        cola = deque([self.raiz])
        hubo_hueco = False
        while cola:
            actual = cola.popleft()
            for hijo in (actual.izquierdo, actual.derecho):
                if hijo is None:
                    hubo_hueco = True
                else:
                    if hubo_hueco:
                        return False
                    cola.append(hijo)
        return True

    def es_lleno(self, nodo="raiz"):
        if nodo == "raiz":
            nodo = self.raiz
        if nodo is None:
            return True
        if nodo.izquierdo is None and nodo.derecho is None:
            return True
        if nodo.izquierdo is not None and nodo.derecho is not None:
            return self.es_lleno(nodo.izquierdo) and self.es_lleno(nodo.derecho)
        return False

    def eliminar_arbol(self):
        self.podar_arbol(self.raiz)
        self.raiz = None


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  Entrada inválida: escribe un número entero.")


def menu():
    print("\n========== ÁRBOL BINARIO DE BÚSQUEDA ==========")
    print(" [1]  Insertar elemento")
    print(" [2]  Mostrar árbol acostado (raíz a la izquierda)")
    print(" [3]  Graficar árbol completo")
    print(" [4]  Buscar un elemento")
    print(" [5]  Recorrido PreOrden")
    print(" [6]  Recorrido InOrden")
    print(" [7]  Recorrido PostOrden")
    print(" [8]  Eliminar nodo (PREDECESOR)")
    print(" [9]  Eliminar nodo (SUCESOR)")
    print(" [10] Recorrido por niveles (Amplitud)")
    print(" [11] Altura del árbol")
    print(" [12] Cantidad de hojas")
    print(" [13] Cantidad de nodos")
    print(" [14] Grado del árbol")
    print(" [15] ¿Es árbol binario completo?")
    print(" [16] ¿Es árbol binario lleno?")
    print(" [17] Eliminar el árbol")
    print(" [18] Cargar datos de ejemplo (8, 3, 1, 20, 5, 10, 7, 4)")
    print(" [0]  Salir")
    return leer_entero("Opción: ")


def main():
    arbol = Arbol()
    while True:
        opcion = menu()

        if opcion == 0:
            print("Fin del programa.")
            break
        elif opcion == 1:
            arbol.insertar_nodo(leer_entero("  Valor a insertar: "))
        elif opcion == 18:
            for v in (8, 3, 1, 20, 5, 10, 7, 4):
                arbol.insertar_nodo(v)
            print("  Datos de ejemplo cargados.")
        elif arbol.es_vacio() and opcion in range(2, 18):
            print("  El árbol está vacío. Inserta elementos primero.")
        elif opcion == 2:
            print()
            arbol.muestra_acostado()
        elif opcion == 3:
            arbol.graficar_arbol()
        elif opcion == 4:
            v = leer_entero("  Valor a buscar: ")
            if arbol.buscar(v):
                print(f"  El valor {v} SÍ está en el árbol (nivel {arbol.nivel_de(v)}).")
            else:
                print(f"  El valor {v} NO está en el árbol.")
        elif opcion == 5:
            print("  PreOrden :", " - ".join(map(str, arbol.pre_orden())))
        elif opcion == 6:
            print("  InOrden  :", " - ".join(map(str, arbol.in_orden())))
        elif opcion == 7:
            print("  PostOrden:", " - ".join(map(str, arbol.post_orden())))
        elif opcion == 8:
            if arbol.eliminar_predecesor(leer_entero("  Valor a eliminar: ")):
                print("  Nodo eliminado (predecesor).")
        elif opcion == 9:
            if arbol.eliminar_sucesor(leer_entero("  Valor a eliminar: ")):
                print("  Nodo eliminado (sucesor).")
        elif opcion == 10:
            print("  Por niveles:", " - ".join(map(str, arbol.recorrido_niveles())))
        elif opcion == 11:
            print("  Altura del árbol:", arbol.altura())
        elif opcion == 12:
            print("  Cantidad de hojas:", arbol.contar_hojas())
        elif opcion == 13:
            print("  Cantidad de nodos:", arbol.contar_nodos())
        elif opcion == 14:
            print("  Grado del árbol:", arbol.grado())
        elif opcion == 15:
            print("  ¿Es completo?", "SÍ" if arbol.es_completo() else "NO")
        elif opcion == 16:
            print("  ¿Es lleno?", "SÍ" if arbol.es_lleno() else "NO")
        elif opcion == 17:
            arbol.eliminar_arbol()
            print("  Árbol eliminado.")
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()
