# Frontend Coding Standards

**Purpose:** Optional guidance for component structure, state management, accessibility, and testing. Use these checklists as needed.

**Reference:** Always reference `./confer-agent.profile.yml` for frontend framework, UI library. Never hard-code infrastructure values.

---

## Component Structure

### Checklist
- ☐ Use functional components with hooks (React) or composition (Vue)
- ☐ Keep components small and focused (< 200 lines)
- ☐ Extract reusable logic into custom hooks/composables
- ☐ Use TypeScript/PropTypes for component props
- ☐ Organize files: `ComponentName.tsx`, `ComponentName.test.tsx`, `ComponentName.styles.ts`

### Examples
```typescript
// Good: Small, focused component
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {label}
    </button>
  );
}

// Bad: Monolithic component
export function Dashboard() {
  // 500+ lines of mixed concerns
}
```

---

## State Management

### Checklist
- ☐ Use local state for component-specific data
- ☐ Use context for shared state (theme, user)
- ☐ Use global state management (Redux, Zustand) for complex app state
- ☐ Avoid prop drilling (use context or state management)
- ☐ Cache API responses when appropriate

### Examples
```typescript
// Good: Appropriate state management
// Local state for form
const [email, setEmail] = useState('');

// Context for theme
const { theme, toggleTheme } = useTheme();

// Global store for user data
const user = useUserStore(state => state.user);

// Bad: Everything in global state
const email = useStore(state => state.email);  // Should be local
```

---

## Accessibility

### Checklist
- ☐ Use semantic HTML (`<button>`, `<nav>`, `<main>`)
- ☐ Add ARIA labels for screen readers
- ☐ Ensure keyboard navigation works (Tab, Enter, Escape)
- ☐ Maintain focus indicators
- ☐ Test with screen reader (VoiceOver, NVDA)
- ☐ Ensure color contrast meets WCAG AA (4.5:1)

### Examples
```typescript
// Good: Accessible component
<button
  aria-label="Close dialog"
  onClick={handleClose}
  className="close-btn"
>
  <span aria-hidden="true">×</span>
</button>

// Bad: Inaccessible
<div onClick={handleClose}>×</div>  // Not keyboard accessible
```

---

## Testing

### Checklist
- ☐ Write unit tests for components (React Testing Library, Vue Test Utils)
- ☐ Test user interactions (clicks, inputs, form submissions)
- ☐ Test error states and edge cases
- ☐ Use E2E tests for critical user flows (Playwright, Cypress)
- ☐ Keep test files close to components (`Component.test.tsx`)

### Examples
```typescript
// Good: Component test
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  render(<Button label="Click me" onClick={handleClick} />);
  
  fireEvent.click(screen.getByText('Click me'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

// Good: Accessibility test
test('button is keyboard accessible', () => {
  const { container } = render(<Button label="Click" onClick={() => {}} />);
  const button = container.querySelector('button');
  expect(button).toHaveAttribute('tabindex', '0');
});
```

---

## API Integration

### Checklist
- ☐ Use hooks/composables for API calls (`useQuery`, `useSWR`)
- ☐ Handle loading and error states
- ☐ Show user-friendly error messages
- ☐ Implement retry logic for failed requests
- ☐ Cache responses appropriately

### Examples
```typescript
// Good: API hook with error handling
function useUser(id: string) {
  const { data, error, isLoading } = useSWR(`/api/users/${id}`, fetcher);
  
  return {
    user: data,
    isLoading,
    error: error ? 'Failed to load user' : null
  };
}

// Usage in component
const { user, isLoading, error } = useUser(userId);
if (isLoading) return <Spinner />;
if (error) return <ErrorMessage message={error} />;
return <UserProfile user={user} />;
```

---

## Performance

### Checklist
- ☐ Use `React.memo` or `useMemo` for expensive computations
- ☐ Lazy load heavy components (`React.lazy`, dynamic imports)
- ☐ Optimize images (WebP, lazy loading, proper sizing)
- ☐ Minimize re-renders (avoid inline functions in JSX)
- ☐ Use code splitting for routes

### Examples
```typescript
// Good: Memoized component
const ExpensiveComponent = React.memo(({ data }) => {
  const processed = useMemo(() => {
    return processLargeDataset(data);
  }, [data]);
  return <div>{processed}</div>;
});

// Good: Lazy loading
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

---

## Profile Usage

**Reference:** `./confer-agent.profile.yml` for:
- Frontend framework: `{{FRAMEWORKS}}`
- UI library: (check profile or project structure)
- Environment: `{{ENV}}`
- HTTP port: `{{HTTP_PORT}}` (for API calls)

**Never:** Hard-code framework versions, API endpoints, or environment values.

---

## File Organization

**Recommendation:**
```
src/
├── components/       # Reusable components
├── hooks/           # Custom hooks
├── pages/            # Page components
├── lib/             # Utilities, API clients
└── styles/          # Global styles
```

**Adapt to your framework's conventions (Next.js, Remix, Vue, etc.)**

