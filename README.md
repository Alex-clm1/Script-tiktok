Projet Quiz TikTok

Description

Ce projet est un quiz interactif pour TikTok Live. Il permet aux spectateurs d'un live TikTok de répondre à des questions en temps réel et de gagner des points en cas de bonne réponse. L'application est développée en Python avec Flask pour la gestion des questions et Tkinter pour l'interface graphique.

Fonctionnalités

Connexion à un live TikTok via l'API TikTokLive

Affichage de questions et gestion des réponses des utilisateurs

Synthèse vocale pour la lecture des questions et des réponses

Système de points et classement en direct

Interface graphique avec Tkinter

API Flask pour ajouter, supprimer et récupérer des questions

Fond vert pour permettre l'ajout d'un arrière-plan personnalisé sur les questions

Prérequis

Avant de lancer le projet, assurez-vous d'avoir installé les dépendances suivantes :

pip install TikTokLive tkinter pillow gtts playsound flask

Installation

Clonez le dépôt :

git clone https://github.com/alex-clm1/quiz-tiktok.git
cd quiz-tiktok

Installez les dépendances :

pip install -r requirements.txt

Utilisation

Lancer le serveur Flask

python server.py

Le serveur sera accessible sur http://localhost:5000.

Lancer le bot TikTok

python bot7.py

Ce script connectera le bot au live TikTok et gérera le quiz.

API

L'API Flask propose plusieurs routes :

GET /get_questions : Récupère toutes les questions.

POST /add_question : Ajoute une question (corps JSON : {"question": "Texte", "answer": "Réponse"}).

POST /delete_question : Supprime une question (corps JSON : {"question": "Texte"}).

Gestion des Questions

Les questions peuvent être ajoutées ou supprimées via l'API Flask, mais il est aussi possible de modifier directement le fichier questions.json pour ajouter de nouvelles questions manuellement.

Fichiers Principaux

bot7.py : Gère le quiz en direct sur TikTok.

server.py : Fournit une API Flask pour gérer les questions.

questions.json : Contient la liste des questions du quiz.

Auteurs

[Votre Nom]

Licence

Ce projet est sous licence MIT.

