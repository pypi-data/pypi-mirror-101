import asyncio
import os
from concurrent.futures.process import ProcessPoolExecutor
from secrets import token_hex
from pathlib import Path
from tempfile import mkdtemp
from loguru import logger as log
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import iscc as iscclib
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE
import iscc_service
from iscc_service.config import ALLOWED_ORIGINS
from starlette.middleware.cors import CORSMiddleware
from iscc_service.utils import secure_filename
import aiofiles
from iscc.schema import ISCC

app = FastAPI(
    title="ISCC Web Service API",
    version=iscc_service.__version__,
    description="Microservice for creating ISCC Codes from Media Files.",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/code_iscc",
    summary="Generate ISCC from File",
    response_model=ISCC,
    response_model_exclude_unset=True,
    tags=["generate"],
)
async def code_iscc(
    file: UploadFile = File(...), title: str = Form(""), extra: str = Form(""),
):
    """Generate Full ISCC Code from Media File with optional explicit metadata."""

    filename = secure_filename(file.filename) or token_hex(16)
    tmp_dir = mkdtemp()
    tmp_file_path = Path(tmp_dir, filename)

    async with aiofiles.open(tmp_file_path, "wb") as out_file:
        await file.seek(0)
        data = await file.read(4096)
        # Exit early on unsupported mediatype
        mediatype = iscclib.mime_guess(data, filename)
        if not iscclib.mime_supported(mediatype):
            raise HTTPException(
                HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "Unsupported media type '{}'. Please request support at "
                "https://github.com/iscc/iscc-service/issues.".format(mediatype),
            )
        while data:
            await out_file.write(data)
            data = await file.read(1024 * 1024)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        app.state.executor, iscclib.code_iscc, tmp_file_path, title, extra
    )

    try:
        os.remove(tmp_file_path)
    except Exception:
        log.warning(f"could not remove {tmp_file_path}")

    try:
        os.rmdir(tmp_dir)
    except Exception:
        log.warning(f"could not remove {tmp_dir}")

    return result


@app.get("/explain/{iscc}", tags=["tools"])
async def explain(iscc: str):
    """Explain details of an ISCC code"""
    code_obj = iscclib.Code(iscc)
    code_objs = iscclib.decompose(code_obj)
    decomposed = "-".join(c.code for c in code_objs)
    components = {
        c.code: {
            "readable": c.explain,
            "hash_hex": c.hash_hex,
            "hash_uint": str(c.hash_uint),
            "hash_bits": c.hash_bits,
        }
        for c in code_objs
    }
    return dict(
        iscc=code_obj.code,
        readable=code_obj.explain,
        decomposed=decomposed,
        components=components,
    )


@app.on_event("startup")
async def on_startup():
    from iscc_service import init

    init.init()
    app.state.options = iscclib.Options()
    app.state.executor = ProcessPoolExecutor()


@app.on_event("shutdown")
async def on_shutdown():
    app.state.executor.shutdown()


def run_server():
    uvicorn.run("iscc_service.main:app", host="127.0.0.1", port=8080, reload=False)


if __name__ == "__main__":
    uvicorn.run("iscc_service.main:app", host="127.0.0.1", port=8080, reload=True)
