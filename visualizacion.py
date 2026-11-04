# visualizacion_gui.py
import tkinter as tk
from tkinter import ttk
import time

# Importamos la lógica base
from canibales_logica import busqueda_bfs, obtener_sucesores, ESTADO_INICIAL, ESTADO_OBJETIVO

def busqueda_dfs_didactica():
    """DFS modificado para forzar una ruta subóptima y mostrar la diferencia empírica"""
    inicio_tiempo = time.perf_counter()
    pila = [(ESTADO_INICIAL, [])]
    visitados = {ESTADO_INICIAL}
    nodos_expandidos = 0
    
    while pila:
        estado_actual, camino = pila.pop()
        nodos_expandidos += 1
        
        if estado_actual == ESTADO_OBJETIVO:
            tiempo_total = time.perf_counter() - inicio_tiempo
            return camino, nodos_expandidos, tiempo_total
            
        sucesores = obtener_sucesores(estado_actual)
        for sucesor, accion in reversed(sucesores):
            if sucesor not in visitados:
                visitados.add(sucesor)
                nuevo_camino = camino + [(estado_actual, accion, sucesor)]
                pila.append((sucesor, nuevo_camino))
                
    return None, nodos_expandidos, time.perf_counter() - inicio_tiempo


class CanibalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Misioneros y Caníbales - Fases de Pensamiento y Ejecución")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        # Estados de animación
        self.animando_bfs = False
        self.animando_dfs = False
        self.fase_pensamiento = False
        
        # Obtener resultados al vuelo
        self.res_bfs = busqueda_bfs()
        self.res_dfs = busqueda_dfs_didactica()
        
        self.camino_bfs = self.res_bfs[0]
        self.camino_dfs = self.res_dfs[0]
        self.total_nodos_bfs = self.res_bfs[1]
        self.total_nodos_dfs = self.res_dfs[1]

        self.construir_interfaz()
        self.dibujar_orilla(self.canvas_bfs, (3, 3, 1), 0, "Esperando iniciar...")
        self.dibujar_orilla(self.canvas_dfs, (3, 3, 1), 0, "Esperando iniciar...")

    def construir_interfaz(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.btn_iniciar = tk.Button(left_frame, text="▶ Iniciar Simulación (Pensar -> Ejecutar)", 
                                     bg="#FF9800", fg="white", font=("Arial", 12, "bold"), 
                                     command=self.iniciar_animacion)
        self.btn_iniciar.pack(fill=tk.X, pady=(0, 5))

        # Leyenda
        leyenda_frame = tk.Frame(left_frame)
        leyenda_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(leyenda_frame, text="Leyenda:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(leyenda_frame, text="M", font=("Arial", 10, "bold"), fg="white", bg="#1976D2", width=3).pack(side=tk.LEFT)
        tk.Label(leyenda_frame, text=" = Misioneros", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(leyenda_frame, text="C", font=("Arial", 10, "bold"), fg="white", bg="#D32F2F", width=3).pack(side=tk.LEFT)
        tk.Label(leyenda_frame, text=" = Caníbales", font=("Arial", 10)).pack(side=tk.LEFT)

        # Canvas BFS
        tk.Label(left_frame, text="Búsqueda en Anchura (BFS) ", font=("Arial", 11, "bold")).pack()
        self.canvas_bfs = tk.Canvas(left_frame, width=500, height=220, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas_bfs.pack(pady=(0, 10))

        # Canvas DFS
        tk.Label(left_frame, text="Búsqueda en Profundidad (DFS) ", font=("Arial", 11, "bold")).pack()
        self.canvas_dfs = tk.Canvas(left_frame, width=500, height=220, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas_dfs.pack()

        # Zona Derecha
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(right_frame, text="Acciones BFS", font=("Arial", 10, "bold")).pack()
        self.tree_bfs = self.crear_tabla_acciones(right_frame, 7)
        self.tree_bfs.pack(fill=tk.X, pady=(0, 10))

        tk.Label(right_frame, text="Acciones DFS", font=("Arial", 10, "bold")).pack()
        self.tree_dfs = self.crear_tabla_acciones(right_frame, 7)
        self.tree_dfs.pack(fill=tk.X, pady=(0, 20))

        tk.Label(right_frame, text="Tabla Comparativa (Benchmarking)", font=("Arial", 12, "bold")).pack()
        cols_comp = ("Algoritmo", "Nodos", "Tiempo", "Longitud")
        self.tree_comp = ttk.Treeview(right_frame, columns=cols_comp, show="headings", height=3)
        for col, texto in zip(cols_comp, ["Algoritmo", "Nodos Exp.", "Tiempo (s)", "Pasos"]):
            self.tree_comp.heading(col, text=texto)
            self.tree_comp.column(col, width=100, anchor="center")
        self.tree_comp.pack(fill=tk.X)

    def crear_tabla_acciones(self, parent, height):
        cols = ("Paso", "Origen", "Acción", "Destino")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=height)
        for col, texto in zip(cols, ["#", "Origen", "Acción", "Destino"]):
            tree.heading(col, text=texto)
        tree.column("Paso", width=30, anchor="center")
        tree.column("Origen", width=80, anchor="center")
        tree.column("Acción", width=170, anchor="center")
        tree.column("Destino", width=80, anchor="center")
        return tree

    def dibujar_entorno_base(self, canvas, nodos_actuales, estado_texto):
        canvas.delete("all")
        # Escenario
        canvas.create_rectangle(0, 0, 120, 220, fill="#8BC34A", outline="") 
        canvas.create_rectangle(120, 0, 380, 220, fill="#4FC3F7", outline="") 
        canvas.create_rectangle(380, 0, 500, 220, fill="#8BC34A", outline="")
        
        # HUD: Nodos Expandidos (Esquina superior izquierda)
        canvas.create_rectangle(5, 5, 180, 30, fill="#333", outline="")
        canvas.create_text(92, 17, text=f"🧠 Nodos Expandidos: {nodos_actuales}", fill="white", font=("Arial", 9, "bold"))
        
        # HUD: Estado de la simulación (Centro superior)
        color_texto = "#FF9800" if "Pensando" in estado_texto else "#4CAF50"
        canvas.create_text(250, 17, text=estado_texto, fill=color_texto, font=("Arial", 11, "bold"))

    def dibujar_personajes(self, canvas, x_base, y_base, cantidad, tipo):
        color = "#1976D2" if tipo == "M" else "#D32F2F"
        for i in range(cantidad):
            x = x_base + (i * 28)
            canvas.create_oval(x, y_base, x+24, y_base+24, fill=color, outline="white")
            canvas.create_text(x+12, y_base+12, text=tipo, fill="white", font=("Arial", 9, "bold"))

    def dibujar_bote(self, canvas, x_bote, y_bote, misioneros=0, canibales=0):
        canvas.create_polygon(x_bote-10, y_bote, x_bote+90, y_bote, 
                              x_bote+70, y_bote+30, x_bote+10, y_bote+30, 
                              fill="#795548", outline="black", width=2)
        slots = [(x_bote + 5, y_bote - 20), (x_bote + 45, y_bote - 20)]
        slot_idx = 0
        for _ in range(misioneros):
            self.dibujar_personajes(canvas, slots[slot_idx][0], slots[slot_idx][1], 1, "M")
            slot_idx += 1
        for _ in range(canibales):
            self.dibujar_personajes(canvas, slots[slot_idx][0], slots[slot_idx][1], 1, "C")
            slot_idx += 1

    def dibujar_orilla(self, canvas, estado, nodos, estado_texto):
        self.dibujar_entorno_base(canvas, nodos, estado_texto)
        m_izq, c_izq, b_izq = estado
        
        self.dibujar_personajes(canvas, 15, 45, m_izq, "M")
        self.dibujar_personajes(canvas, 15, 95, c_izq, "C")
        self.dibujar_personajes(canvas, 395, 45, 3 - m_izq, "M")
        self.dibujar_personajes(canvas, 395, 95, 3 - c_izq, "C")
        
        x_bote = 125 if b_izq == 1 else 295
        self.dibujar_bote(canvas, x_bote, 150)

    def dibujar_transito(self, canvas, paso, nodos, estado_texto):
        self.dibujar_entorno_base(canvas, nodos, estado_texto)
        origen, _, destino = paso
        m_o, c_o, _ = origen
        m_d, c_d, _ = destino
        
        self.dibujar_personajes(canvas, 15, 45, min(m_o, m_d), "M")
        self.dibujar_personajes(canvas, 15, 95, min(c_o, c_d), "C")
        self.dibujar_personajes(canvas, 395, 45, 3 - max(m_o, m_d), "M")
        self.dibujar_personajes(canvas, 395, 95, 3 - max(c_o, c_d), "C")
        
        self.dibujar_bote(canvas, 210, 150, abs(m_d - m_o), abs(c_d - c_o))

    def iniciar_animacion(self):
        if self.animando_bfs or self.animando_dfs or self.fase_pensamiento: return
        self.fase_pensamiento = True
        self.btn_iniciar.config(state=tk.DISABLED)
        
        # Limpiar tablas
        for item in self.tree_bfs.get_children(): self.tree_bfs.delete(item)
        for item in self.tree_dfs.get_children(): self.tree_dfs.delete(item)
        for item in self.tree_comp.get_children(): self.tree_comp.delete(item)

        # FASE 1: Animar la expansión de nodos (Pensamiento)
        self.animar_pensamiento(0, 0)

    def animar_pensamiento(self, contador_bfs, contador_dfs):
        # Aumentamos los contadores visuales hasta llegar a los nodos reales
        bfs_listo = contador_bfs >= self.total_nodos_bfs
        dfs_listo = contador_dfs >= self.total_nodos_dfs
        
        if bfs_listo and dfs_listo:
            self.fase_pensamiento = False
            self.animando_bfs = True
            self.animando_dfs = True
            
            # FASE 2: Iniciar viaje
            self.dibujar_orilla(self.canvas_bfs, (3, 3, 1), self.total_nodos_bfs, "¡Ruta Encontrada! Ejecutando...")
            self.dibujar_orilla(self.canvas_dfs, (3, 3, 1), self.total_nodos_dfs, "¡Ruta Encontrada! Ejecutando...")
            
            self.root.after(800, self.animar_bfs_ciclo, 0, True)
            self.root.after(800, self.animar_dfs_ciclo, 0, True)
            return

        # Incrementar contadores
        if not bfs_listo: contador_bfs += 1
        if not dfs_listo: contador_dfs += 1

        self.dibujar_orilla(self.canvas_bfs, (3, 3, 1), contador_bfs, "Fase 1: Pensando (Expandiendo Memoria)...")
        self.dibujar_orilla(self.canvas_dfs, (3, 3, 1), contador_dfs, "Fase 1: Pensando (Expandiendo Memoria)...")

        # Repetir súper rápido para efecto visual de "Cálculo de CPU"
        self.root.after(50, self.animar_pensamiento, contador_bfs, contador_dfs)

    def verificar_fin_general(self):
        if not self.animando_bfs and not self.animando_dfs:
            self.tree_comp.insert("", "end", values=("BFS (Anchura)", self.total_nodos_bfs, f"{self.res_bfs[2]:.6f}", len(self.camino_bfs)))
            self.tree_comp.insert("", "end", values=("DFS (Profundidad)", self.total_nodos_dfs, f"{self.res_dfs[2]:.6f}", len(self.camino_dfs)))
            self.btn_iniciar.config(state=tk.NORMAL)

    def animar_bfs_ciclo(self, i, transito):
        if i >= len(self.camino_bfs):
            self.dibujar_orilla(self.canvas_bfs, ESTADO_OBJETIVO, self.total_nodos_bfs, "✅ META ALCANZADA (Óptimo)")
            self.animando_bfs = False
            self.verificar_fin_general()
            return

        if transito:
            self.dibujar_transito(self.canvas_bfs, self.camino_bfs[i], self.total_nodos_bfs, "Fase 2: Ejecutando...")
            self.root.after(500, self.animar_bfs_ciclo, i, False)
        else:
            origen, accion, destino = self.camino_bfs[i]
            self.dibujar_orilla(self.canvas_bfs, destino, self.total_nodos_bfs, "Fase 2: Ejecutando...")
            self.tree_bfs.insert("", "end", values=(i + 1, str(origen), accion, str(destino)))
            self.tree_bfs.yview_moveto(1)
            self.root.after(500, self.animar_bfs_ciclo, i + 1, True)

    def animar_dfs_ciclo(self, i, transito):
        if i >= len(self.camino_dfs):
            self.dibujar_orilla(self.canvas_dfs, ESTADO_OBJETIVO, self.total_nodos_dfs, "✅ META ALCANZADA (Subóptimo)")
            self.animando_dfs = False
            self.verificar_fin_general()
            return

        if transito:
            self.dibujar_transito(self.canvas_dfs, self.camino_dfs[i], self.total_nodos_dfs, "Fase 2: Ejecutando...")
            self.root.after(500, self.animar_dfs_ciclo, i, False)
        else:
            origen, accion, destino = self.camino_dfs[i]
            self.dibujar_orilla(self.canvas_dfs, destino, self.total_nodos_dfs, "Fase 2: Ejecutando...")
            self.tree_dfs.insert("", "end", values=(i + 1, str(origen), accion, str(destino)))
            self.tree_dfs.yview_moveto(1)
            self.root.after(500, self.animar_dfs_ciclo, i + 1, True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CanibalesApp(root)
    root.mainloop()