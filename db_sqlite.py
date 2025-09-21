import sqlite3

DB_NAME = "localidades.db"


def inicializa_db():
    cidades_pb = [
        'Araruna',
        'Areia',
        'Baía da Traição',
        'Bananeiras',
        'Cabaceiras',
        'Cabedelo',
        'Campina Grande',
        'Conde',
        'João Pessoa',
        'Lucena',
        'Mamanguape',
        'Pitimbu',
        'Puxinanã',
        'Queimadas',
        'Santa Inês',
        'São Bento',
        'Sousa',
        'Teixeira'
    ]
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS cidades
                       (
                           id     INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome   TEXT NOT NULL,
                           estado TEXT NOT NULL,
                           UNIQUE (nome, estado)
                       )
                       """)
        for cidade in cidades_pb:
            try:
                cursor.execute(
                    "INSERT INTO cidades (nome, estado) VALUES (?, ?)",
                    (cidade, "PB")
                )
            except sqlite3.IntegrityError:
                pass

        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados SQLite: {e}")
    finally:
        if conn:
            conn.close()


def adicionar_cidade(nome, estado):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO cidades (nome, estado) VALUES (?, ?)", (nome, estado))

        conn.commit()
    except sqlite3.IntegrityError:
        print(f"A cidade '{nome} - {estado}' já existe no banco de dados.")
        return False
    except sqlite3.Error as e:
        print(f"Erro ao adicionar cidade: {e}")
        return False
    finally:
        if conn:
            conn.close()
    return True


def listar_cidades():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome, estado FROM cidades ORDER BY nome")

        cidades = cursor.fetchall()
        return cidades
    except sqlite3.Error as e:
        print(f"Erro ao buscar cidades: {e}")
        return []
    finally:
        if conn:
            conn.close()
