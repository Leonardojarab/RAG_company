import json
from pathlib import Path
from pydantic import BaseModel, Field

TEST_FILE = str(Path(__file__).parent / "tests.jsonl")


class TestQuestion(BaseModel):  #Define una clase Pydantic llamada TestQuestion. valida tipos automáticamente, transforma datos (si puede), lanza errores claros si faltan campos o hay tipos mal
    """A test question with expected keywords and reference answer."""

    question: str = Field(description="The question to ask the RAG system")
    keywords: list[str] = Field(description="Keywords that must appear in retrieved context")
    reference_answer: str = Field(description="The reference answer for this question")
    category: str = Field(description="Question category (e.g., direct_fact, spanning, temporal)")


def load_tests() -> list[TestQuestion]:  #Define una función que devuelve una lista de TestQuestion.
    """Load test questions from JSONL file."""
    tests = []
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            tests.append(TestQuestion(**data))  #Crea un TestQuestion usando desempaquetado de diccionario (**data). Pydantic valida que: existan los campos requeridos. los tipos sean correctos (o convertibles). Si algo está mal, lanza un error indicando qué campo falló.
    return tests

#Convierte un archivo tests.jsonl (una pregunta por línea) en una lista de objetos validados por Pydantic, listos para evaluar tu RAG.