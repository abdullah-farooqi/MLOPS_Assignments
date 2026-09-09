# student-ml-api

A production-ready FastAPI ML inference service demonstrating a professional
MLOps workflow with automated CI/CD, Docker containerisation, semantic
versioning, and container registry publishing.

---

## Repository Structure

```text
student-ml-api/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── VERSION
├── pytest.ini
├── scripts/
│   └── bump_version.py
├── tests/
│   └── test_app.py
└── .github/
    └── workflows/
        ├── ci.yml
        ├── release.yml
        └── bump-version.yml
```

---

## API Endpoints

| Method | Endpoint  | Description          |
|--------|-----------|----------------------|
| GET    | /health   | Health and version   |
| POST   | /predict  | ML prediction        |

### GET /health — v1.1.0 response

```json
{
  "status": "healthy",
  "application": "student-ml-api",
  "application_version": "1.1.0",
  "model_version": "model-1"
}
```

### POST /predict

```json
{ "input": 10 }
```

Response:

```json
{ "input": 10, "prediction": 20 }
```

---

## Git Workflow

Development never occurs directly on `main`.
All changes go through feature branches and Pull Requests.

```text
Feature Branch
      ↓
Commits
      ↓
Push
      ↓
Pull Request
      ↓
GitHub Actions CI
      ↓
Merge into main
      ↓
Git Tag
      ↓
Release Workflow
      ↓
Docker Hub
```

---

## Main Branch Protection

The `main` branch is protected with the following settings:

- Pull Request required before merging
- Status checks required: `Run Tests`, `Validate Docker Build`
- Branch must be up to date before merging
- Direct pushes to `main` are prevented
- Force pushes are prevented
- Branch deletion is prevented

---

## Merge Strategy

**Squash and Merge** was selected for both Pull Requests.

This keeps the `main` branch history clean by combining feature branch
commits into one logical commit per feature. The full development history,
including the deliberate CI failure and fix, remains visible inside each
Pull Request for traceability.

---

## CI Workflow

Triggers on Pull Requests targeting `main`.

Jobs:
- Install dependencies
- Run pytest (4 tests)
- Validate Docker build

The CI workflow does **not** publish images. Publishing only happens
via the release workflow triggered by a version tag.

### Why not publish from every PR?

Publishing a Docker image on every PR would:
- Flood the registry with unversioned, unreviewed images
- Make it impossible to identify which image is production-ready
- Risk publishing broken or incomplete features
- Consume registry storage unnecessarily

Only tagged releases represent approved, production-ready artifacts.

---

## Release Workflow

Triggers on semantic version tags: `v*.*.*`

Pipeline:
```text
Git Tag v1.x.x
      ↓
Checkout
      ↓
Install Dependencies
      ↓
Run pytest
      ↓
Extract version from tag (v1.1.0 → 1.1.0)
      ↓
Docker Hub Login
      ↓
Build Image with OCI metadata
      ↓
Push Tags:
  ├── student-ml-api:1.1.0
  ├── student-ml-api:latest
  └── student-ml-api:<commit-sha>
```

The version is derived automatically from the Git tag using:

```bash
VERSION=${GITHUB_REF_NAME#v}
```

It is never hard-coded inside the workflow.

---

## Semantic Versioning

Versions are managed via `VERSION` file and `scripts/bump_version.py`.

```bash
# Local bump
python scripts/bump_version.py patch   # 1.1.0 → 1.1.1
python scripts/bump_version.py minor   # 1.1.0 → 1.2.0
python scripts/bump_version.py major   # 1.1.0 → 2.0.0
```

Also available as a manual GitHub Actions workflow:
**Actions → Bump Version → Run workflow → select bump type**

---

## Docker Image Metadata (OCI Labels)

Each image contains build-time metadata:

```bash
docker inspect abdullahahmadfarooqi/student-ml-api:1.1.0 \
  --format '{{json .Config.Labels}}'
```

Labels include:
- `org.opencontainers.image.version`
- `org.opencontainers.image.revision` (Git commit SHA)
- `org.opencontainers.image.created` (build date)
- `org.opencontainers.image.source` (repository URL)

---

## Docker Layer Cache

Dockerfile layer order is optimised for CI performance:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt   # cached unless requirements change
COPY app.py .                         # only invalidates here on app changes
```

Compared to:

```dockerfile
COPY . .
RUN pip install -r requirements.txt   # always rebuilds — any file change invalidates
```

Modifying only `app.py` reuses the `pip install` layer.
Modifying `requirements.txt` correctly invalidates it and reinstalls.

---

## Registry

Docker Hub: `abdullahahmadfarooqi/student-ml-api`

| Tag     | Digest                                                                |
|---------|-----------------------------------------------------------------------|
| 1.0.0   | sha256:091ecd72c057363aecd44e16be4416348e40c4c577002b46cfae700e74d38930 |
| 1.1.0   | sha256:40f0abadb67751a94b3ea2eaf627d0948c55a1c2b8440f3c8db6fc016739114d |
| latest  | sha256:40f0abadb67751a94b3ea2eaf627d0948c55a1c2b8440f3c8db6fc016739114d |

---

## Traceability Chain

### v1.0.0

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| Pull Request | #1                                                                    |
| Merge Commit | b80a1cb                                                               |
| Git Tag      | v1.0.0                                                                |
| Docker Image | abdullahahmadfarooqi/student-ml-api:1.0.0                            |
| Digest       | sha256:091ecd72c057363aecd44e16be4416348e40c4c577002b46cfae700e74d38930 |

### v1.1.0

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| Pull Request | #2                                                                    |
| Merge Commit | 5660b45                                                               |
| Git Tag      | v1.1.0                                                                |
| Docker Image | abdullahahmadfarooqi/student-ml-api:1.1.0                            |
| Digest       | sha256:40f0abadb67751a94b3ea2eaf627d0948c55a1c2b8440f3c8db6fc016739114d |

---

## Rollback Procedure

To rollback from `1.1.0` to `1.0.0` without rebuilding:

```bash
docker rm -f student-ml-api
docker run -d --name student-ml-api -p 5000:5000 \
  abdullahahmadfarooqi/student-ml-api:1.0.0
curl http://localhost:5000/health
```

This is faster and safer than `git clone → pip install → python app.py`
because the artifact is already built, tested, and stored in the registry.

---

## Failure Analysis

### Failure 1 — Failed pytest

| Field       | Detail                                              |
|-------------|-----------------------------------------------------|
| Symptom     | CI failed on PR #1                                  |
| Root Cause  | `assert data["status"] == "wrong"` (deliberate)    |
| Evidence    | Commit `8900cbb` — GitHub Actions Run Tests failed  |
| Correction  | Commit `e5bfc7c` — fixed assertion to `"healthy"`  |

### Failure 2 — Empty Docker Hub username secret

| Field       | Detail                                                      |
|-------------|-------------------------------------------------------------|
| Symptom     | Release workflow produced tag `/student-ml-api:1.0.0`      |
| Root Cause  | `DOCKERHUB_USERNAME` secret was empty in GitHub Actions     |
| Evidence    | Workflow log showed `--tag /student-ml-api:1.0.0`           |
| Correction  | Added correct secret value, re-ran workflow successfully    |

---

## Commit SHA Docker Tag

Each release publishes three tags:

```text
student-ml-api:1.1.0       ← semantic version
student-ml-api:latest      ← convenience pointer
student-ml-api:5660b45     ← exact commit SHA
```

The commit SHA tag allows pinning a deployment to an exact source
code state, independent of mutable tags like `latest`. If `latest`
is updated by a new release, the SHA tag still unambiguously identifies
the previous artifact.
