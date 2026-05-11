# React Reference (Hooks, TypeScript, React Query)

## Component patterns

### Functional component with typed props

```typescript
// src/components/UserCard/UserCard.tsx
interface UserCardProps {
    user: User;
    onEdit?: (id: string) => void;
    className?: string;
}

export function UserCard({ user, onEdit, className }: UserCardProps) {
    return (
        <article className={cn('user-card', className)} aria-label={`User: ${user.name}`}>
            <h2 className="user-card__name">{user.name}</h2>
            <p className="user-card__email">{user.email}</p>
            {onEdit && (
                <button
                    type="button"
                    onClick={() => onEdit(user.id)}
                    aria-label={`Edit ${user.name}`}
                >
                    Edit
                </button>
            )}
        </article>
    );
}
```

### Custom hook for data fetching (React Query)

```typescript
// src/hooks/useUser.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUser(userId: string) {
    return useQuery({
        queryKey: ['users', userId],
        queryFn: () => api.getUser(userId),
        enabled: !!userId,
        staleTime: 5 * 60 * 1000, // 5 minutes
    });
}

export function useUpdateUser() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (data: UpdateUserInput) => api.updateUser(data),
        onSuccess: (updatedUser) => {
            queryClient.setQueryData(['users', updatedUser.id], updatedUser);
            queryClient.invalidateQueries({ queryKey: ['users'] });
        },
    });
}
```

### Page component pattern

```typescript
// src/pages/UserPage.tsx
export function UserPage() {
    const { userId } = useParams<{ userId: string }>();
    const { data: user, isLoading, error } = useUser(userId!);

    if (isLoading) return <UserCardSkeleton />;
    if (error) return <ErrorBoundaryFallback error={error} />;
    if (!user) return <EmptyState message="User not found" />;

    return (
        <main>
            <h1>{user.name}</h1>
            <UserCard user={user} />
        </main>
    );
}
```

## State management

### Local state: useState + useReducer

```typescript
// Simple state
const [isOpen, setIsOpen] = useState(false);

// Complex state — prefer useReducer
type Action =
    | { type: 'SET_LOADING'; payload: boolean }
    | { type: 'SET_ERROR'; payload: string | null }
    | { type: 'SET_DATA'; payload: User[] };

function reducer(state: State, action: Action): State {
    switch (action.type) {
        case 'SET_LOADING': return { ...state, loading: action.payload };
        case 'SET_ERROR': return { ...state, error: action.payload };
        case 'SET_DATA': return { ...state, data: action.payload, loading: false };
    }
}
```

### Global state: Zustand (lightweight)

```typescript
// src/store/auth.store.ts
import { create } from 'zustand';

interface AuthStore {
    user: User | null;
    token: string | null;
    login: (user: User, token: string) => void;
    logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
    user: null,
    token: null,
    login: (user, token) => set({ user, token }),
    logout: () => set({ user: null, token: null }),
}));
```

## Forms (React Hook Form + Zod)

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const LoginSchema = z.object({
    email: z.string().email('Invalid email'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
});
type LoginForm = z.infer<typeof LoginSchema>;

export function LoginForm({ onSubmit }: { onSubmit: (data: LoginForm) => Promise<void> }) {
    const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginForm>({
        resolver: zodResolver(LoginSchema),
    });

    return (
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
            <label htmlFor="email">Email</label>
            <input
                id="email"
                type="email"
                aria-describedby={errors.email ? 'email-error' : undefined}
                {...register('email')}
            />
            {errors.email && (
                <span id="email-error" role="alert">{errors.email.message}</span>
            )}
            <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Signing in…' : 'Sign in'}
            </button>
        </form>
    );
}
```

## Performance patterns

```typescript
// Memoize expensive renders
const MemoizedList = memo(({ items }: { items: Item[] }) => (
    <ul>{items.map(item => <li key={item.id}>{item.name}</li>)}</ul>
));

// Memoize calculations
const sortedItems = useMemo(
    () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
    [items]
);

// Stable callbacks for child props
const handleDelete = useCallback((id: string) => {
    deleteItem(id);
}, [deleteItem]);

// Lazy-load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
// Usage: <Suspense fallback={<Skeleton />}><HeavyChart /></Suspense>
```

## Testing (Vitest + Testing Library)

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';

function renderWithProviders(ui: React.ReactElement) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>);
}

describe('LoginForm', () => {
    it('shows validation error for invalid email', async () => {
        const user = userEvent.setup();
        renderWithProviders(<LoginForm onSubmit={vi.fn()} />);

        await user.type(screen.getByLabelText('Email'), 'not-an-email');
        await user.click(screen.getByRole('button', { name: 'Sign in' }));

        expect(screen.getByRole('alert')).toHaveTextContent('Invalid email');
    });
});
```

## Key packages

- Data fetching: `@tanstack/react-query`
- Forms: `react-hook-form` + `@hookform/resolvers` + `zod`
- Global state: `zustand` (lightweight) or `jotai` (atomic)
- Routing: `react-router-dom` v6
- Styling: CSS Modules or `clsx`/`cn` utility
- Testing: `vitest` + `@testing-library/react` + `@testing-library/user-event`
