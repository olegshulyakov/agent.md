# Next.js Reference (App Router)

## Project structure (App Router)

```
src/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page (Server Component)
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   └── users/
│       ├── page.tsx            # /users list
│       └── [id]/
│           ├── page.tsx        # /users/[id] detail
│           └── edit/page.tsx
├── components/
│   ├── ui/                     # Shared UI primitives
│   └── users/                  # Feature components
├── lib/
│   ├── api.ts                  # API client / fetch wrappers
│   └── auth.ts                 # Auth helpers
└── types/
    └── index.ts
```

## Server Components (default)

```typescript
// app/users/page.tsx
// No 'use client' — this is a Server Component
import { UserList } from '@/components/users/UserList';
import { getUsers } from '@/lib/api';

export const metadata = {
    title: 'Users',
    description: 'Manage your team members',
};

export default async function UsersPage() {
    // Fetch directly — no useEffect, no loading state needed
    const users = await getUsers();

    return (
        <main>
            <h1>Users</h1>
            <UserList users={users} />
        </main>
    );
}
```

## Client Components (interactivity only)

```typescript
'use client';
// Only add 'use client' when you need: useState, useEffect, event handlers, browser APIs

import { useState } from 'react';

export function DeleteButton({ userId }: { userId: string }) {
    const [isPending, setIsPending] = useState(false);

    async function handleDelete() {
        setIsPending(true);
        await deleteUser(userId);
        setIsPending(false);
    }

    return (
        <button onClick={handleDelete} disabled={isPending} aria-busy={isPending}>
            {isPending ? 'Deleting…' : 'Delete'}
        </button>
    );
}
```

## Server Actions

```typescript
// app/users/actions.ts
'use server';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const CreateUserSchema = z.object({
    email: z.string().email(),
    name: z.string().min(1),
});

export async function createUser(formData: FormData) {
    const parsed = CreateUserSchema.safeParse({
        email: formData.get('email'),
        name: formData.get('name'),
    });

    if (!parsed.success) {
        return { error: parsed.error.flatten() };
    }

    await db.users.create({ data: parsed.data });
    revalidatePath('/users');
    redirect('/users');
}
```

## Data fetching patterns

```typescript
// Parallel fetching (don't await sequentially)
const [user, posts] = await Promise.all([
    getUser(userId),
    getUserPosts(userId),
]);

// With error handling
async function getUser(id: string) {
    const res = await fetch(`/api/users/${id}`, {
        next: { revalidate: 60 }, // ISR: revalidate every 60 seconds
        // or: { cache: 'no-store' } for dynamic data
        // or: { cache: 'force-cache' } for static data
    });
    if (!res.ok) notFound(); // or throw new Error(...)
    return res.json() as Promise<User>;
}
```

## Route handlers (API routes)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const page = Number(searchParams.get('page') ?? '1');

    const users = await db.users.findMany({
        skip: (page - 1) * 20,
        take: 20,
    });

    return NextResponse.json({ users, page });
}

export async function POST(request: NextRequest) {
    const body = await request.json();
    const parsed = CreateUserSchema.safeParse(body);
    if (!parsed.success) {
        return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }
    const user = await db.users.create({ data: parsed.data });
    return NextResponse.json(user, { status: 201 });
}
```

## Image optimization

```typescript
import Image from 'next/image';

<Image
    src={user.avatarUrl}
    alt={`${user.name}'s avatar`}
    width={48}
    height={48}
    className="rounded-full"
    priority={isAboveFold}
/>
```

## Key Next.js-specific imports

- `next/navigation`: `useRouter`, `usePathname`, `useSearchParams`, `redirect`, `notFound`
- `next/cache`: `revalidatePath`, `revalidateTag`
- `next/image`: optimized `Image`
- `next/link`: client-side `Link`
- `next/font`: font optimization
