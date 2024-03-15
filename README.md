# HACKQC 2024
## Defi 4- Solution pour trouver un logement basé sur la piste cyclable pour les cyclistes et l'adresse de travail donnée 
## Données utilisées:
- [Données d'address à Sherbrooke format GeoJSON](https://www.donneesquebec.ca/recherche/dataset/d03eeb91762a41259eb8b959635c7437_0) 
- [Données de la piste cyclable (GeoJSON)](https://www.donneesquebec.ca/recherche/dataset/9478537c06104aa0a2c7e4634947f382_0)
- [Données de les segments de rue (GeoJSON)](https://www.donneesquebec.ca/recherche/dataset/9478537c06104aa0a2c7e4634947f382_0)

### Groupe : Bishop binary  nomad
#### Membres : Yagmur Gulec 
####           Ghazaleh Hamzeh
####           Dan Luo
####           Guang Wang

## Introduction (FR)
Les personnes qui se rendent à leur bureau en vélo veulent avoir accès au vélo. Ils veulent habiter à côté d'une piste cyclable. Dans ce projet, nous aimerions présenter une solution pour offrir un logement approprié accessible depuis une piste cyclable à partir de l'adresse de travail donnée. Une adresse de travail est choisie au hasard parmi les données d'adresses. Le nœud le plus proche est choisi dans le graphe converti à partir des données relatives aux pistes cyclables. 
## A développer
Nous pourrions parvenir à proposer une solution pour utiliser des données géologiques sous forme de graphe. Nous avons pu compléter la recherche d'une piste cyclable dans un intervalle. Cependant, nous avons besoin de trouver une adresse appropriée à proximité de la cible du chemin. 
Une autre amélioration consiste à proposer une piste cyclable avec le moins d'intersection possible avec les rues. 
## Comment exécuter le code
-Créer un environnement python
avec make install 
-make run
