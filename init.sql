CREATE TABLE IF NOT EXISTS films (
    id_film INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) UNIQUE,
    duree INT,
    salles INT,
    genre VARCHAR(100),
    date_sortie DATE,
    pays VARCHAR(100),
    studio VARCHAR(255),
    description TEXT,
    image TEXT,
    budget BIGINT,
    entrees BIGINT,
    anecdotes INT
);

CREATE TABLE IF NOT EXISTS Personnes (
    id_personne INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS Participations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_film INT,
    id_personne INT,
    role VARCHAR(50),
    UNIQUE (id_film, id_personne, role),
    FOREIGN KEY (id_film) REFERENCES films(id_film) ON DELETE CASCADE,
    FOREIGN KEY (id_personne) REFERENCES Personnes(id_personne) ON DELETE CASCADE
);
