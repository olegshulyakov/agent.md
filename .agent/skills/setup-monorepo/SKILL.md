---
name: setup-monorepo
description: >
  Generates monorepo configuration and tooling setup using Nx, Turborepo, or Bazel, including
  workspace structure, build configuration, package boundaries, and CI integration. Use this skill
  whenever the user wants to set up a monorepo, configure a monorepo build system, migrate to a
  monorepo structure, organize multiple packages in a single repository, or asks to "set up a
  monorepo", "configure Turborepo", "set up Nx workspace", "organize my repos into a monorepo",
  "add caching to my monorepo build", "set up shared packages", "configure workspace dependencies",
  or "create a monorepo structure". Also trigger for "pnpm workspaces", "Yarn workspaces", "npm
  workspaces", "monorepo task pipeline", and "affected tests in monorepo". Distinct from
  setup-pipeline-cicd (which generates the CI/CD workflow files) and setup-developer-portal
  (which creates internal documentation).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# setup-monorepo

Generate a **monorepo configuration** with tooling, workspace structure, package boundaries, and build pipeline.

## Tool selection

Detect the preferred tool from context:

| Tool | Best for | Key features |
|------|----------|-------------|
| **Turborepo** | JavaScript/TypeScript teams; simplest setup | Task pipeline caching; minimal config |
| **Nx** | Larger teams; need code generators and module boundaries | Plugin ecosystem; affected graph; generators |
| **Bazel** | Multi-language (Java + JS + Go + Python); huge scale | Hermetic builds; fine-grained caching |
| **pnpm workspaces** | Simple JS monorepo without build tool overhead | Native workspace linking; no extra tooling |

If unclear, use **Turborepo** for JS/TS projects (simplest, most adopted).

## Workspace structure

```
monorepo-root/
├── apps/                        # Deployable applications
│   ├── web/                     # Next.js / React app
│   ├── api/                     # Backend API
│   └── admin/                   # Admin dashboard
├── packages/                    # Shared packages (published or internal)
│   ├── ui/                      # Shared React component library
│   ├── config/                  # Shared configs (ESLint, TypeScript, etc.)
│   │   ├── eslint/
│   │   ├── typescript/
│   │   └── jest/
│   ├── utils/                   # Shared utilities
│   └── types/                   # Shared TypeScript types
├── package.json                 # Root package.json (workspaces declaration)
├── turbo.json                   # Turborepo config (or nx.json for Nx)
├── pnpm-workspace.yaml          # (if using pnpm)
├── .eslintrc.js                 # Root ESLint config
├── tsconfig.base.json           # Base TypeScript config
└── .gitignore
```

## Turborepo Setup

### Root `package.json`

```json
{
  "name": "myorg-monorepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev --parallel",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "type-check": "turbo run type-check",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.0.0"
  }
}
```

### `turbo.json`

```json
{
  "$schema": "https://turbo.build/schema.json",
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],          // Build dependencies first (topological)
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "outputs": [".next/**", "dist/**", "build/**"]
    },
    "test": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", "jest.config.*"],
      "outputs": ["coverage/**"],
      "cache": true
    },
    "lint": {
      "inputs": ["$TURBO_DEFAULT$", ".eslintrc*", "eslint.config.*"]
    },
    "type-check": {
      "dependsOn": ["^build"]
    },
    "dev": {
      "cache": false,
      "persistent": true              // Long-running dev servers
    },
    "clean": {
      "cache": false
    }
  },
  "remoteCache": {
    "enabled": true                   // Enable Vercel Remote Cache (or self-hosted)
  }
}
```

### pnpm workspace (`pnpm-workspace.yaml`)

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

## Nx Setup

### `nx.json`

```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "cache": true
    },
    "lint": {
      "cache": true
    }
  },
  "namedInputs": {
    "production": [
      "default",
      "!{projectRoot}/**/*.spec.ts",
      "!{projectRoot}/jest.config.ts"
    ]
  },
  "plugins": [
    "@nx/next/plugin",
    "@nx/eslint/plugin"
  ]
}
```

### Module boundary rules (`.eslintrc.js`)

```js
module.exports = {
  // ...
  rules: {
    "@nx/enforce-module-boundaries": [
      "error",
      {
        enforceBuildableLibDependency: true,
        depConstraints: [
          { sourceTag: "type:app",     onlyDependOnLibsWithTags: ["type:lib", "type:ui"] },
          { sourceTag: "type:ui",      onlyDependOnLibsWithTags: ["type:lib"] },
          { sourceTag: "scope:web",    onlyDependOnLibsWithTags: ["scope:web", "scope:shared"] },
          { sourceTag: "scope:api",    onlyDependOnLibsWithTags: ["scope:api", "scope:shared"] },
          { sourceTag: "scope:shared", onlyDependOnLibsWithTags: ["scope:shared"] },
        ],
      },
    ],
  },
};
```

## Shared config packages

### `packages/config/typescript/base.json`

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "display": "Base",
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

### `packages/config/typescript/nextjs.json`

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "display": "Next.js",
  "extends": "./base.json",
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "jsx": "preserve",
    "plugins": [{ "name": "next" }]
  }
}
```

### App `tsconfig.json` (references shared base)

```json
{
  "extends": "@myorg/config/typescript/nextjs.json",
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## Shared UI package (`packages/ui`)

```typescript
// packages/ui/package.json
{
  "name": "@myorg/ui",
  "version": "0.1.0",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "dev": "tsup src/index.ts --format esm,cjs --dts --watch",
    "lint": "eslint src/",
    "type-check": "tsc --noEmit"
  },
  "peerDependencies": { "react": "^18.0.0" },
  "devDependencies": {
    "@myorg/config": "*",
    "tsup": "^8.0.0"
  }
}
```

## CI Integration

### GitHub Actions (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # Needed for Nx affected commands

      - uses: pnpm/action-setup@v3
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      # Turborepo remote cache
      - uses: actions/cache@v4
        with:
          path: .turbo
          key: ${{ runner.os }}-turbo-${{ github.sha }}
          restore-keys: ${{ runner.os }}-turbo-

      # Run only affected packages (for PRs)
      - name: Build affected
        run: pnpm turbo run build --filter="...[origin/main]"
        
      - name: Test affected
        run: pnpm turbo run test --filter="...[origin/main]"

      - name: Lint affected
        run: pnpm turbo run lint --filter="...[origin/main]"
```

## Calibration

- **Nx vs Turborepo decision**: If user needs module boundary enforcement, code generators, or has >50 packages → Nx; otherwise Turborepo
- **Migration from multi-repo**: Show the steps to move existing repos in; how to preserve git history
- **Add remote caching**: Turborepo → Vercel Remote Cache; Nx → Nx Cloud; or self-hosted with S3
- **pnpm only (no build tool)**: Just the workspace config and cross-package dependency setup
