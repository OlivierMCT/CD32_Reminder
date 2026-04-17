import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from persistence.entities.category_entity import CategoryEntity
from persistence.entities.todo_entity import TodoEntity


def add_sample_data(session: Session):
    categories = [
        CategoryEntity(title=c, color='yellow', creation_date=datetime.now()) for c in ['perso', 'pro', 'vacances', 'apéro']
    ]
    bucket_list = [
        "Participer à des concerts et me laisser porter par la musique que j'adore, au rythme des lumières dansantes",
        "Faire un truc extraordinaire à mes 30 ans",
        "Vivre 6 mois à l'étranger",
        "Passer une nuit dans un hôtel Spa 5*",
        "Danser sous une pluie tropicale",
        "Avoir une étoile à mon nom",
        "Dormir dans une villa sur pilotis",
        "Siroter un cocktail sous les palmiers",
        "Voir une aurore boréale",
        "Voir la tour Eiffel scintiller et les feux d'artifices du 14 juillet",
        "Observer les étoiles et la voie lactée toute une nuit, voir passer une étoile filante",
        "Camper dans le désert",
        "Dormir dans une cabane dans les arbres",
        "Poser le pied sur un glacier",
        "Faire un séjour en bivouac",
        "Dormir dans une yourte",
        "Prendre un hydravion pour apercevoir les magnifiques lagons",
        "Voir le soleil de minuit puis, lors d'un autre voyage, le Kaamos",
        "Faire un trek en altitude",
        "Me baigner dans les eaux turquoise de Polynésie Française et dormir dans un Faré",
        "Voir la ville de Dubaï et surtout le désert et ses jolies dunes de sable",
        "Passer la nuit dans une cabane de plage au bord de la mer et me réveiller au son des vagues",
        "Mettre un pied sur les 5 continents",
        "Découvrir la Grande barrière de corail",
        "Souffrir du décalage horaire (c'est la seule maladie acceptable)",
        "Avoir la chance de faire de magnifiques randonnées en pleine nature",
        "Dormir dans un château",
        "Ecrire un livre ou un blog",
        "Retrouver les sensations du ski",
        "Partir en vacances en camping",
        "Vivre un noël au soleil",
        "Obtenir un diplôme",
        "Feuilleter des millions de Livres dans la bibliothèque du Trinity college à Dublin",
        "Apercevoir un ours dans les forêts de l'ouest américain",
        "Faire bronzette sur une plage paradisiaque avec un bon bouquin",
        "Etre champion du monde",
        "Faire un voyage humanitaire",
        "Voir les pyramides en Egypte",
        "Dormir dans un igloo aux parois de verre",
        "Aller à Hawaï, voir les volcans et plages de rêves, être accueillie sur l'île avec une couronne de fleur",
        "Faire une croisière pour visiter plusieurs pays en une semaine",
        "Dormir à la belle étoile",
        "Découvrir le temple d'Angkor Wat au Cambodge",
        "Faire un tour du monde",
        "Découvrir un endroit qui n'est pas inscrit dans ma liste et en avoir le souffle coupé",
        "Nager dans tous les océans sur cette planète",
        "Prendre le transsibérien, voir le lac Baïkal",
        "Me baigner dans les sources d'eau chaude en Islande",
        "Participer à la fête des couleurs en Inde",
        "Plonger dans un Cénote, me promener dans les sites archéologiques mayas",
        "Être dépaysée en prenant le train de la Mer de Glace pour une vertigineuse ascension à travers les sapins",
        "Dormir dans un lieu insolite",
        "Faire un tour en barque dans un lac entouré de montagnes",
        "Louer une villa avec piscine",
    ]
    todos = [
        TodoEntity(
            description=d,
            is_done = random.choice([True, False]),
            due_date=datetime.now() + timedelta(days=random.randint(-40, 50)),
            categories = random.choices(categories),
            creation_date=datetime.now()
        ) for d in bucket_list
    ]
    session.add_all(categories)
    session.add_all(todos)
    session.commit()