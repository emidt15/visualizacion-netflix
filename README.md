# Visualización del catálogo de Netflix

Notebook de Jupyter con cuatro visualizaciones (treemap, grafo de co-ocurrencias, histograma + boxplot y serie de tiempo interactiva) sobre el dataset *Netflix Movies and TV Shows* (TidyTuesday, 2021-04-20).

## Contenido
- `Visualizacion_Netflix.ipynb`: notebook comentado y ejecutable.
- `netflix_titles.csv`: copia local del dataset (el notebook lo descarga de GitHub y usa esta copia si no hay conexión).
- `figuras/`: gráficos interactivos (`.html`) y versiones estáticas (`.png`).
- `generar_informe.py`: genera el informe PDF a partir de las figuras.

## Cómo ejecutarlo
```bash
pip install -r requirements.txt
jupyter notebook Visualizacion_Netflix.ipynb
```
En Google Colab: subir el notebook y ejecutar todas las celdas (las librerías ya vienen instaladas, salvo `squarify`; descomentar la primera línea de la celda de configuración).

Las figuras Plotly se ven al abrir el notebook en Jupyter o Colab. GitHub no las renderiza en su vista previa; para eso están los `.html` de `figuras/`.
