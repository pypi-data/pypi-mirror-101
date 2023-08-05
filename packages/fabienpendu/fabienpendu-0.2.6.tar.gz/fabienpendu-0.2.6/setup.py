#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages

# notez qu'on import la lib
# donc assurez-vous que l'importe n'a pas d'effet de bord
#import fabienpendu_lib #ne build pas avec pyproject.toml
 
# Ceci n'est qu'un appel de fonction. Mais il est trèèèèèèèèèèès long
# et il comporte beaucoup de paramètres
setup(
        name='fabienpendu',
        version="0.2.6",
        # Liste les packages à insérer dans la distribution
        # plutôt que de le faire à la main, on utilise la foncton
        # find_packages() de setuptools qui va cherche tous les packages
        # python recursivement dans le dossier courant.
        # C'est pour cette raison que l'on a tout mis dans un seul dossier:
        # on peut ainsi utiliser cette fonction facilement
        packages=find_packages(),
        # votre pti nom
        author="fabien",
        # Votre email, sachant qu'il sera publique visible, avec tous les risques
        # que ça implique.
        author_email="fabien.fab@e-nautia.com",
        # Une description courte
        description="Jeu du pendu avec tkinter",
        # Une description longue, sera affichée pour présenter la lib
        # Généralement on dump le README ici
        long_description= open('README.md').read(),
        long_description_content_type='text/markdown', 
        install_requires= ["unidecode", "pygame"],
        # Active la prise en compte du fichier MANIFEST.in
        #Definition list ends without a blank line; unexpected unindent.
        include_package_data=True,
        # Une url qui pointe vers la page officielle de votre lib
        url='http://github.com/pseudofab/fabien_lib', #non crée
        # Il est d'usage de mettre quelques metadata à propos de sa lib
        # Pour que les robots puissent facilement la classer.
        # La liste des marqueurs autorisées est longue:
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
        #
        # Il n'y a pas vraiment de règle pour le contenu. Chacun fait un peu
        # comme il le sent. Il y en a qui ne mettent rien.
        classifiers=[
            "Programming Language :: Python",
            "Development Status :: 1 - Planning",
            "License :: OSI Approved",
            "Natural Language :: French",
            "Intended Audience :: Education",
            "Operating System :: Unix",
            "Topic :: Games/Entertainment",
            "Programming Language :: Python :: 3.8",
            ],
        # C'est un système de plugin, mais on s'en sert presque exclusivement
        # Pour créer des commandes, comme "django-admin".
        # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
        entry_points = {
                'console_scripts': [
                    'pendu = fabienpendu_lib.core:pendu',
                    'hanged = fabienpendu_lib.core:hanged'
                    ],
                },
        # A fournir uniquement si votre licence n'est pas listée dans "classifiers"
        # ce qui est notre cas
        license="WTFPL",
        )
