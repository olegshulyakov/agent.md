---
name: diagram-c4
description: >
  Produces C4 model diagrams (Context, Container, Component, Code levels) as Mermaid or PlantUML markup for
  visualizing software architecture. Use this skill whenever the user wants a C4 diagram, architecture diagram,
  system context diagram, container diagram, component diagram, or asks to "draw the architecture", "make a C4
  diagram", "show me the system diagram", "visualize the components", "create a context diagram", or "diagram
  how this system works". Also trigger when the user wants to document service boundaries, show how microservices
  relate, or produce any structured architecture visualization. Distinct from design-arch (prose document with
  trade-offs) and diagram-dfd (data flow focus).
---

# diagram-c4

Produce **C4 model diagrams** at the appropriate level(s) using Mermaid syntax (default) or PlantUML C4 macros.

## What is C4?

C4 is a hierarchical diagramming model that zooms into a system at four levels:

| Level | Audience | Shows |
|-------|----------|-------|
| **L1 Context** | Everyone | System + external users and systems it interacts with |
| **L2 Container** | Developers | Applications, databases, services inside the system |
| **L3 Component** | Developers | Internal structure of a single container |
| **L4 Code** | Implementers | Classes, functions — rarely needed, auto-generated from code is better |

## What level to produce

- If the user asks for "a C4 diagram" without specifying: produce L1 + L2
- If the user asks for a "component diagram" or mentions a specific service: produce L3 for that service
- If the user asks for "context diagram" or "system context": produce L1
- Produce all levels only when explicitly requested or when the system is well-defined and small

## Information gathering

From context, identify:
- **What system** is being diagrammed?
- **Who are the users** (personas)?
- **What external systems** does it interact with?
- **What are the main containers** (web app, API, database, queue, etc.)?
- **What level** is needed?

Work with what's provided. Infer reasonable containers/components from the tech stack if not specified.

## Output format

Always output:
1. A brief narrative explaining the diagram(s)
2. The Mermaid code block(s) that renders the diagram
3. A legend or notes if the diagram has non-obvious elements

### Mermaid C4 syntax

Use the official Mermaid C4 diagrams (available in Mermaid v10+):

```markdown
# C4 Context Diagram: [System Name]

[Brief description of what this diagram shows]

```mermaid
C4Context
    title System Context — [System Name]

    Person(user, "End User", "A user of the system")
    Person(admin, "Administrator", "Manages system configuration")

    System(mySystem, "[System Name]", "Description of what the system does")

    System_Ext(emailService, "Email Service", "Sends transactional emails (SendGrid)")
    System_Ext(paymentGateway, "Payment Gateway", "Processes payments (Stripe)")

    Rel(user, mySystem, "Uses", "HTTPS")
    Rel(admin, mySystem, "Administers", "HTTPS")
    Rel(mySystem, emailService, "Sends emails via", "REST/HTTPS")
    Rel(mySystem, paymentGateway, "Processes payments via", "REST/HTTPS")
```

# C4 Container Diagram: [System Name]

```mermaid
C4Container
    title Container Diagram — [System Name]

    Person(user, "End User", "Uses the web application")

    System_Boundary(mySystem, "[System Name]") {
        Container(webApp, "Web Application", "React/TypeScript", "Single-page application served via CDN")
        Container(apiServer, "API Server", "Node.js / Express", "REST API handling business logic")
        ContainerDb(database, "Database", "PostgreSQL 15", "Stores user data and application state")
        Container(cache, "Cache", "Redis", "Session storage and query caching")
        Container(queue, "Message Queue", "RabbitMQ", "Async job processing")
    }

    System_Ext(emailSvc, "Email Service", "SendGrid — transactional email delivery")

    Rel(user, webApp, "Uses", "HTTPS")
    Rel(webApp, apiServer, "API calls", "REST/HTTPS")
    Rel(apiServer, database, "Reads/writes", "TCP/5432")
    Rel(apiServer, cache, "Session + cache", "TCP/6379")
    Rel(apiServer, queue, "Publishes jobs", "AMQP")
    Rel(apiServer, emailSvc, "Sends emails", "REST/HTTPS")
```
```

### L3 Component diagram example

```mermaid
C4Component
    title Component Diagram — API Server

    Container_Boundary(api, "API Server") {
        Component(authController, "Auth Controller", "Express Router", "Handles login, logout, refresh")
        Component(userController, "User Controller", "Express Router", "CRUD for user resources")
        Component(authService, "Auth Service", "Service", "JWT creation, validation, refresh logic")
        Component(userService, "User Service", "Service", "User business logic")
        Component(userRepo, "User Repository", "Repository", "Data access layer for users table")
    }

    ContainerDb(db, "Database", "PostgreSQL")
    Container(cache, "Cache", "Redis")

    Rel(authController, authService, "Uses")
    Rel(userController, userService, "Uses")
    Rel(authService, userRepo, "Uses")
    Rel(userService, userRepo, "Uses")
    Rel(userRepo, db, "Queries", "SQL")
    Rel(authService, cache, "Session storage", "Redis commands")
```

## Diagram quality checklist

Before finalizing each diagram:
- [ ] Every element has a name, technology/type, and description
- [ ] Relationships have labels describing what is communicated and with what protocol
- [ ] The boundary of the system is clear (what's inside vs outside)
- [ ] No more than 7±2 elements at any level (split into multiple diagrams if needed)
- [ ] External systems are clearly distinguished from internal containers
- [ ] Data flows are directed (arrows show who calls whom)

## Alternative: PlantUML C4

If the user prefers PlantUML, use the C4-PlantUML macros:

```plantuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(user, "End User", "Uses the system")
System(mySystem, "My System", "Does important things")
System_Ext(ext, "External System", "Third-party dependency")

Rel(user, mySystem, "Uses")
Rel(mySystem, ext, "Calls")
```

## Calibration

- **Simple system description**: Generate L1 + L2
- **Explicit "component diagram"**: Generate L3 for named service
- **Large system**: Split into multiple L2 diagrams grouped by domain
- **Existing codebase context**: Infer containers from file structure, frameworks, and imports visible in context
