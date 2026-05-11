# Node.js Backend Reference (Express / Fastify)

## Project structure (TypeScript)

```
src/
├── index.ts                  # Entry point
├── routes/
│   └── users.ts              # Route definitions
├── services/
│   └── user.service.ts       # Business logic
├── repositories/
│   └── user.repository.ts    # DB access
├── schemas/
│   └── user.schema.ts        # Zod validation schemas
├── middleware/
│   ├── auth.ts               # JWT validation
│   └── error-handler.ts      # Global error handler
├── types/
│   └── index.ts              # Shared types
└── db/
    └── index.ts              # DB connection (Prisma / Knex / pg)
```

## Fastify (preferred for new projects)

```typescript
// src/routes/users.ts
import { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';
import { UserService } from '../services/user.service';

const CreateUserBody = z.object({
    email: z.string().email(),
    name: z.string().min(1).max(255),
    password: z.string().min(8),
});

export const userRoutes: FastifyPluginAsync = async (fastify) => {
    const userService = new UserService(fastify.db);

    fastify.post('/users', {
        schema: {
            body: CreateUserBody,
        },
    }, async (request, reply) => {
        const user = await userService.create(request.body);
        return reply.status(201).send(user);
    });

    fastify.get('/users/:id', async (request, reply) => {
        const { id } = request.params as { id: string };
        const user = await userService.getById(id);
        if (!user) return reply.status(404).send({ error: 'User not found' });
        return user;
    });
};
```

## Express (established pattern)

```typescript
// src/routes/users.ts
import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { UserService } from '../services/user.service';

const router = Router();

const CreateUserSchema = z.object({
    email: z.string().email(),
    name: z.string().min(1),
    password: z.string().min(8),
});

router.post('/', async (req: Request, res: Response, next: NextFunction) => {
    try {
        const body = CreateUserSchema.parse(req.body);
        const user = await userService.create(body);
        res.status(201).json(user);
    } catch (error) {
        next(error);
    }
});

// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    if (err instanceof z.ZodError) {
        return res.status(400).json({ errors: err.errors });
    }
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
});
```

## Service layer

```typescript
// src/services/user.service.ts
import { hash } from 'bcryptjs';
import { UserRepository } from '../repositories/user.repository';

export class UserService {
    constructor(private readonly repo: UserRepository) {}

    async create(data: CreateUserInput): Promise<UserDTO> {
        const existing = await this.repo.findByEmail(data.email);
        if (existing) {
            throw new ConflictError('Email already registered');
        }
        const passwordHash = await hash(data.password, 12);
        const user = await this.repo.create({ ...data, passwordHash });
        return toUserDTO(user);  // strip sensitive fields
    }
}
```

## Prisma ORM (preferred)

```typescript
// src/repositories/user.repository.ts
import { PrismaClient } from '@prisma/client';

export class UserRepository {
    constructor(private readonly prisma: PrismaClient) {}

    async findById(id: string) {
        return this.prisma.user.findUnique({ where: { id } });
    }

    async findByEmail(email: string) {
        return this.prisma.user.findUnique({ where: { email } });
    }

    async create(data: Prisma.UserCreateInput) {
        return this.prisma.user.create({ data });
    }

    async update(id: string, data: Prisma.UserUpdateInput) {
        return this.prisma.user.update({ where: { id }, data });
    }
}
```

## Authentication middleware (JWT)

```typescript
import jwt from 'jsonwebtoken';

export async function authenticate(req: Request, res: Response, next: NextFunction) {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Authentication required' });

    try {
        const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
        req.user = payload;
        next();
    } catch {
        res.status(401).json({ error: 'Invalid or expired token' });
    }
}
```

## Testing (Vitest + Supertest)

```typescript
import { describe, it, expect, beforeAll } from 'vitest';
import request from 'supertest';
import { app } from '../src/app';

describe('POST /users', () => {
    it('creates a user with valid data', async () => {
        const res = await request(app)
            .post('/users')
            .send({ email: 'test@example.com', name: 'Test', password: 'password123' });

        expect(res.status).toBe(201);
        expect(res.body.email).toBe('test@example.com');
        expect(res.body.password).toBeUndefined();
    });

    it('returns 409 when email already exists', async () => {
        // seed first user...
        const res = await request(app)
            .post('/users')
            .send({ email: 'existing@example.com', name: 'X', password: 'password123' });
        expect(res.status).toBe(409);
    });
});
```

## Key packages

- Runtime: `tsx` or `ts-node` for development; `esbuild` for production build
- Validation: `zod` (prefer over `joi` for TypeScript)
- ORM: `prisma` (prefer) or `drizzle-orm` or `knex`
- Auth: `jsonwebtoken` + `bcryptjs`
- Testing: `vitest` + `supertest`
- Logging: `pino` (structured, fast)
