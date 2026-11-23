# -*- coding: utf-8 -*-
"""Genera el informe técnico en PDF a partir de las figuras que produce el notebook.

Uso:
    python generar_informe.py
    REPO_URL="https://github.com/usuario/repositorio" python generar_informe.py

Antes de entregar, completa los datos de la portada (AUTOR, ASIGNATURA, etc.) y la URL del repositorio.
"""
import os
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

# ------------------------------------------------------------------ datos editables de la portada
TITULO = "Visualización del catálogo de Netflix"
SUBTITULO = "Jerarquías, redes, distribuciones y series de tiempo con Python"
AUTOR = "[Nombre y apellido del estudiante]"
ASIGNATURA = "[Nombre de la asignatura]"
DOCENTE = "[Nombre del docente]"
INSTITUCION = "[Institución]"
FECHA = "Noviembre de 2026"
REPO_URL = os.environ.get("REPO_URL", "https://github.com/TU_USUARIO/visualizacion-netflix")
SALIDA = "Informe_Tecnico_Visualizacion_Netflix.pdf"
FIG = "figuras"

# ------------------------------------------------------------------ estilos
ss = getSampleStyleSheet()
AZUL = colors.HexColor("#1f3a5f")
base = ParagraphStyle("base", parent=ss["Normal"], fontName="Helvetica", fontSize=10.2, leading=14.6,
                      alignment=TA_JUSTIFY, spaceAfter=7)
h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=AZUL,
                    spaceBefore=14, spaceAfter=8, alignment=0, keepWithNext=1)
h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=AZUL,
                    spaceBefore=9, spaceAfter=5, alignment=0, keepWithNext=1)
pie = ParagraphStyle("pie", parent=base, fontName="Helvetica-Oblique", fontSize=8.6, leading=11.5,
                     textColor=colors.HexColor("#444444"), alignment=TA_CENTER, spaceAfter=10)
celda = ParagraphStyle("celda", parent=base, fontSize=8.8, leading=11.5, alignment=0, spaceAfter=0)
celda_b = ParagraphStyle("celda_b", parent=celda, fontName="Helvetica-Bold")
bullet = ParagraphStyle("bullet", parent=base, leftIndent=14, bulletIndent=2, spaceAfter=3)
ref = ParagraphStyle("ref", parent=base, fontSize=9, leading=12.2, leftIndent=14, firstLineIndent=-14,
                     alignment=0, spaceAfter=4)

def P(t, s=base): return Paragraph(t, s)
def B(t): return Paragraph(t, bullet, bulletText="\u2022")

def figura(archivo, ancho_cm, leyenda):
    ruta = os.path.join(FIG, archivo)
    w, h = PILImage.open(ruta).size
    ancho = ancho_cm * cm
    return KeepTogether([Image(ruta, width=ancho, height=ancho * h / w), Spacer(1, 3), P(leyenda, pie)])

def tabla(filas, anchos, cabecera=True, tam=8.8):
    datos = [[Paragraph(str(c), celda_b if (cabecera and i == 0) else celda) for c in f] for i, f in enumerate(filas)]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1 if cabecera else 0)
    est = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c2cc")),
           ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if cabecera:
        est.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6edf5")))
    t.setStyle(TableStyle(est))
    return t

# ------------------------------------------------------------------ portada y pie de página
def portada(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(AZUL); canvas.rect(0, h - 7.5 * cm, w, 7.5 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11); canvas.drawString(2.5 * cm, h - 2.3 * cm, INSTITUCION)
    canvas.setFont("Helvetica-Bold", 26); canvas.drawString(2.5 * cm, h - 4.7 * cm, "Informe técnico")
    canvas.setFont("Helvetica", 13); canvas.drawString(2.5 * cm, h - 5.9 * cm, "Visualización de Datos")
    canvas.restoreState()

def pagina(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5); canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2.2 * cm, 1.3 * cm, "Visualización del catálogo de Netflix")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.3 * cm, f"Página {doc.page}")
    canvas.restoreState()

doc = BaseDocTemplate(SALIDA, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                      topMargin=2.0 * cm, bottomMargin=2.2 * cm,
                      title="Informe técnico: visualización del catálogo de Netflix", author=AUTOR)
marco = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")
doc.addPageTemplates([PageTemplate(id="portada", frames=[marco], onPage=portada, autoNextPageTemplate="cuerpo"),
                      PageTemplate(id="cuerpo", frames=[marco], onPage=pagina)])
S = []

# ------------------------------------------------------------------ portada
S += [Spacer(1, 6.2 * cm),
      Paragraph(TITULO, ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=22, leading=27,
                                       textColor=AZUL, alignment=0, spaceAfter=6)),
      Paragraph(SUBTITULO, ParagraphStyle("st", parent=base, fontSize=13, leading=17, alignment=0,
                                          textColor=colors.HexColor("#444444"), spaceAfter=30)),
      tabla([["Autor", AUTOR], ["Asignatura", ASIGNATURA], ["Docente", DOCENTE], ["Fecha", FECHA],
             ["Dataset", "Netflix Movies and TV Shows (7,787 títulos)"],
             ["Código fuente", f'<link href="{REPO_URL}" color="#1a5fb4">{REPO_URL}</link>']],
            [3.6, 12.8], cabecera=False, tam=10),
      PageBreak()]

# ------------------------------------------------------------------ 1. dataset
S += [P("1. Descripción del dataset", h1),
      P("El dataset es <i>Netflix Movies and TV Shows</i>, publicado en Kaggle y redistribuido en el repositorio "
        "TidyTuesday (semana del 20 de abril de 2021). Es de acceso libre y no requiere registro. Contiene 7,787 "
        "títulos descritos con 12 columnas y representa el catálogo estadounidense de Netflix hasta el 16 de enero "
        "de 2021. De los títulos, 5,377 son películas (69.1%) y 2,410 son series (30.9%)."),
      P("Lo elegí porque cumple los cuatro requisitos del trabajo con columnas que ya existen, sin construir datos "
        "artificiales:"),
      tabla([["Requisito", "Columnas", "Evidencia en el dataset"],
             ["Categórica con jerarquía", "type, rating, listed_in",
              "2 tipos, 4 públicos, 9 géneros (8 más \"Otros\")"],
             ["Conexiones o co-ocurrencias", "cast",
              "32,489 actores; dos actores se conectan si comparten título"],
             ["Cuantitativas continuas y discretas", "duration, release_year, date_added",
              "Duración en minutos (5,377 películas); rezago en años (7,777 títulos)"],
             ["Índice temporal", "date_added", "Altas mensuales entre 2008 y enero de 2021"]],
            [4.4, 4.2, 7.8]),
      Spacer(1, 8),
      P("<b>Preparación de los datos.</b> La fecha de incorporación llega como texto (por ejemplo "
        "\"August 14, 2020\") y se convirtió a fecha. La duración mezcla minutos (películas) y temporadas (series), "
        "así que se separó en dos columnas. Se creó el <i>rezago</i> como la diferencia entre el año de "
        "incorporación y el año de estreno; los 12 casos negativos, que corresponden a estrenos anunciados antes de "
        "publicarse, se fijaron en cero. La clasificación por edades (14 códigos) se agrupó en cuatro públicos: "
        "adultos, adolescentes, familiar y niños. Del género se tomó el primero de la lista y se conservaron los 8 "
        "más frecuentes; el resto pasó a \"Otros\" (1,937 títulos, 24.9%)."),
      P("<b>Limitaciones conocidas.</b> El catálogo es una captura puntual: los títulos que Netflix retiró antes de "
        "2021 no aparecen, de modo que los conteos de años anteriores probablemente subestiman las altas reales. "
        "Faltan datos en el reparto (718 títulos), el país (507) y la fecha de incorporación (10). El mes de enero de "
        "2021 está incompleto y se excluyó de la serie de tiempo."),

      # -------------------------------------------------------------- 2. teoría
      P("2. Justificación teórica", h1),
      P("2.1 Canales visuales y precisión perceptual", h2),
      P("Una visualización codifica variables en marcas (puntos, líneas, áreas) y canales (posición, longitud, "
        "área, color, grosor). Cleveland y McGill (1984) ordenaron los canales según la precisión con que las "
        "personas estiman cantidades: la posición sobre una escala común es la más precisa, seguida de la "
        "longitud, el ángulo, el área y, por último, la saturación y el matiz del color. Munzner (2014) añade que "
        "los canales de magnitud (posición, longitud, luminosidad) sirven para variables ordenadas, mientras que los "
        "de identidad (matiz, forma) sirven para categorías. Las cuatro visualizaciones del trabajo parten de esa "
        "regla: cada variable se asigna al canal que mejor se ajusta a su tipo."),
      P("2.2 Jerarquía: treemap y control del aspect ratio", h2),
      P("El treemap (Johnson y Shneiderman, 1991) representa una jerarquía mediante rectángulos anidados cuya área "
        "es proporcional a un valor. Su ventaja es que aprovecha todo el espacio y muestra tres niveles a la vez. "
        "Su costo es que codifica la magnitud con área, un canal poco preciso. Para reducir ese costo se usó el "
        "algoritmo <i>squarified</i> (Bruls et al., 2000), que minimiza la diferencia entre ancho y alto de cada "
        "rectángulo: los bloques casi cuadrados se comparan mejor que los alargados. En Plotly esto se controla con "
        "<font face='Courier'>tiling.packing=\"squarify\"</font> y <font face='Courier'>squarifyratio=1</font>, y el "
        "lienzo se fijó en 1100 x 680 px (relación 1.62:1). La legibilidad se resolvió limitando el segundo nivel a "
        "8 géneros más \"Otros\", separando los bloques con un margen de 3 px y ocultando las etiquetas que no caben "
        "en tamaño legible. El color usa una escala secuencial Viridis, perceptualmente uniforme y apta para "
        "daltonismo."),
      P("2.3 Redes y el problema de la bola de pelos", h2),
      P("En un grafo con miles de nodos y cientos de miles de aristas, el diagrama de nodos y enlaces se vuelve una "
        "mancha donde no se distingue ninguna estructura. Este fenómeno se conoce como <i>hairball</i>. Aquí el "
        "grafo completo tiene 32,489 nodos y 252,053 aristas. La estrategia aplicada combina seis medidas, "
        "descritas con detalle en la sección 4.2: filtrar aristas por peso, conservar solo las componentes "
        "conexas mayores, colorear por comunidad (modularidad, Newman, 2006), escalar los nodos por grado y "
        "rotular únicamente a los más conectados, apilar las aristas en capas según su peso, y calcular el "
        "layout Kamada-Kawai (Kamada y Kawai, 1989) por componente. En un layout de fuerzas la posición no "
        "tiene valor cuantitativo; solo importa la cercanía relativa."),
      P("2.4 Distribuciones: histograma, boxplot y asimetría", h2),
      P("El histograma muestra la forma completa de una distribución, incluidas las modas y la cola, pero depende "
        "del ancho de los intervalos. El boxplot (Tukey, 1977) resume la mediana, los cuartiles y los valores "
        "atípicos, y no detecta multimodalidad. Se combinan en un solo panel con el eje x compartido para que cada "
        "uno cubra la debilidad del otro. Los atípicos se identifican con la regla de Tukey, es decir, los datos "
        "que quedan fuera del intervalo [Q1 - 1.5 IQR, Q3 + 1.5 IQR]. La asimetría se mide con el coeficiente de "
        "asimetría (<i>skewness</i>) y el peso de las colas con la curtosis en exceso. Cuando hay asimetría fuerte, "
        "la mediana describe mejor el valor típico que la media."),
      P("2.5 Series de tiempo: tendencia, estacionalidad y ruptura", h2),
      P("Una serie mensual se puede descomponer en tendencia, ciclo estacional y residuo. La tendencia se estimó "
        "con una media móvil centrada de 12 meses, que elimina el ciclo anual. La estacionalidad se midió como el "
        "cociente entre cada mes y esa media móvil, promediado por mes calendario. Para buscar una ruptura se "
        "ajustaron dos rectas con un punto de corte variable y se conservó el corte que minimiza la suma de "
        "errores cuadrados. La interacción sigue el patrón de enfoque más contexto: selector de rango y "
        "minigráfico permiten acotar una ventana sin perder la vista global."),

      # -------------------------------------------------------------- 3. implementación
      P("3. Implementación", h1),
      P("Todo el análisis está en un único notebook de Jupyter, <font face='Courier'>Visualizacion_Netflix.ipynb"
        "</font>, comentado línea a línea y ejecutable de principio a fin. Las librerías usadas son pandas y numpy "
        "para los datos, Plotly Express y Plotly Graph Objects para las figuras interactivas, NetworkX para el "
        "grafo, Seaborn y Matplotlib para las distribuciones y SciPy para los estadísticos. El notebook lee el CSV "
        "directo desde GitHub y, si no hay conexión, usa la copia incluida en el repositorio. Plotly necesita un "
        "navegador instalado para exportar imágenes, así que las figuras de este informe son versiones estáticas "
        "equivalentes que el propio notebook dibuja con Matplotlib y los mismos datos (sección \"Apéndice\"). Las "
        "versiones interactivas se guardan como HTML en la carpeta <font face='Courier'>figuras/</font>."),

      # -------------------------------------------------------------- 4. resultados
      P("4. Interpretación analítica", h1),
      P("4.1 Jerarquía y composición", h2),
      figura("s01_treemap.png", 15.6,
             "Figura 1. Treemap del catálogo por tipo, público y género principal. El área indica la cantidad de "
             "títulos y el color el año de estreno promedio. Captura estática; la versión interactiva está en el notebook."),
      P("Las películas son el 69.1% del catálogo y las series el 30.9%. El bloque más grande es <i>Películas, "
        "Adultos, Dramas</i> con 773 títulos (9.9% del total). El contenido para adultos domina en ambos "
        "formatos, aunque con matices: 48.3% de las películas frente a 42.5% de las series. La diferencia mayor "
        "está en el público infantil, que pesa 14.1% en las series y solo 4.0% en las películas."),
      P("El color separa dos épocas. Los bloques de series son casi todos violeta oscuro, es decir, estrenos "
        "recientes: <i>Crime TV Shows</i> promedia 2017.9 y <i>Otros</i> de series para adultos, 2017.4. Las "
        "películas se reparten entre azules y verdes, con los bloques grandes entre 2011 y 2015 y <i>Action &amp; "
        "Adventure</i> para adolescentes (305 títulos) en 2008.2. Los bloques amarillos, en las películas "
        "familiares (promedios de 2001.4 y 2003.3), son el material más antiguo. En conjunto, el año de estreno "
        "promedio es 2012.9 para las películas y 2016.2 para las series."),
      P("Desde el punto de vista de la codificación, el área permite ver la composición anidada de un vistazo, "
        "pero no sirve para comparar con precisión bloques parecidos: distinguir 490 comedias de 363 títulos de "
        "acción exige leer el número. Tampoco muestra dispersión, porque un promedio de 2013 puede ocultar desde "
        "estrenos de 1990 hasta estrenos de 2020. Esa pregunta se responde en la sección 4.3."),

      KeepTogether([P("4.2 Relaciones y redes", h2), tabla([["Etapa de reducción", "Nodos", "Aristas", "Densidad"],
             ["Grafo completo (todas las parejas)", "32,489", "252,053", "0.0005"],
             ["Aristas con peso &gt;= 2 títulos", "3,741", "9,143", "0.0013"],
             ["Aristas con peso &gt;= 3 títulos", "889", "1,956", "0.0050"],
             ["Seis mayores componentes conexas", "346", "974", "0.0163"]],
            [8.0, 2.6, 2.8, 3.0]),
      Spacer(1, 4),
      P("Tabla 1. Efecto de cada filtro sobre el tamaño y la densidad del grafo.", pie)]),
      figura("s02_grafo.png", 15.6,
             "Figura 2. Red de co-ocurrencia de actores (346 nodos, 974 aristas, 15 comunidades). El color indica "
             "la comunidad, el tamaño el número de colaboradores y el grosor de la arista el número de títulos "
             "compartidos (3, 4 a 5, 6 o más)."),
      P("<b>Estrategia contra el hairball.</b> El código aplica seis medidas en cadena. Primero, descarta las "
        "parejas que coinciden en menos de 3 títulos (<font face='Courier'>PESO_MIN = 3</font>), porque casi todas "
        "las aristas del grafo completo son coincidencias de un solo título. Segundo, conserva las 6 componentes "
        "conexas mayores y elimina las parejas y tríos aislados. Tercero, detecta comunidades por modularidad y "
        "las colorea, de modo que el ojo agrupa sin seguir cada arista. Cuarto, escala cada nodo por su grado y "
        "etiqueta solo al actor más conectado de cada comunidad. Quinto, dibuja las aristas en tres capas de "
        "grosor y opacidad según su peso, con las débiles al fondo. Sexto, calcula el layout Kamada-Kawai por "
        "componente y las ubica en una cuadrícula para que no se superpongan. Con esto se pasa de 252,053 "
        "aristas a 974 y la densidad sube de 0.0005 a 0.016."),
      P("<b>Resultados.</b> La red se divide en varias islas. Las seis componentes tienen 164, 89, 38, 21, "
        "17 y 17 actores, y la modularidad (Q = 0.842) indica grupos muy cerrados. La mayor está dominada por "
        "actores de voz del anime japonés, con Takahiro Sakurai (37 colaboradores), Yuki Kaji (33) y Daisuke Ono "
        "(29) como los más conectados. La segunda es la de Bollywood, con Shah Rukh Khan y Anupam Kher (17 "
        "colaboradores cada uno). La tercera reúne actores de voz de animación infantil, encabezados por Andrea "
        "Libman, Vincent Tong y Erin Mathews."),
      P("La centralidad de intermediación señala a Jun Fukuyama, Bryce Papenbrook, Takahiro Sakurai, Erin "
        "Fitzgerald y Stephanie Sheh como puentes dentro de la componente mayor. Los nombres que reconozco de esa "
        "lista son de doblaje al inglés de anime, lo que sugiere que conectan al elenco japonés con el doblado, "
        "pero el dataset no registra el idioma de la voz y por eso lo tomo como hipótesis. En cuanto a la "
        "codificación, el matiz representa una categoría (la comunidad), el tamaño una cantidad (el grado) y el "
        "grosor el peso de la relación. El filtro a 3 títulos descarta colaboraciones reales pero breves, y como "
        "los actores se identifican por nombre escrito, un homónimo o una grafía distinta genera un nodo "
        "duplicado o fusionado."),

      P("4.3 Distribuciones", h2),
      figura("03_distribuciones.png", 15.6,
             "Figura 3. Histograma con KDE y boxplot de la duración de las películas (izquierda) y del rezago entre "
             "estreno y llegada a Netflix (derecha). Línea negra: media; línea roja: mediana."),
      KeepTogether([tabla([["Estadístico", "Duración (min)", "Rezago (años)"],
             ["n", "5,377", "7,777"], ["Media", "99.31", "4.56"], ["Mediana", "98.00", "1.00"],
             ["Desviación estándar", "28.53", "8.73"], ["Q1 - Q3 (IQR)", "86 - 114 (28)", "0 - 5 (5)"],
             ["Asimetría", "0.19", "3.68"], ["Curtosis en exceso", "2.04", "17.60"],
             ["Límites de Tukey", "44 - 156", "-7.5 - 12.5"],
             ["Atípicos", "337 (6.3%)", "812 (10.4%)"], ["Mínimo - máximo", "3 - 312", "0 - 93"]],
            [5.4, 5.0, 5.0]),
      Spacer(1, 4),
      P("Tabla 2. Estadísticos descriptivos y valores atípicos según la regla de Tukey.", pie)]),
      P("<b>Duración de las películas.</b> La distribución es casi simétrica: media 99.3 y mediana 98 minutos, con "
        "asimetría de 0.19. Aun así, la curtosis en exceso de 2.04 indica colas más pesadas que las de una normal. "
        "Fuera de los límites de Tukey (44 y 156 minutos) hay 337 películas, el 6.3%, tanto cortas como muy "
        "largas. El histograma muestra además una pequeña joroba entre los 25 y los 45 minutos que el boxplot no "
        "registra, porque un resumen de cinco números no detecta multimodalidad. Supongo que se trata de "
        "especiales y cortometrajes, aunque el dataset no permite comprobarlo."),
      P("<b>Rezago.</b> Aquí la asimetría es fuerte: 3.68, con una curtosis en exceso de 17.6. La media (4.6 años) "
        "es más de cuatro veces la mediana (1.0), y el primer cuartil es 0, lo que significa que al menos una cuarta "
        "parte de los títulos entra a Netflix el mismo año de su estreno. Hay 812 atípicos por encima de los 12.5 "
        "años, y el máximo llega a 93. No son errores de captura sino catálogo histórico, así que eliminarlos "
        "distorsionaría el resultado. El límite inferior de Tukey (-7.5) queda por debajo del mínimo posible; en "
        "variables acotadas en cero, la regla no puede marcar atípicos de ese lado."),
      P("En el rezago la mediana es el resumen honesto, y para comparar grupos convendría una escala logarítmica o "
        "<font face='Courier'>log1p</font>. Ambas variables usan posición sobre una escala común, el canal más "
        "preciso, y compartir el eje x entre histograma y boxplot permite alinear forma y resumen."),

      P("4.4 Modelos temporales", h2),
      figura("s04_serie.png", 16.4,
             "Figura 4. Izquierda: títulos añadidos por mes (2015-2020), media móvil de 12 meses, ruptura estimada y "
             "fecha de la declaración de pandemia. Derecha: índice estacional (1.00 = nivel medio del año). "
             "Captura estática; la versión interactiva incluye selector de rango y minigráfico."),
      P("<b>Tendencia.</b> Las altas anuales pasan de 88 en 2015 a 443, 1,225, 1,685 y 2,153 en 2019, y bajan a "
        "2,009 en 2020. La media móvil sube casi en línea recta hasta mediados de 2019 y luego se aplana en torno a "
        "180 títulos por mes. El máximo mensual es noviembre de 2019, con 272."),
      P("<b>Ruptura.</b> El método ubica el quiebre en octubre de 2019. Antes el volumen mensual crecía unos 3.5 "
        "títulos por mes; después cae unos 4.5 por mes. Dos rectas reducen el error cuadrático un 34% frente a "
        "una sola (de 66,567 a 44,002). Hay que leerlo con cautela: el corte queda a 15 meses del final, la mejora "
        "no se acompañó de una prueba de significancia y el pico de noviembre de 2019 influye mucho en el ajuste."),
      P("<b>Año 2020.</b> La caída viene de las películas, que bajan de 1,497 a 1,312 altas (-12%), mientras las "
        "series suben de 656 a 697 (+6%). Febrero de 2020, con 117 títulos, ya era el valor más bajo del período "
        "reciente antes de la declaración de pandemia del 11 de marzo, de modo que los datos muestran "
        "coincidencia temporal y no permiten atribuir la caída a la pandemia."),
      P("<b>Estacionalidad.</b> Enero (1.43), diciembre (1.29), marzo (1.17) y octubre (1.14) quedan por encima del "
        "nivel anual; mayo y junio (0.82) son los más bajos. El patrón describe cuándo se registran las altas, no "
        "cuándo se consume, y refleja el calendario de lanzamientos. Como el índice se apoya en unos cinco ciclos "
        "y la tendencia creciente lo sesga, sirve como orden de magnitud. En cuanto a la codificación, la posición "
        "sobre ejes comunes permite comparar películas, series y total directamente; las líneas aprovechan el "
        "principio de continuidad y las anotaciones directas evitan buscar en una leyenda."),

      # -------------------------------------------------------------- 5. conclusiones
      P("5. Conclusiones y limitaciones", h1),
      P("Cada técnica respondió una pregunta distinta sobre el mismo catálogo. El treemap muestra que las series "
        "son más recientes y más infantiles que las películas. El grafo muestra que los actores colaboran en islas "
        "cerradas (anime japonés, Bollywood, animación infantil) y no en una red global. El panel de distribuciones "
        "deja claro que el rezago se resume con la mediana y no con la media. La serie de tiempo registra un "
        "crecimiento sostenido que se frena hacia finales de 2019."),
      P("Tres limitaciones condicionan estas lecturas. El catálogo es una captura puntual y omite lo retirado. Los "
        "actores se identifican solo por nombre. Y la serie termina en enero de 2021, un horizonte demasiado corto "
        "para saber si la desaceleración fue pasajera."),

      # -------------------------------------------------------------- 6. repositorio
      P("6. Repositorio del código fuente", h1),
      P("El notebook ejecutable, el CSV, las figuras interactivas (HTML) y estáticas (PNG) y el archivo de "
        "requisitos están en el siguiente repositorio:"),
      P(f'<link href="{REPO_URL}" color="#1a5fb4"><u>{REPO_URL}</u></link>',
        ParagraphStyle("url", parent=base, alignment=0, fontSize=10.5)),
      P("Para reproducir los resultados basta con abrir <font face='Courier'>Visualizacion_Netflix.ipynb</font> "
        "en Jupyter o en Google Colab y ejecutar todas las celdas. Los datos se descargan automáticamente."),

      # -------------------------------------------------------------- referencias
      P("Referencias", h1),
      P("Bruls, M., Huizing, K. y van Wijk, J. J. (2000). Squarified treemaps. <i>Data Visualization 2000</i>, "
        "Springer, 33-42.", ref),
      P("Cleveland, W. S. y McGill, R. (1984). Graphical perception: theory, experimentation, and application to "
        "the development of graphical methods. <i>Journal of the American Statistical Association</i>, 79(387), "
        "531-554.", ref),
      P("Johnson, B. y Shneiderman, B. (1991). Tree-maps: a space-filling approach to the visualization of "
        "hierarchical information structures. <i>Proceedings of IEEE Visualization '91</i>, 284-291.", ref),
      P("Kamada, T. y Kawai, S. (1989). An algorithm for drawing general undirected graphs. <i>Information "
        "Processing Letters</i>, 31(1), 7-15.", ref),
      P("Munzner, T. (2014). <i>Visualization Analysis and Design</i>. CRC Press.", ref),
      P("Newman, M. E. J. (2006). Modularity and community structure in networks. <i>PNAS</i>, 103(23), "
        "8577-8582.", ref),
      P("Tukey, J. W. (1977). <i>Exploratory Data Analysis</i>. Addison-Wesley.", ref),
      P("Bansal, S. (s. f.). <i>Netflix Movies and TV Shows</i> [conjunto de datos]. Kaggle. Redistribuido en "
        "TidyTuesday, 2021-04-20: github.com/rfordatascience/tidytuesday.", ref),
      ]

doc.build(S)
print("Informe generado:", SALIDA)
