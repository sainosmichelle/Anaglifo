<h1> Land cover classification </h1>
<br/>
<img src="https://github.com/sainosmichelle/Anaglifo/blob/main/images/retorno2.PNG"
  width="500"
  height="400">

<p>Interfaz de usuario para convertir un par estereoscópico en un anaglifo. El proceso interno de la generación del anaglifo se divide en tres partes: correción de distancia de las imágenes mediante puntos de control, saturación de cada imagen del par estereoscópico con un tinte (rojo o cyan) y la fusión de las imágenes para crear el anaglifo. </p>

<p>La interfaz básicamente usa los módulos de Tkinter  y  Pillow.  La  interfaz  consiste  de una ventana con dos tabuladores. En el primer tabulador se cargan las imágenes (izquierda y derecha) que correspondenal par esteroscópico. En este tabulador también se realizan las  debidas  correcciones  de  desplazamiento  mediante  unpunto  de  control  y  posteriormente  se  genera  el  anaglifo. En  el  segundo  tabulador  se  muestran  el  resultado  de  este proceso. Para generar el anaglifo se transforman las imágenes estereoscópicas RGB a un solo canal en escala de grises.</p>

<h2>Getting Started</h2>
The code is developed in python 3, you can run it in Colab or in your local Anaconda Enviroment.

<p>If you run it in your local enviroment make sure to use your GPU and verify if the following packages are installed</p>

```
pip install PIL
pip install Tkinter
conda install numpy
```

<h2>Corrección de desplazamiento</h2>
 Las  imágenes  estereoscópicas  no  abarcan  exactamente  la  misma  área,  i.e.  la  imagen izquerda  tiene  un  área  que  no  cubre  la  imagen  derecha  y visceversa. Esto representa un problema ya que si se realiza la fusión de ambas imágenes se observará que no coinciden en ningún punto y no se generará un buen anaglifo. La forma en la que se abordó este problema fue a través de un punto de control mediante el cual se asegura que ambas imágenes coinciden.

 <img src="https://github.com/sainosmichelle/Anaglifo/blob/main/images/retorno1.PNG"
  width="800"
  height="400">


<h2>Contributing</h2>
<p>Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.</p>
<h2>Authors</h2>
<ul>
<li> <b>Michelle Sainos Vizuett</b> <em>- Coder</it></em> </li>
</ul>
