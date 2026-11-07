# Möbius Angoulême pour Home Assistant

Intégration custom qui affiche les prochains passages de bus du réseau Möbius (Grand Angoulême) dans Home Assistant, à partir du flux temps réel GTFS-RT.

## Installation (HACS)

1. Dans HACS, ouvre **Intégrations**, puis le menu ⋮ et **Dépôts personnalisés**.
2. Ajoute `https://github.com/len12-Dev/stga-mobius-haaddon` avec la catégorie **Intégration**.
3. Installe **Möbius Angoulême**, puis redémarre Home Assistant.
4. Va dans **Paramètres → Appareils et services → Ajouter une intégration** et cherche *Möbius Angoulême*.

## Configuration

Le formulaire demande :

- **Nom du capteur** : libre, par exemple `BHNS A - mon arrêt`.
- **Identifiant de l'arrêt (stop_id)** : l'identifiant GTFS de l'arrêt. Il se trouve dans le fichier `stops.txt` du GTFS statique Möbius (colonne `stop_id`).
- **Identifiant de la ligne (route_id)** : colonne `route_id` de `routes.txt`. Par défaut `174`, qui correspond à la BHNS A.
- **Sens (0 ou 1)** : colonne `direction_id` de `trips.txt`. Vérifie dans `trips.txt` quel sens mène à ta destination.

Chaque couple arrêt, ligne et sens peut être ajouté une seule fois. Pour suivre plusieurs arrêts, ajoute l'intégration plusieurs fois.

## Capteur

Le capteur affiche le nombre de minutes avant le prochain passage. Ses attributs listent les cinq prochains passages au format `HH:MM`.

Il est mis à jour toutes les 60 secondes.

## Données et licence

- Données : réseau Möbius (CA du Grand Angoulême), publiées sur [data.gouv.fr](https://www.data.gouv.fr/datasets/horaires-theoriques-et-temps-reel-reseau-mobius) et [transport.data.gouv.fr](https://transport.data.gouv.fr/datasets/horaires-theoriques-et-temps-reel-reseau-mobius).
- Licence des données : [ODbL](http://opendatacommons.org/licenses/odbl/summary/).
- Le flux temps réel ne fournit que les mises à jour de trajets. Il ne donne pas la position des bus, et sa fraîcheur n'est pas garantie : un passage peut être affiché avec un léger décalage.

## Limites connues

- L'intégration n'utilise que le flux temps réel. Si le flux est vide ou indisponible, le capteur passe à « inconnu ».
- Le format du flux peut évoluer avec les saisons de service.
