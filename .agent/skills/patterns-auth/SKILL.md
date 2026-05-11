---
name: patterns-auth
description: >
  Produces an auth pattern catalogue with implementation examples for JWT, OAuth2, sessions, API keys, RBAC,
  and related authentication/authorization patterns. Use this skill whenever the user wants to implement
  authentication or authorization, choose between auth strategies, add login/logout to an app, implement
  OAuth2 or JWT, add API key auth, set up RBAC or permission systems, or asks "how should I implement auth",
  "should I use JWT or sessions", "implement OAuth2 login", "add role-based access control", "how do I
  authenticate API requests", or "secure my endpoints". Also trigger for refresh token patterns, SSO setup,
  and MFA implementation guidance.
---

# patterns-auth

Produce **auth implementation guidance** selecting the right pattern for the context with working code examples.

## Pattern Selection Guide

Help the user pick the right auth pattern first, then implement it:

| Pattern | Best for | Avoid when |
|---------|----------|------------|
| **JWT (stateless)** | APIs, microservices, mobile backends | Long-lived sessions needed, immediate revocation required |
| **Session cookies** | Traditional web apps, server-rendered UIs | Distributed systems without shared session store |
| **OAuth2 / OIDC** | Third-party login (Google/GitHub), delegating access | Internal-only apps with no third-party integration needed |
| **API keys** | Server-to-server, developer APIs, CI/CD | End-user auth, short-lived tokens needed |
| **RBAC** | Multi-role apps where different users have different capabilities | Simple single-role systems |
| **Refresh token rotation** | Mobile apps, SPAs that need long sessions without storing credentials | Short-lived single-session use |

## Information gathering

From context, identify:
- **App type**: Web, API, mobile, SPA, server-rendered?
- **Users**: Human end-users, machines/services, third-party developers?
- **Session duration**: Short (API calls), medium (web session), long (mobile)?
- **Revocation needs**: Must tokens be immediately invalidatable?
- **Multi-tenancy / RBAC**: Are there different user roles?
- **Framework**: Express, FastAPI, Django, Spring, etc.?

## Output format

For each auth pattern requested, produce:
1. **When to use** (brief justification)
2. **Implementation** (complete, runnable code for the detected framework)
3. **Security notes** (what to watch out for)
4. **Testing checklist** (what to verify works correctly)

---

## JWT Pattern

### Implementation (Node.js/Express example)

```typescript
// middleware/auth.ts
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

const JWT_SECRET = process.env.JWT_SECRET!; // never hardcode
const JWT_EXPIRY = '15m'; // keep access tokens short-lived

export function generateTokens(userId: string, role: string) {
  const accessToken = jwt.sign(
    { sub: userId, role, type: 'access' },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRY, algorithm: 'HS256' }
  );
  const refreshToken = jwt.sign(
    { sub: userId, type: 'refresh' },
    JWT_SECRET,
    { expiresIn: '7d', algorithm: 'HS256' }
  );
  return { accessToken, refreshToken };
}

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid Authorization header' });
  }

  try {
    const token = authHeader.slice(7);
    const payload = jwt.verify(token, JWT_SECRET, { algorithms: ['HS256'] });
    req.user = payload as { sub: string; role: string };
    next();
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### Security notes
- Use `jwt.verify()` never `jwt.decode()` — decode skips signature validation
- Always specify `algorithms` to prevent the `alg:none` attack
- Keep access tokens short-lived (15m); use refresh tokens for longevity
- Store refresh tokens server-side to enable revocation
- Never put sensitive data in JWT payload (it's base64, not encrypted)

---

## Session Pattern

### Implementation (Express + express-session + Redis)

```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production', // HTTPS only in prod
    httpOnly: true,   // prevents JS access (XSS protection)
    sameSite: 'lax',  // CSRF protection
    maxAge: 24 * 60 * 60 * 1000 // 24h
  }
}));

// Login
app.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await validateCredentials(email, password);
  if (!user) return res.status(401).json({ error: 'Invalid credentials' });
  
  req.session.regenerate((err) => { // prevent session fixation
    if (err) return res.status(500).json({ error: 'Session error' });
    req.session.userId = user.id;
    req.session.role = user.role;
    res.json({ message: 'Logged in' });
  });
});

// Logout
app.post('/auth/logout', (req, res) => {
  req.session.destroy(() => {
    res.clearCookie('connect.sid');
    res.json({ message: 'Logged out' });
  });
});
```

---

## OAuth2 / OIDC Pattern

```typescript
// Using passport.js with Google OAuth2
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  callbackURL: '/auth/google/callback'
}, async (accessToken, refreshToken, profile, done) => {
  const user = await upsertUser({
    googleId: profile.id,
    email: profile.emails?.[0].value,
    name: profile.displayName
  });
  return done(null, user);
}));

app.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));
app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => res.redirect('/dashboard')
);
```

---

## API Key Pattern

```typescript
// Secure API key generation and validation
import crypto from 'crypto';

export function generateApiKey(): { raw: string; hash: string } {
  const raw = `key_${crypto.randomBytes(32).toString('hex')}`;
  const hash = crypto.createHash('sha256').update(raw).digest('hex');
  return { raw, hash }; // store hash, return raw once to user
}

export async function apiKeyMiddleware(req: Request, res: Response, next: NextFunction) {
  const apiKey = req.headers['x-api-key'] as string;
  if (!apiKey) return res.status(401).json({ error: 'API key required' });

  const hash = crypto.createHash('sha256').update(apiKey).digest('hex');
  const keyRecord = await db.apiKeys.findByHash(hash); // constant-time comparison via DB lookup
  
  if (!keyRecord || keyRecord.revokedAt) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  
  await db.apiKeys.updateLastUsed(keyRecord.id);
  req.apiKey = keyRecord;
  next();
}
```

---

## RBAC Pattern

```typescript
// Role-based access control middleware
type Role = 'admin' | 'editor' | 'viewer';
type Permission = 'read' | 'write' | 'delete' | 'manage_users';

const ROLE_PERMISSIONS: Record<Role, Permission[]> = {
  admin: ['read', 'write', 'delete', 'manage_users'],
  editor: ['read', 'write'],
  viewer: ['read']
};

export function requirePermission(permission: Permission) {
  return (req: Request, res: Response, next: NextFunction) => {
    const role = req.user?.role as Role;
    if (!role || !ROLE_PERMISSIONS[role]?.includes(permission)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

// Usage
app.delete('/posts/:id', authMiddleware, requirePermission('delete'), deletePost);
```

## Testing checklist

- [ ] Valid credentials → 200 + token/session created
- [ ] Invalid credentials → 401 (same message for wrong email vs wrong password — no enumeration)
- [ ] Expired token → 401 with `token expired` message
- [ ] Missing auth header → 401
- [ ] Valid token for wrong role → 403
- [ ] Logout invalidates session/token
- [ ] Account lockout after N failed attempts
- [ ] Password reset tokens expire and are single-use
