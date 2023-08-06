from setuptools import setup

setup(
  name='foronoi',
  packages=[
    'foronoi',
    'foronoi.visualization',
    'foronoi.contrib',
    'foronoi.observers',
    'foronoi.tree',
    'foronoi.nodes',
    "foronoi.graph",
    "foronoi.events",
    "foronoi.tests"
  ],
  version="1.0.0",
  description="Fortune's algorithm for fast Voronoi diagram construction with extras.",
  author='Jeroen van Hoof',
  author_email='jeroen@jeroenvanhoof.nl',
  url='https://github.com/Yatoom/voronoi',
  download_url='',
  keywords=['voronoi', 'polygon', 'fortune', 'algorithm'],
  classifiers=[],
  install_requires=[
    "numpy", "matplotlib", "graphviz"
  ]
)