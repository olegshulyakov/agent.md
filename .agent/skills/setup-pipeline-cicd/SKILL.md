---
name: setup-pipeline-cicd
description: >
  Generates CI/CD pipeline configuration files for GitHub Actions, GitLab CI, CircleCI, or similar platforms
  covering build, test, lint, security scan, and deployment stages. Use this skill whenever the user wants
  to set up a CI/CD pipeline, automate deployments, create a GitHub Actions workflow, configure GitLab CI,
  add automated testing to a repo, or asks to "set up CI/CD", "create a GitHub Actions workflow", "automate
  this deployment", "add a pipeline", "configure CI for this project", or "set up automated testing and
  deployment". Also trigger for "add linting to CI", "automate Docker builds", "set up deployment automation",
  and "create a release pipeline".
---

# setup-pipeline-cicd

Generate **CI/CD pipeline configuration** that builds, tests, and deploys the application reliably.

## Platform detection

Identify the CI/CD platform:
1. **Explicit mention**: "GitHub Actions", "GitLab CI", "CircleCI", "Jenkins", "Azure DevOps"
2. **Existing files**: `.github/workflows/` → GitHub Actions, `.gitlab-ci.yml` → GitLab CI
3. **Repository host**: GitHub → GitHub Actions (default), GitLab → GitLab CI

## Pipeline structure

A well-designed CI/CD pipeline has these stages in order:

```
Trigger → [Lint/Format] → [Test] → [Build] → [Security Scan] → [Deploy to Staging] → [Deploy to Prod]
```

- **Lint/Format**: Fast feedback (< 2 min). Gate on style before running tests.
- **Test**: Unit + integration tests. Cache dependencies.
- **Build**: Docker image or artifact. Only if tests pass.
- **Security scan**: SAST, dependency vulnerability scan. Don't block prod for warnings.
- **Deploy staging**: Automatic on main branch.
- **Deploy prod**: Manual approval gate or tag-triggered.

## GitHub Actions output

### Node.js/TypeScript example

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/testdb
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-report
          path: coverage/

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push'
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha
            type=ref,event=branch
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          # Replace with your deployment command
          # e.g., kubectl, helm, aws ecs update-service, fly deploy
          echo "Deploying ${{ needs.build.outputs.image-tag }} to staging"

  deploy-prod:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://app.example.com
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production"
```

### Python example

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - run: pip install -r requirements-dev.txt
      - run: ruff check .
      - run: mypy .
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
```

## GitLab CI output

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

lint:
  stage: lint
  image: node:20-alpine
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths: [node_modules/]
  script:
    - npm ci
    - npm run lint
    - npm run format:check

test:
  stage: test
  image: node:20-alpine
  services:
    - postgres:15
  variables:
    POSTGRES_PASSWORD: testpass
    DATABASE_URL: postgres://postgres:testpass@postgres:5432/testdb
  script:
    - npm ci
    - npm test

build:
  stage: build
  image: docker:24
  services: [docker:24-dind]
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main

deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - echo "Deploy $DOCKER_IMAGE to staging"
  only:
    - main
```

## Best practices to always follow

- **Cache dependencies** between runs (npm, pip, Maven, Go modules)
- **Use secrets** for credentials — never hardcode API keys or passwords
- **Parallelize** independent jobs (lint and test can run in parallel)
- **Pin action versions** to SHA or specific version tag (not `@main`)
- **Add environment protection rules** for production (manual approval)
- **Fail fast** — lint before test, test before build
- **Upload artifacts** on failure for debugging (logs, test reports)
- **Matrix builds** when multiple language versions need to be supported

## Security scan integration

```yaml
# Add to your CI pipeline
security-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        severity: 'CRITICAL,HIGH'
    - name: Dependency audit
      run: npm audit --audit-level=high  # or: pip-audit, safety check
```
