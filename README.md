# Edunexa
## Learning, Thinking, Research & Experimentation Journal

**Project Name:** Edunexa

**Project Status:** Under Development

**Project Start Date:** 15 November 2026 

---

# Edunexa — Development Server Commands

**Virtual Environment**

```bash
source /home/matin/Desktop/Edunexa-/venv/bin/activate
```

| Service | Command |
|---|---|
| WebSocket — Daphne | `daphne -b 127.0.0.1 -p 8000 Edunexa.asgi:application` |
| Redis | `redis-server` |
| Celery Worker | `celery -A Edunexa worker -l info` |
| Celery Beat | `celery -A Edunexa beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler` |
| Django | `python manage.py runserver 8001` |


# 1. The Real Goal
The goal of Edunexa is to explore new concepts, understand how they work, investigate their underlying principles, and apply that knowledge through practical experiments.

# 2 WebSocket — Real-Time Communication

### 2.1 Purpose

WebSocket is a communication protocol that allows a client and server to maintain a persistent, two-way connection.

Unlike traditional HTTP request-response communication, WebSocket allows both sides to send messages through an established connection without creating a new HTTP request for every message.

The purpose of studying WebSocket in Edunexa is to understand real-time communication, asynchronous processing, connection management and event-driven architecture.


### 2.2 Technologies and Libraries

| Technology / Library | Purpose |
|---|---|
| WebSocket | Two-way communication between client and server |
| Django Channels | Adds asynchronous and WebSocket capabilities to Django |
| ASGI | Asynchronous server interface used by Django applications |
| Daphne | ASGI server that handles WebSocket connections |
| Redis | Supports communication between channel layers |
| channels_redis | Redis-backed channel layer for Django Channels |


## 3. Zstandard — Data Compression and Performance Engineering

### 3.1 Purpose

Zstandard (Zstd) is a data compression algorithm designed to reduce data size while providing fast compression and decompression.

The purpose of studying Zstandard in Edunexa is to understand how compression algorithms work, how compression levels affect output size and processing time, and how compression influences application performance and resource consumption.

The investigation focuses on the relationship between:

- Original data size.
- Compressed data size.
- Compression level.
- Compression time.
- Decompression time.
- CPU consumption.
- Memory usage.
- Network data transfer.

### 3.2 Technology and Libraries

| Technology / Library | Purpose |
|---|---|
| Zstandard | Data compression algorithm |
| zstandard | Python implementation and interface for Zstandard |
| Django | Integration with HTTP request and response processing |
| Middleware | Centralized compression and decompression handling |
| Python | Experimentation, implementation and measurement |

### 3.3 Compression Concepts Being Studied

1. Lossless data compression.
2. Compression and decompression.
3. Compression levels and their trade-offs.
4. Compression ratios.
5. CPU processing cost.
6. Memory consumption.
7. Streaming compression.
8. Request decompression.
9. Response compression.
10. HTTP content negotiation.
11. Compressed data storage.
12. Maximum compressed and decompressed size limits.

### 3.4 Historical Compression Benchmark — Nexora

An earlier experiment was conducted in the historical Nexora project to compare Zstandard compression levels 3, 11 and 22.

These measurements are historical experimental evidence, not a benchmark of the current Edunexa implementation.

#### Compressed Output Size

| Page | Original Size | Level 3 | Level 11 | Level 22 |
|---|---:|---:|---:|---:|
| Homepage | 840,000 B | 136 B | 136 B | 130 B |
| Admin | 21,819 B | 3,129 B | 2,885 B | 2,796 B |
| Admin Home | 12,650 B | 2,391 B | 2,286 B | 2,227 B |
| Admin Login | 4,084 B | 1,578 B | 1,523 B | 1,497 B |

#### CPU Processing Time

| Page | Level 11 | Level 22 |
|---|---:|---:|
| Homepage | 5.538 ms | 6.615 ms |
| Admin | 0.529 ms | 11.939 ms |
| Admin Home | 0.698 ms | 6.598 ms |
| Admin Login | 0.674 ms | 0.919 ms |

Level 3 CPU measurements were not recorded in this benchmark.

#### Comparison: Level 22 vs Level 11

| Page | CPU Time Difference |
|---|---:|
| Homepage | 1.19× |
| Admin | 22.57× |
| Admin Home | 9.45× |
| Admin Login | 1.36× |

### 3.5 Experimental Observations

The measurements showed that:

- Higher compression levels produced smaller output files.
- The additional reduction from Level 11 to Level 22 was relatively small.
- Level 22 required substantially more CPU time on some pages.
- Compression behaviour differed between pages.
- The homepage produced unusually high compression, suggesting highly repetitive or compressible content.

The experiment demonstrated that the smallest compressed output does not necessarily provide the best overall performance.

A compression configuration must consider both data reduction and processing cost.

### 3.6 Limitations of the Historical Benchmark

The benchmark had several limitations:

- CPU measurements were individual measurements.
- Memory consumption was not sufficiently evaluated.
- Actual internet transfer performance was not measured.
- Concurrent user behaviour was not tested.
- Streaming compression was not included in the historical middleware.
- Level 3 CPU measurements were unavailable.
- The unusually compressible homepage should not be treated as representative of every type of content.

Therefore, the historical results are useful for understanding the trade-offs but are not sufficient to establish a universal optimal compression level.

### 3.7 Current Edunexa Implementation

The current Edunexa project contains a more extensive Zstandard compression implementation.

| Component | Current Implementation |
|---|---|
| Zstandard Engine | Compression and decompression functionality |
| Request Decompression | Handles compressed incoming request data |
| Response Compression | Compresses outgoing HTTP responses |
| Streaming Compression | Supports streaming response compression |
| Content Negotiation | Handles client compression support |
| Size Limits | Restricts incoming and decompressed data sizes |
| Zstandard Storage | Custom `ZstandardStorage` implementation |
| Temporary Files | Handles temporary-file operations |

#### Current Configuration

| Setting | Value |
|---|---:|
| Compression Level | 22 |
| Minimum Compression Size | 1,024 bytes |
| Maximum Request Size | 50 MB |
| Maximum Decompressed Size | 100 MB |

### 3.8 Testing and Verification

Tests have been written for the following areas:

- Compression and decompression round trips.
- Request size limits.
- Content negotiation.
- Request compression.
- Response compression.
- Streaming compression.
- Custom storage.
- Temporary-file handling.

**Testing status:** Tests are written. Their successful execution and results must be recorded separately; writing a test does not establish that it passed.

### 3.9 Further Learning

Future investigations can compare:

1. Zstandard with Brotli and gzip.
2. Different compression levels.
3. Compression speed and decompression speed.
4. CPU and RAM consumption.
5. Small files versus large files.
6. Text, JSON, HTML and binary data.
7. Streaming versus non-streaming compression.
8. Single requests versus concurrent requests.
9. Compression overhead versus network transfer savings.
10. Different compression settings under realistic workloads.

### 3.10 Expected Learning Outcome

Understand how lossless compression works, how compression algorithms trade processing resources for data reduction, and how compression can be integrated into a web application.

The broader objective is to develop performance-engineering knowledge by measuring actual behaviour rather than selecting configurations based only on theoretical compression ratios.

# 4. Background Tasks, Scheduled Tasks and Caching

## 4.1 Background Tasks — Celery

### Purpose

Celery is used to execute tasks in the background instead of making the user wait for lengthy operations during a normal Django HTTP request.

The objective is to understand how task queues, workers and message brokers work together to execute operations independently of the main request-response process.

### Technologies

| Technology / Library | Version | Purpose |
|---|---:|---|
| Celery | 5.7.0 | Background task processing |
| Kombu | 5.7.0 | Messaging and transport management |
| billiard | 4.3.2 | Multiprocessing support |
| Redis | 8.1.0 | Message broker client |
| Django | 6.0.10 | Application framework |


### Learning Objectives

- Background task execution.
- Task queues and message brokers.
- Worker processes.
- Asynchronous processing.
- Multiprocessing and concurrency.
- Task registration and discovery.
- Task execution status.
- Error handling and retries.

## 4.2 Scheduled Tasks — Celery Beat

### Purpose

Celery Beat is used to schedule background tasks for execution at predefined times or recurring intervals.

The objective is to understand how scheduled operations are triggered automatically and how a scheduler communicates with Celery workers through a message broker.

### Technologies

| Technology / Library | Version | Purpose |
|---|---:|---|
| Celery | 5.7.0 | Executes background tasks |
| django-celery-beat | 2.9.0 | Database-backed periodic task scheduling |
| Redis | 8.1.0 | Transfers scheduled task messages |
| Django | 6.0.10 | Application and database integration |

### Learning Objectives

- Periodic task scheduling.
- Cron-based scheduling.
- Database-backed schedules.
- Scheduler and worker communication.
- Time zones and UTC.
- Task execution timing.
- Missed and delayed tasks.
- Repeated task execution.


## 4.3 Caching — Redis

### Purpose

Redis is configured as the Django caching backend.

Caching stores data temporarily so that frequently requested information can be retrieved without repeating the original processing or database operation.

The objective is to understand in-memory data storage, cache retrieval, expiration, invalidation and performance.

### Technologies

| Technology / Library | Version | Purpose |
|---|---:|---|
| Redis | 8.1.0 | Python Redis client |
| django-redis | 7.0.0 | Additional Django Redis integration |
| Django | 6.0.10 | Built-in caching framework |


### Learning Objectives

- In-memory data storage.
- Cache keys and values.
- Cache expiration and TTL.
- Cache hits and misses.
- Cache invalidation.
- Data serialization.
- Memory consumption.
- Cache consistency.
- Performance comparison between cached and uncached operations.

## 4.4 Overall Learning Objective

Understand how three different systems cooperate within a Django application:

1. **Celery:** Executes background tasks.
2. **Celery Beat:** Schedules tasks for execution.
3. **Redis:** Provides message-broker and caching functionality.

# 5. Centralized Security Middleware — Request Monitoring and History

## 5.1 Overview

Edunexa implements a custom Django middleware named `SecurityMiddleware`, located in:

`security/middleware.py`

This middleware is part of the Edunexa security system. Its primary responsibility is to monitor incoming website requests and maintain request-history records for both authenticated and unauthenticated users.

The middleware provides a centralized point for collecting request activity throughout the application.

Its current responsibilities include:

1. Monitoring incoming requests.
2. Identifying authenticated and unauthenticated users.
3. Recording request history.
4. Associating requests with user accounts or anonymous identifiers.
5. Checking whether requested URL paths can be resolved by Django.
6. Storing request information for later review.

## 5.2 Central Request Monitoring

The middleware processes requests through Django's middleware lifecycle.

It checks the authentication status of each request and records the corresponding activity in the `userhistory` database model.

There are two identification paths:

| Request identity | Identification method | History association |
|---|---|---|
| Authenticated user | Django authentication system | User account |
| Unauthenticated user | `tapmuser` cookie | Anonymous user code |

Both paths contribute to the same request-history system.

The objective is to maintain a record of application activity rather than monitor only anonymous visitors.

## 5.3 Request History Data Structure

The `userhistory` model is defined in `security/models.py`.

It stores the following information:

| Field | Type | Purpose |
|---|---|---|
| `user_names` | ForeignKey to Django User | Associates a request with an authenticated account |
| `User_Code` | TextField | Stores an anonymous identifier |
| `Path` | TextField | Stores the absolute request URL |
| `method` | CharField | Stores the HTTP request method |
| `found` | BooleanField | Stores the URL-resolution result |
| `Date` | DateTimeField | Automatically records the creation time |

Both `user_names` and `User_Code` allow null values.

This model supports two identification methods within one request-history structure.

## 5.4 Authenticated Request Monitoring

When Django identifies a request as authenticated, the middleware records the request against the authenticated user.

The following information is stored:

- User account.
- Absolute request URL.
- HTTP method.
- URL-resolution status.
- Record creation timestamp.

The record is created before the middleware calls `self.get_response(request)`.

This means the request history is recorded before the downstream response processing finishes.

## 5.5 Unauthenticated Request Monitoring

When Django identifies a request as unauthenticated, the middleware uses a cookie named `tapmuser` to associate requests with an anonymous identifier.

If the incoming request does not contain this cookie, the middleware generates a new identifier and adds it to the outgoing response.

The current identifier-generation function:

- Uses uppercase and lowercase letters.
- Uses digits.
- Uses punctuation characters.
- Generates a string with a length of 500 characters.
- Uses a 30-day cookie lifetime.

The middleware then creates a request-history record using the incoming request's cookie value.

The anonymous identification mechanism is only one part of the broader request-monitoring system.

## 5.6 URL Resolution Monitoring

The middleware defines `check_url_status(url_path)`.

It uses Django's `resolve()` function to check whether a requested path matches a configured URL pattern.

The result is stored in the `found` field.

- `True`: Django successfully resolves the URL path.
- `False`: Django raises `Resolver404`.

This provides information about requests to paths that do not match the application's URL configuration.

This check does not establish whether a user has permission to access a resource or whether the final HTTP response is successful.

## 5.7 Middleware Execution Flow

The current implementation follows this sequence:

1. Receive an incoming request.
2. Check whether the user is authenticated.
3. If authenticated, create a request-history record associated with the user account.
4. Pass the request to the next response handler.
5. If unauthenticated, check whether the incoming request contains `tapmuser`.
6. If the cookie is missing, generate an identifier and attach it to the outgoing response.
7. Create an anonymous request-history record using the incoming cookie value.
8. Return the response.

## 5.8 Security Data and Administrative Review

The request-history records collected by the middleware serve two purposes within Edunexa's security architecture:

**1. Security analysis and investigation**

The collected request data provides information that can be used by the security system to analyze application activity, investigate unusual request patterns and support security-related decisions.

The `userhistory` model maintains information such as user identity, anonymous identifier, request path, HTTP method, URL-resolution status and timestamp.

This data forms part of the security system's activity-history foundation.

**2. Administrative review**

The `security/admin.py` file registers the `userhistory` model with Django Admin.

Administrators can inspect the collected request-history records through the administrative interface.

The current list display includes:

- Record ID.
- User account.
- Request path.
- Date.
- HTTP method.
- URL-resolution status.

The administrative interface provides human visibility into the same request-history data that can support security analysis.

**Important distinction:** Django Admin currently provides record inspection. The middleware itself collects the data. Any automated security analysis or decision-making using these records must be documented according to its actual implementation.


#  Python Libraries and Dependencies

| No. | Python Library | Version | Primary Purpose |
|---:|---|---|---|
| 1 | amqp | 5.4.2 | AMQP messaging protocol |
| 2 | asgiref | 3.13.0 | ASGI and asynchronous utilities |
| 3 | attrs | 26.1.0 | Classes and structured data attributes |
| 4 | autobahn | 26.11.1 | WebSocket and WAMP communication |
| 5 | Automat | 25.4.16 | State-machine and workflow automation |
| 6 | billiard | 4.3.2 | Multiprocessing support for Celery |
| 7 | brotli | 1.2.1 | Brotli data compression |
| 8 | cbor2 | 6.3.0 | CBOR binary data serialization |
| 9 | celery | 5.7.0 | Background task processing |
| 10 | certifi | 2026.10.23 | Trusted CA certificates |
| 11 | cffi | 2.1.1 | Calling C code from Python |
| 12 | channels | 4.3.2 | Django asynchronous and real-time communication |
| 13 | channels_redis | 4.3.0 | Redis channel-layer backend for Django Channels |
| 14 | charset-normalizer | 3.5.2 | Character encoding detection |
| 15 | click | 8.5.1 | Command-line interface development |
| 16 | click-didyoumean | 0.3.1 | Command-line suggestion support |
| 17 | click-plugins | 1.1.1.2 | Click command-line plugin support |
| 18 | click-repl | 0.4.1 | Interactive command-line interfaces |
| 19 | constantly | 23.10.4 | Constant values and utilities |
| 20 | cron-descriptor | 1.4.5 | Human-readable cron descriptions |
| 21 | cryptography | 50.0.2 | Cryptographic operations and encryption |
| 22 | daphne | 4.2.3 | ASGI server |
| 23 | Django | 6.0.10 | Web application framework |
| 24 | django-celery-beat | 2.9.0 | Periodic task scheduling for Celery |
| 25 | django-debug-toolbar | 8.0.0 | Django debugging and performance inspection |
| 26 | django-filter | 26.2 | Filtering Django querysets |
| 27 | django-http-compression | 1.5.0 | HTTP response compression |
| 28 | django-redis | 7.0.0 | Redis cache integration for Django |
| 29 | django-timezone-field | 7.2.2 | Time-zone fields for Django models |
| 30 | djangorestframework | 3.18.3 | REST API development |
| 31 | hyperlink | 21.0.0 | URL and hyperlink handling |
| 32 | idna | 3.20 | Internationalized domain names |
| 33 | Incremental | 24.11.0 | Incremental version management |
| 34 | kombu | 5.7.0 | Messaging and transport abstraction for Celery |
| 35 | Markdown | 3.11.3 | Markdown text processing |
| 36 | msgpack | 1.2.4 | MessagePack serialization |
| 37 | packaging | 26.3 | Python package version and requirement handling |
| 38 | prompt_toolkit | 3.0.53 | Interactive command-line input |
| 39 | pycparser | 3.12 | C parser written in Python |
| 40 | pyOpenSSL | 26.4.0 | OpenSSL integration for Python |
| 41 | python-crontab | 3.4.0 | Cron job management |
| 42 | python-dateutil | 2.9.0.post0 | Date and time utilities |
| 43 | redis | 8.1.0 | Redis client for Python |
| 44 | requests | 2.34.2 | HTTP requests |
| 45 | service-identity | 26.1.0 | TLS service identity verification |
| 46 | six | 1.17.0 | Python 2 and 3 compatibility utilities |
| 47 | sqlparse | 0.6.1 | SQL parsing and formatting |
| 48 | Twisted | 26.10.0 | Asynchronous networking framework |
| 49 | txaio | 26.6.1 | Asyncio and Twisted compatibility utilities |
| 50 | typing_extensions | 4.16.0 | Extended Python typing features |
| 51 | tzdata | 2026.6 | Time-zone database |
| 52 | tzlocal | 5.4.5 | Local time-zone detection |
| 53 | ujson | 6.1.0 | Fast JSON encoding and decoding |
| 54 | urllib3 | 2.8.0 | HTTP client and connection management |
| 55 | vine | 5.1.0 | Function and callback utilities |
| 56 | wcwidth | 0.9.4 | Terminal character-width calculation |
| 57 | zope.interface | 8.7 | Interfaces and component contracts |


