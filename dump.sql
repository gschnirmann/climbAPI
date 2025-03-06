-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE
);

-- Inserir dados na tabela users
INSERT INTO users (user_id, username) VALUES
(1, 'gschnirmann'),
(2, 'gui'),
(3, 'gui2'),
(4, 'gui4'),
(5, 'gui9'),
(6, 'Gui'),
(7, 'mchlsartori'),
(8, 'kinkin');

-- Criar tabela de crags
CREATE TABLE IF NOT EXISTS crags (
    crag_id SERIAL PRIMARY KEY,
    cragname TEXT NOT NULL UNIQUE,
    country TEXT NOT NULL,
    city TEXT NOT NULL
);

-- Inserir dados na tabela crags
INSERT INTO crags (crag_id, cragname, country, city) VALUES
(1, 'Sao Luiz do Puruna', 'Brasil', 'Curitiba'),
(2, 'Pirai do sul - Amigos', 'Brasil', 'Pirai do Sul'),
(5, 'Pirai do sul - Corpo Seco', 'Brasil', 'Pirai do Sul');

-- Criar tabela de rotas
CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    grade TEXT NOT NULL,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    crag_id INTEGER REFERENCES crags(crag_id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    description TEXT
);

-- Inserir dados na tabela routes
INSERT INTO routes (id, name, grade, user_id, crag_id, type, description) VALUES
(3, 'Mato Psicodelico', '6a', 7, 1, 'sent', 'Via boa para aquecer e bombar'),
(6, 'Aço de navaia', '8a', 1, 2, 'sent', 'Inicio pela esquerda, cuidado para não subir muito os pés...');

-- Ajustar os valores das sequências para refletir os IDs inseridos
SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users));
SELECT setval('crags_crag_id_seq', (SELECT MAX(crag_id) FROM crags));
SELECT setval('routes_id_seq', (SELECT MAX(id) FROM routes));

COMMIT;

