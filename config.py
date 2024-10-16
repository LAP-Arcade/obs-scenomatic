import typing as t
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class Config(BaseModel):
    class Client(BaseModel):
        host: str = Field(default="localhost")
        port: int = Field(default=4444)
        password: str = Field(default="")

    client: Client = Field(default_factory=Client)
    default_scene: str = Field(default=None)
    collection: str = Field(default=None)
    profile: str = Field(default=None)

    class SceneParams(BaseModel):
        match: list[str] = Field(default_factory=list)
        delay: float = Field(default=0.0)

    scenes: dict[str, SceneParams | list[str]] = Field(default_factory=dict)

    @classmethod
    def load(cls) -> "Config":
        path = Path("config.yml")
        if not path.exists():
            with path.open("w") as f:
                yaml.safe_dump(
                    cls.model_validate(
                        {
                            "scenes": {
                                "MyScene1": ["app1.exe"],
                                "MyScene2": {
                                    "match": ["app2.exe"],
                                    "delay": 2.5,
                                },
                            }
                        }
                    ).model_dump(exclude_unset=True),
                    f,
                )
        with path.open() as f:
            return cls.model_validate(yaml.safe_load(f))
