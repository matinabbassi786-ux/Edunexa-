# Edunexa
## Learning, Thinking, Research & Experimentation Journal

**Project Name:** Edunexa

**Project Status:** Under Development

**Project Start Date:** 15 November 2026 

---

# Edunexa — Development Server Commands


### Virtual Environment
```bash
source /home/matin/Desktop/Edunexa-/venv/bin/activate

```

### Django 
```bash
python manage.py runserver 8001
```


### WebSocket — Daphne 
```bash
daphne -b 127.0.0.1 -p 8000 Edunexa.asgi:application
```


### Celery Worker 
```bash
celery -A Edunexa worker -l info
```

### Celery Beat 
```bash
celery -A Edunexa beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```


### Redis 
```bash
redis-server
```

### Valkey 
```bash
valkey-server
```




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

## 5.8 Police System — Wronging and Security Investigation

### 5.8.1 Overview

The Police System represents the investigation authority within Edunexa's Centralized Security Middleware architecture.

Its main component is the Wronging System.

The Police System receives collected user activity from the `userhistory` model and investigates potentially suspicious events. It evaluates available information and assigns a numerical severity level between 0 and 10.

Its responsibility is to investigate and evaluate events, not to make the final user classification.

### 5.8.2 Data Collection — userhistory

The centralized `SecurityMiddleware` records request information in the `userhistory` model.

The collected information includes:

| Field | Purpose |
|---|---|
| `user_names` | Links the record to an authenticated Django user |
| `User_Type` | Stores the user's type |
| `User_Code` | Stores a user identifier |
| `Ip` | Stores the request IP address |
| `user_agent` | Stores browser or client information |
| `language` | Stores the request language |
| `host` | Stores the request host |
| `method` | Stores the HTTP method |
| `Path` | Stores the requested path |
| `path_Short` | Stores a shortened path representation |
| `found` | Stores whether Django resolved the URL |
| `Date` | Records the creation date and time |

These records provide historical information for investigating user activity.

### 5.8.3 Wronging System — Event Investigation

The Wronging System investigates collected events using available information, historical activity, and security rules.

Its responsibilities include:

1. Investigating suspicious requests.
2. Identifying repeated unusual activity.
3. Evaluating unauthorized access attempts.
4. Examining relevant historical activity.
5. Identifying patterns across multiple events.
6. Assigning an event severity score.
7. Recording the investigation result.

The investigation should consider the user's permissions and the actual security context. A URL that does not resolve is not automatically an unauthorized access attempt.

### 5.8.4 Wronging Model — Numerical Evaluation

The `Wronging` model stores the investigation result.

| Field | Type | Purpose |
|---|---|---|
| `Wronging_link` | ForeignKey | Connects the evaluation to its original `userhistory` record |
| `Wronging` | SmallIntegerField | Stores the severity level from 0 to 10 |
| `Wronging_Type` | CharField | Stores the event category |
| `Date` | DateTimeField | Records the evaluation date and time |

The relationship between `Wronging` and `userhistory` preserves the connection between the original event and its investigation result.

### 5.8.5 Wronging Severity Scale

The Wronging System uses a numerical severity scale from 0 to 10.

| Level | Example interpretation |
|---:|---|
| 0 | Normal activity |
| 1 | Minor unusual activity |
| 2 | Low-level suspicious activity |
| 3 | Suspicious or unauthorized activity |
| 4 | Repeated suspicious activity |
| 5 | Multiple unusual events |
| 6 | Significant suspicious activity |
| 7 | High-severity event |
| 8 | Very high-severity event |
| 9 | Critical security event |
| 10 | Highest severity category |

These levels are an illustrative scoring policy. Actual scoring rules must be defined, tested, and validated.

A severity score is an investigation result, not proof of malicious intent.

### 5.8.6 Example — Unauthorized Administrative Access Attempt

Suppose a student named XYZ attempts to access:

`/admin/home/1/editor`

The middleware records the request. The Police System investigates the event using available evidence and user permissions.

Example investigation result:

| Information | Value |
|---|---|
| User | XYZ |
| User type | Student |
| Requested path | `/admin/home/1/editor` |
| Event category | Unauthorized access attempt |
| Wronging level | 8/10 |

The result is stored in the Wronging model.

Example:

```text
Wronging: 8
Wronging_Type: Unauthorized Access Attempt
```

The investigation result is then provided to the Government System for further analytical evaluation.

A single request or numerical score should not automatically cause a permanent restriction.

### 5.8.7 Connection with the Government System

The Police System provides structured investigation information to the Government System.

The Government System uses this information for further analysis through multiple parties and their individual members.

The Police System does not participate in Government voting and does not directly decide whether a user should be placed on the Whitelist, Graylist, or Blacklist.

### 5.8.8 Police System Responsibilities

1. Collect investigation information from `userhistory`.
2. Examine suspicious and unusual activity.
3. Evaluate events using available security evidence.
4. Assign Wronging severity levels.
5. Store investigation results.
6. Maintain a connection between original events and their evaluations.
7. Provide structured information to the Government System.

---

## 5.9 Government System — Political Parties, Analytical Members and Majority Voting

### 5.9.1 Overview

The Government System represents the analytical and decision-making authority within Edunexa's Centralized Security Middleware architecture.

It receives investigation results from the Police System and evaluates them through multiple parties containing individual analytical members.

The structure is inspired by a parliamentary government.

The Government System contains:

- Multiple parties.
- Multiple members within each party.
- Independent analysis by individual members.
- Individual YES or NO voting.
- Overall majority-based decision-making.

BJP and Congress are illustrative examples used to explain the party structure. They are not actual political integrations.

### 5.9.2 Government Party Structure

The Government System can contain multiple parties. Each party represents a group of analytical members.

For example:

| Party | Example analytical members |
|---|---|
| BJP (example) | Random Forest, Logistic Regression, Linear Regression |
| Congress (example) | Statistical Model 1, Statistical Model 2, Statistical Model 3 |
| Probability Party | Probability methods and models |
| Additional parties | Other analytical methods and models |

The party structure can be expanded with additional analytical authorities as the system develops.

The party is an organizational grouping. It does not cast one collective YES or NO vote.

### 5.9.3 Party Members — Independent Analysis

Each party contains multiple members.

Every member independently analyzes the available investigation information according to its own methodology.

Examples include:

**Machine Learning members**
- Random Forest
- Logistic Regression
- Linear Regression
- Other machine-learning models

**Statistics members**
- Statistical analysis methods
- Distribution analysis
- Historical trend analysis
- Other statistical methods

**Probability members**
- Probability calculations
- Likelihood estimation
- Uncertainty analysis
- Other probability methods

Each member produces an individual analytical result and, when eligible, an individual vote.

### 5.9.4 Individual Member Voting

Each participating member votes independently.

The available voting choices are:

- YES
- NO

Example:

**Party A — BJP (illustrative example)**

| Member | Analytical method | Vote |
|---|---|---|
| Member 1 | Random Forest | YES |
| Member 2 | Logistic Regression | NO |
| Member 3 | Linear Regression | YES |
| Member 4 | Additional ML Model | YES |

**Party B — Congress (illustrative example)**

| Member | Analytical method | Vote |
|---|---|---|
| Member 1 | Statistical Method 1 | NO |
| Member 2 | Statistical Method 2 | NO |
| Member 3 | Statistical Method 3 | YES |
| Member 4 | Additional Statistical Method | NO |

Every member's vote is counted individually.

The party does not submit one final YES or NO vote on behalf of all its members.

### 5.9.5 Government-Level Majority Voting

After individual members complete their analysis and voting, the Government System counts all participating members' votes across all parties.

Example:

| Party | YES | NO | Total members |
|---|---:|---:|---:|
| BJP | 3 | 1 | 4 |
| Congress | 1 | 3 | 4 |
| Probability Party | 3 | 1 | 4 |
| **Total** | **7** | **5** | **12** |

Government voting result:

- YES: 7
- NO: 5
- Total participating members: 12

**Final result: YES wins by majority.**

The result is determined by the total number of individual YES and NO votes, not by counting the number of parties supporting each side.

Every participating member has one vote under this voting model.

### 5.9.6 Majority Rule

The Government System follows an overall majority-based decision process.

| YES votes | NO votes | Result |
|---:|---:|---|
| 7 | 3 | YES wins |
| 6 | 4 | YES wins |
| 3 | 7 | NO wins |
| 5 | 5 | Tie |

A tie does not produce a majority decision. The case should be sent for further review or handled through a predefined tie-breaking policy.

The voting system must also define how it handles:

- Abstentions.
- Unavailable members.
- Inactive models.
- Failed analysis.
- Members that do not submit a vote.

Only valid votes should be included in the YES and NO totals. The system should retain the total number of eligible members and the number of members who actually participated.

### 5.9.7 Linear Regression — Future Value Prediction

Linear Regression can be used as one of the analytical members in the Government System.

Its purpose may include predicting future numerical Wronging values based on historical events.

Example:

| Historical event | Wronging value |
|---|---:|
| Event 1 | 2 |
| Event 2 | 3 |
| Event 3 | 5 |
| Event 4 | 6 |
| Predicted next value | 8 |

The predicted value represents a forecast, not an actual recorded Wronging score.

A predefined decision rule can translate the prediction into a YES or NO vote.

Linear Regression predicts numerical values. It does not independently produce a YES or NO classification without a defined decision rule.

### 5.9.8 Government Decision Workflow

```text
             POLICE SYSTEM
             WRONGING RESULT
                    |
                    v
             GOVERNMENT SYSTEM
                    |
          +---------+---------+
          |         |         |
          v         v         v
        PARTY A   PARTY B   PARTY C
          |         |         |
          v         v         v
        MEMBERS   MEMBERS   MEMBERS
          |         |         |
          v         v         v
       INDIVIDUAL YES / NO VOTES
          |         |         |
          +---------+---------+
                    |
                    v
          COUNT ALL MEMBER VOTES
                    |
                    v
             MAJORITY RESULT
                    |
              +-----+-----+
              |           |
              v           v
           YES WINS     NO WINS
              |           |
              +-----+-----+
                    |
                    v
           GOVERNMENT DECISION
                    |
                    v
           SUPREME COURT SYSTEM
```

### 5.9.9 Decision Transparency and Audit History

Every Government decision should maintain an auditable record containing:

- Investigation reference.
- Party identification.
- Member identification.
- Analytical method or model.
- Model version, where applicable.
- Individual vote.
- Supporting analysis or reason.
- Total YES votes.
- Total NO votes.
- Total participating members.
- Final majority result.
- Decision timestamp.

This makes the decision process traceable and supports future review.

### 5.9.10 Government System Responsibilities

1. Receive investigation results from the Police System.
2. Organize analytical members into parties.
3. Distribute relevant information for analysis.
4. Allow individual members to analyze independently.
5. Collect individual YES or NO votes.
6. Count votes across all participating parties.
7. Determine the overall majority.
8. Handle ties and unavailable members according to defined rules.
9. Record voting history and supporting analysis.
10. Forward the Government decision to the Supreme Court System.

The Government System performs analytical evaluation and majority voting. It does not directly apply the final user classification.

---

## 5.10 Supreme Court System — Final Classification and Access Control

### 5.10.1 Overview

The Supreme Court System represents the final classification and enforcement authority within Edunexa's architecture.

It receives the Government System's majority decision and processes the result according to the application's security policies.

Its main responsibility is to determine and apply the appropriate user classification.

The Supreme Court is an architectural analogy for the final application-level authority. It is not a real-world court.

### 5.10.2 User Classification System

The Supreme Court System manages three primary classifications.

#### 1. Whitelist — Trusted Users

Whitelist represents users who are considered trusted under the applicable security policy.

Possible effects:

- Normal access according to account permissions.
- No additional restrictions from this classification.
- Continued security monitoring where required.

#### 2. Graylist — Monitored Users

Graylist represents users who require additional monitoring or review.

Possible effects:

- Additional security checks.
- Restricted access to selected features.
- Continued activity monitoring.
- Review when new evidence becomes available.

#### 3. Blacklist — Restricted or Blocked Users

Blacklist represents users who have been classified as high-risk under the applicable security policy.

Possible effects:

- Blocking access to protected application areas.
- Restricting account activity.
- Preventing access until the required review or appeal process is completed.

In the architecture's analogy, the Blacklist represents a jail or restricted state within the application. It is not a real-world criminal conviction.

### 5.10.3 Classification Process

Suppose the Government System completes its voting process and produces a majority decision recommending that XYZ be placed on the Blacklist.

The Supreme Court System:

1. Receives the Government decision.
2. Checks the decision and its supporting information.
3. Processes the result according to the classification policy.
4. Determines the applicable user classification.
5. Records the classification.
6. Enforces the relevant access restrictions.
7. Notifies the President (Super Admin) for oversight.

### 5.10.4 Classification History

The system should maintain a record of:

- User identification.
- Previous classification.
- New classification.
- Reason for the change.
- Related Government decision.
- Supporting evidence.
- Date and time.
- Enforcement status.
- Later reviews or modifications.

This makes classification changes traceable.

### 5.10.5 Supreme Court Responsibilities

1. Receive and process Government decisions.
2. Apply Whitelist, Graylist, or Blacklist classifications.
3. Enforce access restrictions according to the classification.
4. Maintain classification history.
5. Notify the President (Super Admin).
6. Support authorized review and changes.

The Supreme Court System is the final application-level classification and enforcement authority.

---

## 5.11 President System — Super Admin and Human Oversight

### 5.11.1 Overview

The President represents the Super Admin authority in Edunexa's architecture.

Unlike the Police System and Government System, the President is not an AI model, analytical party, or voting member.

The President is a real human administrator who can observe the system's decisions and intervene when necessary.

The purpose of this layer is to provide human oversight over automated analysis and classification.

### 5.11.2 Super Admin Dashboard

The President (Super Admin) can review information from the security architecture, including:

- User classifications.
- Whitelist records.
- Graylist records.
- Blacklist records.
- Police investigation results.
- Wronging severity levels.
- Government analytical results.
- Party and member information.
- Individual member votes.
- Government majority results.
- Supreme Court decisions.
- Classification history.

This provides visibility into how a decision was reached.

### 5.11.3 Notifications and Human Review

When the Supreme Court System applies an important classification, the President receives a notification.

For example:

1. The Police System investigates XYZ's activity.
2. The Government System analyzes the evidence.
3. Individual members vote YES or NO.
4. The Government System calculates the overall majority.
5. The Supreme Court System processes the decision and places XYZ on the Blacklist.
6. The President receives a notification.
7. The President can inspect the investigation, analysis, voting history, and classification.

### 5.11.4 Human Modification and Override

The President can change a classification when a review shows that a correction is necessary.

Possible changes include:

- Blacklist to Graylist.
- Graylist to Whitelist.
- Whitelist to Graylist.
- Other authorized classification changes.

Every modification should record:

- Administrator identification.
- Previous classification.
- New classification.
- Reason for modification.
- Date and time.

The President does not need to participate in the Government's automated voting process. The President provides a separate human oversight and correction mechanism.

### 5.11.5 President Responsibilities

1. Monitor important security decisions.
2. Review Government voting results.
3. Inspect Supreme Court classifications.
4. Receive notifications.
5. Examine supporting evidence.
6. Correct classifications when necessary.
7. Maintain human oversight.
8. Ensure administrative changes are recorded and auditable.

### 5.11.6 Human Oversight Principle

Automated systems provide analysis and recommendations, but the Super Admin retains the ability to review and correct decisions when necessary.

This creates a human-supervised security architecture rather than a system that relies entirely on automated decisions.

---

## 5.12 Complete Centralized Security Decision Workflow

The following diagram represents the complete architecture.

```text
                       USER REQUEST
                            |
                            v
              CENTRALIZED SECURITY MIDDLEWARE
                            |
                            v
                       userhistory
                            |
                            v
                  5.8 POLICE SYSTEM
                    WRONGING SYSTEM
                            |
                            v
                   EVENT INVESTIGATION
                            |
                            v
                   WRONGING LEVEL 0–10
                            |
                            v
                5.9 GOVERNMENT SYSTEM
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
           PARTY A        PARTY B       PARTY C
           (BJP)         (Congress)   (Probability)
              |             |             |
              v             v             v
           MEMBERS        MEMBERS       MEMBERS
              |             |             |
              v             v             v
         INDIVIDUAL YES / NO VOTES
              |             |             |
              +-------------+-------------+
                            |
                            v
                  COUNT ALL MEMBER VOTES
                            |
                            v
                     OVERALL MAJORITY
                            |
                            v
                  GOVERNMENT DECISION
                            |
                            v
                5.10 SUPREME COURT SYSTEM
                            |
                            v
                   USER CLASSIFICATION
                            |
               +------------+------------+
               |            |            |
               v            v            v
           WHITELIST     GRAYLIST    BLACKLIST
               |            |            |
               +------------+------------+
                            |
                            v
                  5.11 PRESIDENT SYSTEM
                     SUPER ADMIN
                            |
                            v
                   HUMAN REVIEW
                            |
                            v
                AUTHORIZED MODIFICATION
                    WHEN REQUIRED
```

### Architecture Summary

| Section | Authority | Main responsibility |
|---|---|---|
| 5.8 | Police | Investigate events and assign Wronging severity |
| 5.9 | Government | Organize parties and members, collect individual votes, and determine the overall majority |
| 5.10 | Supreme Court | Apply user classifications and access restrictions |
| 5.11 | President | Human oversight, review, and authorized classification changes |

### Important Architectural Principles

1. Every decision should be traceable to its original event and supporting evidence.
2. Each Government member votes individually; parties do not cast collective votes.
3. The Government's overall decision is determined by the majority of participating members across all parties.
4. Model predictions must be distinguished from actual recorded event values.
5. A Wronging score or model vote alone does not establish malicious intent.
6. Serious restrictions should support human review and an appropriate correction or appeal process.
7. The President is a real human Super Admin, not an automated decision-making member.
8. Every classification and administrative modification should maintain an audit history.
   


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


