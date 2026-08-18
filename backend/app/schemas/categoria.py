from sqlmodel import Field, SQLModel


class CategoriaBase(SQLModel):
    nome: str = Field(min_length=1, max_length=50)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaRead(CategoriaBase):
    id: int
