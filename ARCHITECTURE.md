# Architecture Overview

## System Architecture

This document provides a visual overview of the Maypo system architecture and its components.

```mermaid
graph LR
  %% Clients
  subgraph Client["Client Layer"]
    WEB["Web Browser\n(HTTPS)"]
    MOBILE["Mobile App\n(HTTPS)"]
  end

  %% API
  subgraph API["API Layer"]
    GATEWAY["API Gateway\n(Rate limiting, routing)"]
    AUTH["Authentication Service\n(OAuth / JWT)"]
  end

  %% Services
  subgraph Services["Business Logic Layer"]
    USER["User Service\n(REST / gRPC)"]
    CONTENT["Content Service\n(REST / gRPC)"]
    PROCESS["Processing Service\n(Workers / Jobs)"]
  end

  %% Data & Cache
  subgraph Data["Data & Cache"]
    DB[(Database)]
    CACHE["Cache (Redis)"]
  end

  %% Async & External
  subgraph External["Async & External"]
    QUEUE[[Message Queue]]
    STORAGE["Cloud Storage (S3)"]
    EXTSVC["Third‑party APIs"]
  end

  %% Infra / Observability
  subgraph Infra["Infra & Ops"]
    MON["Observability\n(Tracing / Logs / Metrics)"]
    CD["CI/CD"]
    ASG["Autoscaling\n(K8s / HPA)"]
  end

  %% Client -> API
  WEB -->|HTTPS| GATEWAY
  MOBILE -->|HTTPS| GATEWAY

  %% Gateway routing & auth
  GATEWAY -->|auth request| AUTH
  GATEWAY -->|route| USER
  GATEWAY -->|route| CONTENT
  GATEWAY -->|route| PROCESS

  %% Services -> Data
  USER -->|read / write| DB
  CONTENT -->|read / write| DB
  PROCESS -->|read / write| DB

  USER -->|cache read / write| CACHE
  CONTENT -->|cache read / write| CACHE

  %% Async flows (explicit)
  PROCESS -->|enqueue (async)| QUEUE
  QUEUE -->>|worker pull| PROCESS
  PROCESS -->|store media| STORAGE
  PROCESS -->|call| EXTSVC

  %% Observability & infra links
  GATEWAY --> MON
  USER --> MON
  CONTENT --> MON
  PROCESS --> MON
  DB --> MON
  QUEUE --> MON

  GATEWAY --> ASG
  PROCESS --> ASG

  CD --> GATEWAY
  CD --> USER
  CD --> CONTENT
  CD --> PROCESS

  %% Visual styles
  classDef client fill:#e1f5ff,stroke:#036,stroke-width:1px;
  classDef api fill:#fff3e0,stroke:#d97706,stroke-width:1px;
  classDef services fill:#f3e5f5,stroke:#6b21a8,stroke-width:1px;
  classDef data fill:#e8f5e9,stroke:#166534,stroke-width:1px;
  classDef external fill:#fce4ec,stroke:#be123c,stroke-width:1px;
  classDef infra fill:#eef2ff,stroke:#2563eb,stroke-width:1px;

  class WEB,MOBILE client;
  class GATEWAY,AUTH api;
  class USER,CONTENT,PROCESS services;
  class DB,CACHE data;
  class QUEUE,STORAGE,EXTSVC external;
  class MON,CD,ASG infra;
```

## Component Descriptions

### Client Layer
- **Web Browser**: Main web application interface
- **Mobile App**: Native mobile application

### API Layer
- **API Gateway**: Central entry point for all client requests, handles routing and request distribution
- **Authentication Service**: Manages user authentication and authorization

### Business Logic Layer
- **User Service**: Handles user management and profiles
- **Content Service**: Manages content creation and delivery
- **Processing Service**: Handles business logic and background processing

### Data Layer
- **Database**: Primary data store for persistent data
- **Cache Layer**: Redis or similar for performance optimization

### External Services
- **Cloud Storage**: File storage and media management
- **Message Queue**: Asynchronous task processing and communication

## Data Flow

1. Clients send requests through the API Gateway
2. Gateway routes requests to appropriate services
3. Services authenticate via the Authentication Service
4. Services process requests and interact with the database and cache
5. Long-running tasks are queued for asynchronous processing
6. Results are cached for improved performance

## Deployment

- Services are deployed as containerized microservices
- API Gateway serves as the single entry point
- Database and cache are managed separately
- External services are integrated via APIs
