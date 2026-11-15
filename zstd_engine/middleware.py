"""
Edunexa - Centralized Zstandard Engine

Features:
- HTTP request decompression
- HTTP response compression
- GET, POST, PUT, PATCH, DELETE
- Streaming request decompression
- Streaming response compression
- Zstandard file storage
- File upload compression
- Transparent file download decompression
- Size limits
- Compression negotiation

Dependency:
    pip install zstandard
"""

import io
import tempfile
import zstandard as zstd

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


# ==========================================================
# 1. CONFIGURATION
# ==========================================================

LEVEL = 22

CHUNK_SIZE = 64 * 1024

TEMP_MEMORY_LIMIT = 8 * 1024 * 1024

COMPRESSIBLE_TYPES = (
    "text/",
    "application/json",
    "application/javascript",
    "application/xml",
    "application/xhtml+xml",
    "image/svg+xml",
)


def config(name, default):
    return getattr(settings, name, default)


# ==========================================================
# 2. COMPRESSION ENGINE
# ==========================================================

def compress_data(data, level=LEVEL):
    return zstd.ZstdCompressor(
        level=level
    ).compress(data)


def decompress_data(data, max_size=None):
    max_size = max_size or config(
        "ZSTD_MAX_DECOMPRESSED_SIZE",
        100 * 1024 * 1024
    )

    output = bytearray()

    with zstd.ZstdDecompressor().stream_reader(
        io.BytesIO(data)
    ) as reader:

        while True:
            chunk = reader.read(CHUNK_SIZE)

            if not chunk:
                break

            output.extend(chunk)

            if len(output) > max_size:
                raise ValueError("Decompressed size limit exceeded")

    return bytes(output)


# ==========================================================
# 3. HTTP NEGOTIATION
# ==========================================================

def accepts_zstd(request):
    header = request.headers.get(
        "Accept-Encoding", ""
    )

    wildcard_quality = None

    for item in header.split(","):
        parts = item.strip().split(";")
        encoding = parts[0].strip().lower()
        quality = 1.0

        for parameter in parts[1:]:
            key, separator, value = parameter.partition("=")

            if separator and key.strip().lower() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0

        if encoding == "zstd":
            return 0 < quality <= 1

        if encoding == "*":
            wildcard_quality = quality

    return bool(
        wildcard_quality is not None
        and 0 < wildcard_quality <= 1
    )


def add_vary(response):
    existing = response.get("Vary", "")

    values = [
        item.strip()
        for item in existing.split(",")
        if item.strip()
    ]

    if "*" in values:
        return

    if "accept-encoding" not in [
        value.lower() for value in values
    ]:
        values.append("Accept-Encoding")

    response["Vary"] = ", ".join(values)


# ==========================================================
# 4. HTTP RESPONSE COMPRESSION
# ==========================================================

def compress_response(request, response):
    add_vary(response)

    if not accepts_zstd(request):
        return response

    if response.streaming:
        return response

    if request.method == "HEAD":
        return response

    if response.status_code < 200:
        return response

    if response.status_code in (204, 206, 304):
        return response

    if response.get("Content-Encoding"):
        return response

    if response.get("Content-Range"):
        return response

    if "no-transform" in response.get(
        "Cache-Control", ""
    ).lower():
        return response

    content_type = response.get(
        "Content-Type", ""
    ).lower()

    if not any(
        content_type.startswith(item)
        for item in COMPRESSIBLE_TYPES
    ):
        return response

    original = response.content

    minimum = config(
        "ZSTD_MINIMUM_SIZE",
        1024
    )

    if len(original) < minimum:
        return response

    compressed = compress_data(
        original,
        config("ZSTD_COMPRESSION_LEVEL", LEVEL)
    )

    if len(compressed) >= len(original):
        return response

    response.content = compressed
    response["Content-Encoding"] = "zstd"
    response["Content-Length"] = str(
        len(compressed)
    )

    response.headers.pop("ETag", None)
    response.headers.pop("Content-MD5", None)

    return response


# ==========================================================
# 5. REQUEST DECOMPRESSION
# ==========================================================

def decompress_request(request):
    encoding = request.headers.get(
        "Content-Encoding", ""
    ).strip().lower()

    if not encoding or encoding == "identity":
        return None, None

    if encoding != "zstd":
        return HttpResponse(
            "Unsupported Content-Encoding",
            status=415
        ), None

    compressed_limit = config(
        "ZSTD_MAX_REQUEST_SIZE",
        50 * 1024 * 1024
    )

    decompressed_limit = config(
        "ZSTD_MAX_DECOMPRESSED_SIZE",
        100 * 1024 * 1024
    )

    length = request.META.get("CONTENT_LENGTH")

    if length:
        try:
            if int(length) > compressed_limit:
                return HttpResponse(
                    "Request too large",
                    status=413
                ), None
        except ValueError:
            return HttpResponse(
                "Invalid Content-Length",
                status=400
            ), None

    temporary = None

    try:
        compressed = request.body

        if len(compressed) > compressed_limit:
            return HttpResponse(
                "Compressed request too large",
                status=413
            ), None

        temporary = tempfile.SpooledTemporaryFile(
            max_size=TEMP_MEMORY_LIMIT,
            mode="w+b"
        )

        total = 0

        with zstd.ZstdDecompressor().stream_reader(
            io.BytesIO(compressed)
        ) as reader:

            while True:
                chunk = reader.read(CHUNK_SIZE)

                if not chunk:
                    break

                total += len(chunk)

                if total > decompressed_limit:
                    raise ValueError(
                        "Decompressed request too large"
                    )

                temporary.write(chunk)

        temporary.seek(0)

        request._body = None
        request._stream = temporary
        request._read_started = False

        request.META["CONTENT_LENGTH"] = str(total)
        request.META.pop(
            "HTTP_CONTENT_ENCODING",
            None
        )

        return None, temporary

    except Exception:
        if temporary:
            temporary.close()

        return HttpResponse(
            "Invalid or oversized Zstandard request",
            status=400
        ), None


# ==========================================================
# 6. STREAMING RESPONSE COMPRESSION
# ==========================================================

class _NonClosingWriter:
    def __init__(self):
        self.output = []

    def write(self, data):
        if data:
            self.output.append(data)
        return len(data)

    def flush(self):
        pass

    def close(self):
        pass


def compress_streaming_response(request, response):
    add_vary(response)

    if not accepts_zstd(request):
        return response

    if request.method == "HEAD":
        return response

    if response.status_code != 200:
        return response

    if response.get("Content-Encoding"):
        return response

    if response.get("Content-Range"):
        return response

    content_type = response.get(
        "Content-Type", ""
    ).lower()

    if not any(
        content_type.startswith(item)
        for item in COMPRESSIBLE_TYPES
    ):
        return response

    original_iterator = response.streaming_content

    def compressed_iterator():
        compressor = zstd.ZstdCompressor(
            level=config(
                "ZSTD_COMPRESSION_LEVEL",
                LEVEL
            )
        )

        writer_obj = _NonClosingWriter()

        try:
            with compressor.stream_writer(
                writer_obj
            ) as writer:

                for chunk in original_iterator:
                    if isinstance(chunk, str):
                        chunk = chunk.encode(
                            response.charset or "utf-8"
                        )

                    writer.write(chunk)

                    while writer_obj.output:
                        yield writer_obj.output.pop(0)

                writer.flush(zstd.FLUSH_FRAME)

                while writer_obj.output:
                    yield writer_obj.output.pop(0)

        finally:
            close = getattr(
                original_iterator,
                "close",
                None
            )

            if close:
                close()

    response.streaming_content = compressed_iterator()
    response["Content-Encoding"] = "zstd"

    response.headers.pop("Content-Length", None)
    response.headers.pop("ETag", None)

    return response


# ==========================================================
# 7. FILE STORAGE
# ==========================================================

class _NonClosingFileWrapper:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        return self.stream.write(data)

    def flush(self):
        if hasattr(self.stream, "flush"):
            self.stream.flush()

    def close(self):
        pass


class ZstandardStorage(FileSystemStorage):

    def __init__(
        self,
        location=None,
        base_url=None,
        compression_level=LEVEL,
        max_file_size=2 * 1024 * 1024 * 1024,
        **kwargs
    ):
        super().__init__(
            location=location,
            base_url=base_url,
            **kwargs
        )

        self.level = compression_level
        self.max_file_size = max_file_size

    def _save(self, name, content):
        temporary = tempfile.SpooledTemporaryFile(
            max_size=TEMP_MEMORY_LIMIT,
            mode="w+b"
        )

        total = 0

        try:
            compressor = zstd.ZstdCompressor(
                level=self.level
            )

            wrapped_temporary = _NonClosingFileWrapper(temporary)

            with compressor.stream_writer(
                wrapped_temporary
            ) as writer:

                for chunk in content.chunks():
                    total += len(chunk)

                    if total > self.max_file_size:
                        raise ValueError(
                            "File size limit exceeded"
                        )

                    writer.write(chunk)

            temporary.seek(0)

            return super()._save(
                name,
                File(temporary, name=name)
            )

        except Exception:
            temporary.close()
            raise

    def _open(self, name, mode="rb"):
        if mode != "rb":
            raise ValueError(
                "Only read mode is supported"
            )

        original = super()._open(name, "rb")

        temporary = tempfile.SpooledTemporaryFile(
            max_size=TEMP_MEMORY_LIMIT,
            mode="w+b"
        )

        try:
            total = 0

            with zstd.ZstdDecompressor().stream_reader(
                original
            ) as reader:

                while True:
                    chunk = reader.read(CHUNK_SIZE)

                    if not chunk:
                        break

                    total += len(chunk)

                    if total > self.max_file_size:
                        raise ValueError(
                            "Decompressed file size limit exceeded"
                        )

                    temporary.write(chunk)

            temporary.seek(0)

            return File(temporary, name=name)

        except Exception:
            temporary.close()
            raise

        finally:
            original.close()


# ==========================================================
# 8. MAIN MIDDLEWARE
# ==========================================================

class ZstandardMiddleware:

    sync_capable = True
    async_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not config("ZSTD_ENABLED", True):
            return self.get_response(request)

        temporary = None

        try:
            if config("ZSTD_REQUEST_ENABLED", True):
                error, temporary = decompress_request(
                    request
                )

                if error:
                    return error

            response = self.get_response(request)

            if config("ZSTD_RESPONSE_ENABLED", True):
                if response.streaming:
                    response = compress_streaming_response(
                        request,
                        response
                    )
                else:
                    response = compress_response(
                        request,
                        response
                    )

            return response

        finally:
            if temporary:
                temporary.close()