## Objetivos de la Sesión:
En esta sesión comenzamos con la segunda práctica, un proyecto de desarrollo fullstack. Los principales objetivos era desarrollar el backend agregando nuevos modelos, generando migraciones de bases de datos y creando puntos finales para operaciones CRUD en la API.

## Tecnologías y Herramientas:
Las principales tecnologías y herramientas utilizadas en esta sesión incluyen:
- **FastAPI:** Un marco web moderno y rápido (de alto rendimiento) para crear API con Python.
- **SQLAlchemy:** Un kit de herramientas SQL y una biblioteca de mapeo relacional de objetos (ORM) para Python.
- **Alembic:** Una herramienta ligera de migración de bases de datos para usar con SQLAlchemy.
- **SQLite:** Una biblioteca en lenguaje C que implementa un motor de base de datos SQL..

## Creación de Modelos y Migraciones de Bases de Datos:
Durante esta sesión, creamos nuevos modelos para representar entidades en nuestra aplicación y generamos migraciones de bases de datos para reflejar estos cambios. Los modelos se definieron utilizando la biblioteca SQLModel, que proporciona una forma sencilla de definir modelos de datos en Python. Luego, utilizamos Alembic para generar scripts de migración que se pueden aplicar a la base de datos para reflejar los cambios en los modelos.

Para cada modelo, también creamos clases adicionales, como una clase XXXOut o una clase XXXCreate, para representar los datos que queremos generar para el modelo correspondiente o los datos necesarios para recopilar información y crear la entidad en nuestra base de datos.

### 1. Teams Model
Creamos un modelo `Team` para representar un equipo en nuestra aplicación. El modelo incluye  los campos:

- `name`: Nombre del equipo.
- `country`: País del equipo.
- `description`: Descripción opcional del equipo.

### 2. Competitions Model
Creamos un modelo `Competition` para representar una competencia en nuestra aplicación. El modelo incluye los siguentes campos: 

- `name`: Nombre de la competencia.
- `sport`: Deporte al que pertenece la competencia.
- `category`: Categoría de la competencia.

### 3. Matches Model
Creamos un modelo `Match` para representar un partido en nuestra aplicación. El modelo incluye los campos:

 - `date`: Fecha y hora del partido.
 - `price`: Precio de las entradas.
 - `competition`: Competencia a la que pertenece el partido.
 - `local_team`: Equipo local.
 - `visitor_team`: Equipo visitante.
 - `tickets_available`: Número de entradas disponibles en un momento dado.

- 
## Detailed Activities and Code Snippets:

**Ejemplo de un Model (`team.py`):**
```python
from sqlmodel import Field
from .base import SQLModel

class TeamBase(SQLModel):
    name: str
    country: str
    description: str | None = None
    
class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TeamCreate(TeamBase):
    ...

class TeamOut(TeamBase):
    ...
```

**Ejemplo de Operaciones CRUD(`teams.py`):**
```python
from typing import Any
from sqlmodel import Session, select
from app.models import Team, TeamCreate, TeamUpdate

def create_team(*, session: Session, team_create: TeamCreate) -> Team:
    ...

def get_team(*, session: Session, name: str) -> Team:
    ...

def delete_team(*, session: Session, team_id: int) -> Any:
    ...

def update_team(*, session: Session, team: Team, team_in: TeamUpdate) -> Any:
    ...
```

**API Endpoint Example (`teams.py`):**
```python
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import Team, Message, TeamOut, TeamsOut, TeamCreate, TeamUpdate

router = APIRouter()

@router.get("/{team_name}", response_model=TeamOut)
async def read_team(team_name: str, session: SessionDep):
   team = crud.team.get_team_by_name(session=session, name=team_name)
   if not team:
      raise HTTPException(status_code=404, detail=f"Team {team_name} not found")

   return team
```

## Resumen:
Esta sesión se centró en configurar el entorno de desarrollo, definir nuevos modelos, integrarlos en la base de datos y desarrollar puntos finales API para gestionar estos modelos. La sesión también cubrió las pruebas de estos puntos finales para garantizar que funcionen correctamente. Al seguir las pautas y completar los ejercicios, aseguramos una base sólida para el backend de nuestro proyecto de desarrollo fullstack.