# Organizaciones Inteligentes y Sistemas Multiagente en Acción

## Acerca de este Repositorio

Este repositorio contiene los materiales para la charla "Organizaciones Inteligentes y Sistemas Multiagente en Acción" que se impartirá o ha sido impartida el 20 de marzo de 2025. La presentación está diseñada para introducir a los asistentes al framework CrewAI y su aplicación en el desarrollo de sistemas multiagente en Python.

## Contenido del Repositorio

### Archivos Principales

- **notebook.ipynb**: Jupyter Notebook con ejemplos prácticos y código ejecutable que muestra cómo implementar agentes de IA utilizando CrewAI. El notebook incluye:
  - Introducción a CrewAI y sus conceptos fundamentales
  - Configuración del entorno con Google AI Studio (Gemini 2.0 Flash) y LiteLLM
  - Explicación detallada de `Crew`, `Agent`, `Tools` y `Flows`
  - Ejemplos prácticos desde agentes básicos hasta equipos de múltiples agentes

- **Organizaciones_Inteligentes_y_Sistemas_Multiagentes_en_acción.pdf**: Presentación completa en formato PDF que complementa el contenido del notebook, ofreciendo explicaciones teóricas sobre los agentes y sistemas multiagente.

### Requisitos

El archivo `requirements.txt` contiene todas las dependencias necesarias para ejecutar los ejemplos del notebook:

```text
crewai
crewai[tools]
dotenv
jupyter
IPython
```

## Configuración del Entorno

1. Clona este repositorio
2. Crea un entorno virtual (recomendado)
3. Instala las dependencias: `pip install -r requirements.txt`
4. Configura tus credenciales de API en un archivo `.env` siguiendo el ejemplo en `.env.example`
5. Abre el notebook con Jupyter: `jupyter notebook notebook.ipynb`

## Licencia

Este repositorio está licenciado bajo la licencia MIT. Puedes encontrar más información en el archivo LICENSE (en inglés).