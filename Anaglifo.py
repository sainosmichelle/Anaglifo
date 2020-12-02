# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:44:40 2020

@author: Michelle Sainos
"""

from tkinter import Tk, Canvas, ALL,TOP,BOTH, W, N, E, S, NW, Menu, Label, Scale, DoubleVar, HORIZONTAL
from tkinter.ttk import Frame, Button, Label, Style, Notebook
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence, ImageOps, ImageEnhance
import optparse
import numpy as np
import imutils
import matplotlib.pyplot as plt


#CREACION DE CLASE: Anaglifo que hereda de la clase Frame de tk
class Anaglifo(Frame):
    #Metodo de incicialización de la clase
    def __init__(self):
        #esta instrucción hace que se autoejecute la inicializacion de Frame
        super().__init__()
        #Esta instruccion hace que se llame el método con todo lo de adentro de la ventana
        self.initUI()


    def initUI(self):
        #Aqui creo todos los widgets de la ventana:
        #Les pongo self.blabla para poder usar estos atributos en cualquier parte
        # de la clase (atributos globales)
        self.master.title("Anaglifo")
        self.pack(fill=BOTH, expand=True)
        
        
        self.menu = Menu(self)
        self.master.config(menu = self.menu)
        self.abrir = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label = 'Abrir', menu = self.abrir)
        self.abrir.add_command(label = 'Imagen Izquierda', command = self.IzqImagen)
        self.abrir.add_command(label = 'Imagen Derecha', command = self.DerImagen)
        
        self.guardar = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label = 'Guardar', menu = self.guardar)
        self.guardar.add_command(label = 'Guardar Anaglifo', command = self.guardarImagen)

        
        self.tab_parent = Notebook(self)
        self.tab1 = Frame(self.tab_parent)
        self.tab2 = Frame(self.tab_parent)
        self.tab_parent.add(self.tab1, text="Crudas")
        self.tab_parent.add(self.tab2, text="Anaglifo")
        self.tab_parent.pack(fill=BOTH, expand=True)
        
        self.tab1.columnconfigure(1, weight=1)
        self.tab1.columnconfigure(2, weight=1)
        self.tab1.columnconfigure(4, pad=7)
        self.tab1.rowconfigure(3, weight=1)
        self.tab1.rowconfigure(5, pad=7)
        
        self.tab2.columnconfigure(1, weight=1)
        self.tab2.columnconfigure(2, weight=1)
        self.tab2.columnconfigure(4, pad=7)
        self.tab2.rowconfigure(3, weight=1)
        self.tab2.rowconfigure(5, pad=7)
        
        self.area = Canvas(self.tab1)
        self.area.grid(row=1, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)
        self.area.config(scrollregion=self.area.bbox(ALL))
        


        self.area2 = Canvas(self.tab1)
        self.area2.grid(row=1, column=2, columnspan=2, rowspan=4,
            padx=5, sticky=W+E+S+N)
        
        self.areatab2 = Canvas(self.tab2)
        self.areatab2.grid(row=1, column=1, columnspan=2, rowspan=4,
            padx=5, sticky=W+E+S+N)
        #Creación de los botones y conexión de acciones con metodos
        cbtn = Button(self.tab1, text="Punto de Control", command=self.Distor)
        cbtn.grid(row=1, column=4)
        lbtn = Button(self.tab1, text="Generar Anaglifo", command=self.Anaglifo)
        lbtn.grid(row=2, column=4)
        
        #Creación de los botones y conexión de acciones con metodos
        lbl = Label(self.tab2, text="Brillo")
        lbl.grid(row=1, column=4, pady=4, padx=5)
        s1 = Scale(self.tab2, from_ = 1, to = 5, digits = 2, resolution = 0.1, 
           orient = HORIZONTAL, command=self.Brillo) 
        s1.grid(row=2, column=4)

        
    def rebootArea(self,img):
        """Método para resetear el tamaño del canvas
        donde se pondrá la imagen izquierda"""
        self.area = Canvas(self.tab1)
        self.area.grid(row=1, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=E+W+S+N)
        self.area.config(width=self.dsize[0], height=self.dsize[1],
                         scrollregion=self.area.bbox(ALL))
        
        img = img.resize(self.dsize)
        img = ImageTk.PhotoImage(image=img) 
        self.area.create_image(0,0,image=img,anchor="nw")
        self.area1canvas = self.area
        self.area = img
        
    def AreaSize(self):
        """Método para calcular las dimensiones de las imagenes en la ventana"""
        width = int(self.area.winfo_width())
        height = int(self.area.winfo_height())
        self.dsize = (width, height)
        
    def rebootArea2(self,img):
        """Método para resetear el tamaño del canvas
        donde se pondrá la imagen derecha"""
        self.areatab2 = Canvas(self.tab2)
        self.areatab2.grid(row=1, column=0, columnspan=2, rowspan=4,
            padx=5, sticky=W+E+S+N)
        self.AreaSize2()
        self.areatab2.config(width=self.dsize2[0], height=self.dsize2[1])
        img = img.resize(self.dsize2)      
        img = ImageTk.PhotoImage(image=img) 
        self.areatab2.create_image(0,0,image=img,anchor="nw")
        self.areatab2 = img
        
        
    def AreaSize2(self):
        """Método para calcular las dimensiones de las imagenes en la ventana"""
        width = int(self.areatab2.winfo_width())
        height = int(self.areatab2.winfo_height())
        self.dsize2 = (width, height)
        
    def IzqImagen(self):
        """Método para abrir la imagen izquierda"""
        # Metodo que se activa con la accion de darle clic al botón cargar
        image_name = filedialog.askopenfilename(initialdir="/",
                                                title="Select file",
                                                filetypes=(("jpeg files","*.jpeg"),
                                                           ("jpg files","*.jpg"),
                                                           ("png files","*.png"),
                                                          ("all files","*.*")))
        img = Image.open(image_name)
        self.left_img = img.convert("L")
        self.AreaSize()
        self.left_img = img.resize(self.dsize).convert("L")
        self.rebootArea(img)
        
        
        
    def DerImagen(self):
        """Método para abrir la imagen izquierda"""
        # Metodo que se activa con la accion de darle clic al botón cargar
        image_name = filedialog.askopenfilename(initialdir="/",
                                                title="Select file",
                                                filetypes=(("jpeg files","*.jpeg"),
                                                           ("jpg files","*.jpg"),
                                                           ("png files","*.png"),
                                                          ("all files","*.*")))
        img = Image.open(image_name)
        self.right_img = img.convert("L")        
        self.area2 = Canvas(self.tab1)
        self.area2.grid(row=1, column=2, columnspan=2, rowspan=4,
            padx=5, sticky=W+E+S+N)
        self.area2.config(width=self.dsize[0], height=self.dsize[1])
        self.area2.bind('<Button-1>', self.printcoordsDer)
        img = img.resize(self.dsize)
        self.right_img = img.resize(self.dsize).convert("L")
        img = ImageTk.PhotoImage(image=img) 
        self.area2.create_image(0,0,image=img,anchor="nw")
        self.area2canvas = self.area2
        self.area2 = img
   

    def printcoordsIzq(self, event):
        """Punto de control izquierdo"""
        self.xIzq = event.x
        self.yIzq = event.y
        print (event.x,event.y)
        self.area1canvas.create_oval(self.xIzq-5, self.yIzq-5, self.xIzq+5, self.yIzq+5, 
                                     outline = "red", fill = "red", width = 2)
        try:
            self.ImagenesNuevas()
        except:
            pass
            

        
    def printcoordsDer(self, event):
        """Punto de control derecho"""
        self.xDer = event.x
        self.yDer = event.y
        print (event.x,event.y)
        self.area2canvas.create_oval(self.xDer-5, self.yDer-5, self.xDer+5, self.yDer+5, 
                                     outline = "red", fill = "red", width = 2)
        try:
            self.ImagenesNuevas()
        except:
            pass

                
    def Distor(self):
        """Boton de puntos de control"""
        self.area1canvas.bind('<Button-1>', self.printcoordsIzq)
        self.area2canvas.bind('<Button-1>', self.printcoordsDer)
        
        
    def ImagenesNuevas(self):
        """Corrección de distancia en imágenes"""
        m = self.dsize[0] 
        n = self.dsize[1]
        x1 = self.xIzq
        x2 = self.xDer
        y1 = self.yIzq
        y2 = self.yDer
        eta = np.abs(y2-y1)
        w = np.abs(x1-x2)
        v = n-eta
        u = m-w
        #print("n", n)
        #print("m", m)
        #print("w", w)
        #print("eta", eta)
        #print("u", u)
        #print("v", v)
        mat  = np.zeros((self.dsize[1], self.dsize[0]))
        #print("mat",mat.shape)
        if x1>=x2:
            dim = np.array(self.right_img)
            if y2 >= y1:
                #print("1")
                mat[:v, w:] = dim[eta:,:mat[:v, w:].shape[1]]
            elif y1>y2:
                #print("2")
                mat[eta:,w:] = dim[:mat[eta:,w:].shape[0],:mat[eta:,w:].shape[1]]
                
            self.right_img = Image.fromarray(mat.astype('uint8'), 'L')
        else:
            iim = np.array(self.left_img)
            if y2 >= y1:
                #print("3") 
                mat[eta:, w:] = iim[:mat[eta:, w:].shape[0],:mat[eta:, w:] .shape[1]]
            elif y1>y2:
                #print("4")
                mat[:v, w:] = iim[eta:,:mat[:v, w:].shape[1]]
                
            self.left_img = Image.fromarray(mat.astype('uint8'), 'L')
        #print(mat)
        #plt.imshow(mat, cmap='gray')
        #plt.show()
    
    
    def Anaglifo(self):
        """Generación de anaglifo a partir de 2 imágenes"""
        self.tab_parent.select(self.tab2)
        self.size = self.left_img.size
        print(self.left_img.height, self.left_img.width)
        print(self.right_img.height, self.right_img.width)
        red_img = ImageOps.colorize(self.left_img,(0,0,0),(255,0,0))
        cian_img = ImageOps.colorize(self.right_img,(0,0,0),(0,255,255))
        self.blend = Image.blend(red_img,cian_img,0.5)
        img=self.blend
        self.areatab2 = Label(self.tab2)
        self.areatab2.grid(row=1, column=2, columnspan=2, rowspan=4,
            padx=5, sticky=W+E+S+N)
        #img = img.resize(self.dsize)
        img = ImageTk.PhotoImage(image=img) 
        self.areatab2.configure(image=img)
        self.areatab2 = img
        
 
    def Brillo(self,val):
        """Modificación del brillo"""
        brightness = ImageEnhance.Brightness(self.blend)
        self.blend2 = brightness.enhance(float(val))
        img=self.blend2
        self.areatab2 = Label(self.tab2)
        self.areatab2.grid(row=1, column=2, columnspan=2, rowspan=4,
            padx=5, sticky=W+E+S+N)
        img = img.resize(self.dsize)
        img = ImageTk.PhotoImage(image=img) 
        self.areatab2.configure(image=img)
        self.areatab2 = img
    
        
    def guardarImagen(self):
        """Guardar el anaglifo en el sistema"""
        # Metodo que se activa con la accion de darle clic al botón guardar
        file_name = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        self.blend.save(file_name.name)
        

        
def main():
    #Función que me crea a la ventana
    root = Tk()
    root.geometry("1500x600+200+200")
    #Aqui creo al objeto que va dentro de la ventana
    app = Anaglifo()
    #Para que no se cierre
    root.mainloop()


#Esto significa que solo abre la ventana si estoy corriendo el programa principal
if __name__ == '__main__':
    main()