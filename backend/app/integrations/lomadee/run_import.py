import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from sqlmodel import Session
from app.core.database import engine, criar_tabelas
from app.integrations.lomadee.importer import ImportadorLomadee

PRODUTOS_ALVO = [
    ("GTX 1650", "Placa de Vídeo"),
]


def main():
    criar_tabelas()

    with Session(engine) as session:
        importador = ImportadorLomadee(session)
        for query, categoria_nome in PRODUTOS_ALVO:
            resumo = importador.importar(query, categoria_nome)
            print(f"[{query}] {resumo}")


if __name__ == "__main__":
    main()
