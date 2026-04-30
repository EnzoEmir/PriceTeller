import os
os.environ["DATABASE_URL"] = "sqlite:///./seed.db"

import sys
from pathlib import Path
# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import engine, criar_tabelas
from app.test.builder.scenario_builder import ScenarioBuilder
from sqlmodel import Session

def seed():
    criar_tabelas()

    with Session(engine) as session:
        builder = ScenarioBuilder(session)
        builder.basic()

if __name__ == "__main__":
    seed()