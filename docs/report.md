---
institute: Sorbonne Université
title: "PSTL: MrPython"
subtitle: Rapport de projet
author:
- Alexandre Doussot
- Crhistopher Trublereau
teacher: Fréderic Peschanski
course: PSTL
place: Paris
date: 24 Mai 2018
papersize: a4
fontsize: 12pt
header-includes:
  - \usepackage{tikz}
  - \usepackage{listings}
  - \usepackage{color}
  - \usepackage{courier}
  - \usepackage{syntax}
  - \usepackage{fancyvrb}
  - \usepackage{booktabs}
---

\include tex_templates/code.tex

# Introduction

Nous a été donné la tâche d'enrichir un projet développé depuis plusieurs ans
dans le cadre de Projets STL. Ce projet, MrPython, est une sorte d'IDE pour
Python, dans lequel les étudiants de première année peuvent écrire et faire
tourner leur code, notamment dans le cadre de l'UE 1I103. _(?)_
Cette UE demande aux étudiants d'annoter le type de leur fonctions
et variables. Cependant, jusqu'a présent, il n'y avait aucune vérification
logicielle réalisée sur ces annotations, de même que les erreurs de types
n'étaient attrapés qu'au runtime. On propose alors un système de vérification
de type préalable à l'exécution.

\newpage

# Théorie

Pour résoudre le problème qui a été donné, il a fallu nous pencher sur 
une théorie nommée _Typage Bidirectionnel_.

## Typage Bi-Directionnel

La force du typage bidirectionnel réside dans son compromis entre les
systèmes d'inférence et l'annotation complète.


### Système d'inférence

Dans un système similaire à un système Hindley-Miller, il n'y a pas besoin
de déclarer de types - le compilateur peut les trouver lui-même. Cependant,
les programmeurs sont ainsi privés d'une forme de documentation sous la forme
d'annotations, et les messages d'erreurs peuvent être confus.


### Annotation Complète

C'est un système assez répandu dans les langages populaires. On peut
par exemple le retrouver dans C++.

### Bidirection

Plutôt que persister à tenter de trouver le type d'une expression - en ne connaissant
que le type des variables, et parfois même pas toutes - comme le fait l'inférence,
on alterne entre _synthétiser_ des types et _vérifier_ les expressions contre
des types déjà connus.

En termes de jugement, le typage bidirectionnel remplace le jugement de typage standard

*put latex here*

par deux différents jugements:

*synthetize judgement*
*check against judgement*


*// Maybe dive a little more inside bidirtypecheck*

## Typage de MrPython

Pour les besoins de MrPython, il faut séparer de types d'erreurs.
Les erreurs d'annotations - warnings -, et les erreurs fatales - errors.

On se propose d'enrichir la notation développée dans le cadre du typage bidirectionnel
par les sigles suivants: *inclure /skull et /warn*

### Skull

Ce sigle dénote les erreurs fatales. Si une telle erreur est rencontrée, l'éxécution
ne peut plus continuer, et l'on affiche l'erreur correspondante.

### Warn

Ce sigle dénote les erreurs d'annotations. Par exemple, un étudiant peut déclarer x de
la manière suivante:

\code
# x : int
x = "wow"
\end_code

Ainsi, le typeur lui affichera un warning pour annotation érronée.

## Règles

_Insérer les règles développées dans py101_

\newpage

# Implémentation

## Parseur

Le parseur pour les annotations a été implémentée à l'aide
de la bibliothèque `popparser`. Cette dernière permet de 
décrire une grammaire de façon concise sous forme de combinateurs
de parseurs.

## Vérificateur de type

Le vérificateur de type - implémenté en Python lui aussi - se
base sur la classe NodeVisitor exposée par la runtime Python.
Elle réimplémente le patron de conception bien connu: Visiteur.

Ainsi, le typechecker implémente une fonction de visite pour chaque
noeud de l'AST intéressant, dans laquelle vont être vérifier le type
des expressions ainsi que mettre à jour le type de retour de l'expression.
Prenons pour exemple la fonction `visit_BoolOp`, visitant un noeud d'opération booléenne - e.g. `True or False or x`.

\code
  def visit_BoolOp(self, node):
        # a or b or c is collapsed into a single Or node
        for operand in node.values:
            self.visit(operand)
            self.check_bool(operand)
        self.return_type = TypeEnum.BOOL
\end_code

Pour chacune des opérandes de l'opération, on vérifie qu'elles sont bien de types
booléens, et l'on met à jour le type de retour à `TypeEnum.BOOL`.

Quant à l'autre direction de vérification, l'on peut se pencher sur `visit_NameConstant.`

\code
    def visit_NameConstant(self, node):
        if node.value == True or node.value == False:
            self.return_type = TypeEnum.BOOL
\end_code


\newpage

# Organisation

Le PSTL s’est principalement articulé autour de la branche pstl-2018 du GitHub dédié à MrPython. Ce dernier contient un certain nombre de fichiers et de dossiers, dont 3 ont été utilisés pour notre travail :

1. Le dossier docs/pythons101, contenant :
    - Le fichier python101-spec.tex dans lequel se trouve la rubrique « Type system » où a été consignée l’ensemble des règles de bidirectional type checking utilisées.
    - Le Makefile pour compiler du .tex vers du .pdf.
2. Le dossier mrpython/typechecking, contenant : 
    - Le fichier typecheck_annotation_parser.py qui parse un programme MrPython afin de récupérer ses annotations de type.
    - Les fichiers typecheck_visitor.py et typer.py qui effectuent le type checking sur un programme MrPython.
    - Le fichier warnings.py qui lance des avertissements lorsqu’une variable n’a pas d’annotation de type, ou lorsque cette dernière n’est pas adaptée à l’opération (par exemple, un float qui stocke le résultat d’une addition entre 2 int).
3. Le dossier examples, contenant des fichiers .py pour tester l’analyse de typage, dont l’implémentation se trouve dans les fichiers décrits précédemment.
    - Par exemple, le fichier aire.py contient un programme permettant de calculer l’aire d’un triangle. 
    Une division réelle par 2 est faite sur la somme des côtés du triangle, et le résultat est stocké dans une variable p.
    Cette dernière doit donc être typée par un float, d’où l’annotation #p : float, écrite juste au-dessus de l’opération.
    Le parser doit donc être en mesure de récupérer cette annotation, le type checker lui, doit vérifier que le type est correct à l’aide de cette dernière.
