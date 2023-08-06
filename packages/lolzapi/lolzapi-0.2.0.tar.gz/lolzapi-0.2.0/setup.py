from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(name='lolzapi',
      version='0.2.0',
      description='Библиотека для удобной работы с lolz.guru api',
      packages=['lolzapi'],
      long_description=long_description,
      long_description_content_type='text/markdown', 
      author_email='cotanton111@gmail.com',
      zip_safe=False)
