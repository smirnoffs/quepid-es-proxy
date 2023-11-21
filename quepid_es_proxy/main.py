from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .auth import basic_auth
from .elasticsearch import executor

app = FastAPI()

# Replace "*" to the list of your origins, e.g.
# origins = ["quepid.yourcompany.com", "localhost:8080"]  # noqa: ERA001
origins = "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
async def root():
    """Health check"""
    return {"status": "OK"}


class ProxyRequst(BaseModel):
    explain: bool
    from_: int = Field(..., alias="from")
    size: int
    source: str | list[str] | None = Field(None, alias="_source")
    query: dict | None


@app.post("/{index_name}")
async def search_proxy(index_name: str, body: ProxyRequst, username: str = Depends(basic_auth)) -> dict:
    return await executor.search(
        index_name,
        body.from_,
        body.size,
        body.explain,
        body.source,
        {"query": body.query} if body.query else None,
        None,
    )


@app.get("/{index_name}")
async def explain_missing_documents(
    index_name: str,
    _source: str,
    q: str,
    size: int,
    username: str = Depends(basic_auth),
) -> dict:
    return await executor.search(
        index_name,
        0,
        size,
        False,
        _source,
        None,
        q,
    )


@app.post("/{index_name}/_doc/{doc_id}/_explain")
async def explain(
    index_name: str,
    doc_id: str,
    query: dict,
    username: str = Depends(basic_auth),
) -> dict:
    return await executor.explain(index_name, doc_id, query)
