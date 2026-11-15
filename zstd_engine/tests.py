import io
import zstandard as zstd
from django.test import TestCase, RequestFactory, override_settings
from django.http import HttpResponse, StreamingHttpResponse
from django.core.files.base import ContentFile
from zstd_engine.middleware import (
    compress_data,
    decompress_data,
    accepts_zstd,
    ZstandardMiddleware,
    ZstandardStorage,
)


class ZstandardEngineTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # ==========================================
    # 1. CORE COMPRESSION / DECOMPRESSION TESTS
    # ==========================================
    def test_core_compression_roundtrip(self):
        original_text = b"Edunexa Zstandard compression test payload string data..." * 10
        compressed = compress_data(original_text)
        decompressed = decompress_data(compressed)
        self.assertEqual(original_text, decompressed)

    def test_decompression_size_limit(self):
        original_text = b"A" * (2 * 1024 * 1024)  # 2MB
        compressed = compress_data(original_text)
        with self.assertRaises(ValueError):
            decompress_data(compressed, max_size=1024)

    # ==========================================
    # 2. HTTP NEGOTIATION TESTS
    # ==========================================
    def test_accepts_zstd_header(self):
        request = self.factory.get("/", HTTP_ACCEPT_ENCODING="gzip, zstd, deflate")
        self.assertTrue(accepts_zstd(request))

        request_no_zstd = self.factory.get("/", HTTP_ACCEPT_ENCODING="gzip, deflate")
        self.assertFalse(accepts_zstd(request_no_zstd))

        request_q_zero = self.factory.get("/", HTTP_ACCEPT_ENCODING="zstd;q=0")
        self.assertFalse(accepts_zstd(request_q_zero))

    # ==========================================
    # 3. HTTP RESPONSE COMPRESSION TESTS
    # ==========================================
    @override_settings(ZSTD_ENABLED=True, ZSTD_RESPONSE_ENABLED=True)
    def test_middleware_response_compression(self):
        # Make payload larger than ZSTD_MINIMUM_SIZE (1024 bytes)
        large_payload = b"Hello, this is a compressible JSON-like or text response payload for testing Zstandard compression middleware pipeline performance. " * 20

        def dummy_view(request):
            return HttpResponse(
                large_payload,
                content_type="text/plain"
            )

        middleware = ZstandardMiddleware(dummy_view)
        request = self.factory.get("/", HTTP_ACCEPT_ENCODING="zstd")
        response = middleware(request)

        self.assertEqual(response["Content-Encoding"], "zstd")
        self.assertIn("Accept-Encoding", response["Vary"])
        
        decompressed = decompress_data(response.content)
        self.assertEqual(decompressed, large_payload)

    # ==========================================
    # 4. HTTP REQUEST DECOMPRESSION TESTS
    # ==========================================
    @override_settings(ZSTD_ENABLED=True, ZSTD_REQUEST_ENABLED=True)
    def test_middleware_request_decompression(self):
        raw_payload = b'{"action": "sync", "status": "active"}'
        compressed_payload = compress_data(raw_payload)

        def dummy_view(request):
            # Read from request stream/body directly after middleware processing
            body_content = request.read()
            return HttpResponse(body_content, content_type="application/json")

        middleware = ZstandardMiddleware(dummy_view)
        request = self.factory.post(
            "/api/",
            data=compressed_payload,
            content_type="application/json",
            HTTP_CONTENT_ENCODING="zstd"
        )
        
        response = middleware(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, raw_payload)

    # ==========================================
    # 5. STREAMING RESPONSE COMPRESSION TESTS
    # ==========================================
    @override_settings(ZSTD_ENABLED=True, ZSTD_RESPONSE_ENABLED=True)
    def test_streaming_response_compression(self):
        def streaming_view(request):
            def generator():
                yield b"Chunk one data stream padding block bytes content text. " * 30
                yield b"Chunk two data stream padding block bytes content text. " * 30
            return StreamingHttpResponse(generator(), content_type="text/plain")

        middleware = ZstandardMiddleware(streaming_view)
        request = self.factory.get("/", HTTP_ACCEPT_ENCODING="zstd")
        response = middleware(request)

        self.assertEqual(response["Content-Encoding"], "zstd")
        
        compressed_chunks = list(response.streaming_content)
        full_compressed = b"".join(compressed_chunks)
        
        decompressed = decompress_data(full_compressed)
        self.assertIn(b"Chunk one data stream", decompressed)
        self.assertIn(b"Chunk two data stream", decompressed)

    # ==========================================
    # 6. STORAGE ENGINE TESTS
    # ==========================================
    def test_zstandard_storage_roundtrip(self):
        storage = ZstandardStorage()
        sample_data = b"Secret secure document archive content block bytes..." * 50
        file_content = ContentFile(sample_data)

        file_name = storage.save("unit_test_doc.txt", file_content)

        try:
            with storage.open(file_name, "rb") as f:
                read_data = f.read()
                self.assertEqual(sample_data, read_data)
        finally:
            storage.delete(file_name)