USE empresa_dados;

CREATE TABLE empresa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_empresa VARCHAR(255) NOT NULL
);

CREATE TABLE telefone (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE
);

CREATE TABLE endereco_dns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    endereco_dns VARCHAR(255) NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresa(id) ON DELETE CASCADE
);

INSERT INTO empresa (nome_empresa) VALUES
    ('Magazine Osasco'),
    ('Magazine Barueri');


INSERT INTO telefone (empresa_id, telefone) VALUES
    (1, '11958758844'),
    (1, '1136084157'),
    (1, '1136825541'),
    (2, '11958744253'),
    (2, '11965541235'),
    (2, '1136825541');

INSERT INTO endereco_dns (empresa_id, endereco_dns) VALUES
    (1, 'www.magaosasco.com'),
    (1, 'www.magazineosasco.com'),
    (1, 'www.osascomagazine.com'),
    (2, 'www.magazinebarueri.com'),
    (2, 'www.magabarueri.com'),
    (2, 'www.baruerimagazine.com');

CREATE USER 'root'@'172.18.0.3' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.18.0.3' WITH GRANT OPTION;
FLUSH PRIVILEGES;
