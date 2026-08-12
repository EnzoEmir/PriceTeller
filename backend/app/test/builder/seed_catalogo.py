from sqlmodel import Session

from app.core.database import engine, criar_tabelas
from app.test.builder.scenario_builder import ScenarioBuilder


def main():
    criar_tabelas()

    with Session(engine) as session:
        print(ScenarioBuilder(session).catalogo_com_ofertas())


if __name__ == "__main__":
    main()
