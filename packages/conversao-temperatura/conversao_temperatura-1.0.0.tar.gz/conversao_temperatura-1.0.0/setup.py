
from setuptools import setup

setup(
    name = 'conversao_temperatura',
    version = '1.0.0',
    author = 'Fabrício Antoniasse',
    author_email = 'fabricio.antoniasse@hotmail.com',
    packages = ['conversao_temperatura'],
    description = 'Um simples conversor de temperatura (Celsius - Fahrenheit)',
    long_description = 'Um simples conversor de temperatura, com funções para '
                        + 'conversão de Celsius para Fahrenheit e vice-versa, '
                        + 'usado para um post no Blog da Alura',
    url = 'https://github.com/FAntoniasse/Conversao_temperatura',
    project_urls = {
        'Código fonte': 'https://github.com/FAntoniasse/Conversao_temperatura',
        'Download': 'https://github.com/FAntoniasse/Conversao_temperatura/blob/main/conversor.rar'
    },
    license = 'MIT',
    keywords = 'conversor temperatura',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)