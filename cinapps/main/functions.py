import mysql.connector

def scoring_casting(film, actors_df):
    poids_total = 0
    noms_personnes_dans_film = ','.join(film['acteurs'] + film['realisateurs'])
    for personne in noms_personnes_dans_film.split(','):
        if personne in actors_df['name'].values:
            poids_acteur = actors_df.loc[actors_df['name'] == personne, 'coef_personne'].values[0]
            poids_total += poids_acteur
            print(f"POUR L'ACTEUR : {personne}: {poids_acteur}")
    return poids_total

def get_studio_coefficient(studio):
    if studio in ('Walt Disney Pictures','Warner Bros.','Paramount','Sony Pictures','Universal','20th Century Fox','Lionsgate','Columbia'):
        return 3
    elif studio in ('Pathé','Studiocanal','Gaumont','UGC Distribution','SND','Le Pacte','Metropolitan','EuropaCorp','GBVI','Wild Bunch','UFD','ARP Selection','Ad vitam','Haut et Court','Films du Losange','Rezo Films','TFM Distribution'):
        return 2
    elif studio in ('Gébéka','Memento Films','KMBO','Océan Films','AMLF','MK2 Diffusion','Gaumont Sony','Apollo Films','Sophie Dulac','Eurozoom','Jour2Fête','Pan-Européenne','Cinema Public','Polygram'):
        return 1
    else:
        return 0
