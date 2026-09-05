# Student ML API — Advanced MLOps Exercise

A production-oriented MLOps workflow for a Flask-based machine learning inference API. This project demonstrates professional software development practices including feature branches, Pull Requests, automated CI, Docker containerization, semantic versioning, GitHub Actions, container registry publishing, artifact traceability, reproducibility, and rollback.

---

## 1. Project Overview

**Student ML API** is a simple prediction service developed to demonstrate an end-to-end MLOps development and deployment workflow.

The API accepts a numeric input and returns a prediction using a simple mathematical operation. The primary objective of this project is not model complexity, but demonstrating how application code can be developed, tested, containerized, versioned, and released using a professional CI/CD workflow.

### Core Workflow

```text
Feature Branch
      ↓
Commit + Push
      ↓
Pull Request
      ↓
GitHub Actions CI
      ↓
Tests + Docker Build Validation
      ↓
Code Review
      ↓
Merge into main
      ↓
Semantic Version Tag
      ↓
Release Workflow
      ↓
Docker Build
      ↓
Container Registry
      ↓
Versioned Docker Image
```

---

# 2. Objectives

This project demonstrates the following MLOps practices:

* Flask API development
* Automated unit testing with pytest
* Git feature-branch development
* Pull Request based development
* Protected `main` branch
* GitHub Actions CI
* Docker containerization
* Docker build validation
* Semantic versioning
* Automated Docker image publishing
* GitHub Container Registry (GHCR)
* Docker image versioning
* Commit-specific image tags
* OCI image metadata
* Artifact traceability
* Reproducible deployments
* Container-based rollback
* CI/CD failure analysis

---

# 3. Technology Stack

| Technology          | Purpose                            |
| ------------------- | ---------------------------------- |
| Python              | Application development            |
| Flask               | REST API framework                 |
| pytest              | Automated testing                  |
| Docker              | Application containerization       |
| Git                 | Source-code version control        |
| GitHub              | Repository and Pull Requests       |
| GitHub Actions      | CI/CD automation                   |
| GHCR                | Docker container registry          |
| Semantic Versioning | Application and release versioning |

---

# 4. Project Structure

```text
student-ml-api/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── VERSION
│
├── tests/
│   └── test_app.py
│
└── .github/
    └── workflows/
        ├── ci.yml
        └── release.yml
```

### Important Files

**app.py**
Contains the Flask application and API endpoints.

**requirements.txt**
Contains the Python dependencies required by the application.

**Dockerfile**
Defines how the application is packaged into a Docker image.

**.dockerignore**
Prevents unnecessary files from being included in the Docker build context.

**VERSION**
Contains the current application version.

**tests/test_app.py**
Contains automated API tests.

**ci.yml**
Runs automated validation for Pull Requests.

**release.yml**
Builds and publishes versioned Docker images when a Git tag is pushed.

---

# 5. API Endpoints

## Health Endpoint

### Request

```http
GET /health
```

### Response

```json
{
  "status": "healthy",
  "application": "student-ml-api",
  "version": "1.0.0"
}
```

The endpoint is used to verify that the application is running correctly and to expose the application version.

---

## Prediction Endpoint

### Request

```http
POST /predict
```

### Input

```json
{
  "value": 10
}
```

### Response

```json
{
  "input": 10,
  "prediction": 20
}
```

The prediction logic used for this exercise is intentionally simple:

```text
prediction = input × 2
```

The purpose is to demonstrate the MLOps lifecycle rather than machine-learning model performance.

---

# 6. Automated Testing

The project uses **pytest** for automated testing.

The test suite covers:

1. Health endpoint
2. Successful prediction
3. Missing input
4. Invalid input

Tests are executed using:

```bash
pytest
```

or:

```bash
python -m pytest
```

A successful test execution should report all tests passing.

Example:

```text
4 passed
```

---

# 7. Git Development Workflow

Direct development on `main` is not permitted.

Development is performed using feature branches.

Example:

```bash
git checkout -b feature/prediction-api
```

Changes are committed using meaningful commit messages.

Examples:

```bash
git commit -m "feat: add prediction endpoint"
```

```bash
git commit -m "test: add API unit tests"
```

The feature branch is then pushed:

```bash
git push origin feature/prediction-api
```

A Pull Request is created:

```text
feature/prediction-api
        ↓
       main
```

---

# 8. Pull Request Workflow

Pull Requests are used to review and validate changes before they enter `main`.

Each Pull Request should contain:

### Summary

A brief explanation of what was implemented.

### Changes

A list of important modifications.

### Testing Performed

Information about tests executed locally and by CI.

### Docker Impact

Information about Dockerfile or container changes.

### Checklist

```text
[ ] Application runs locally
[ ] Tests pass locally
[ ] Docker image builds successfully
[ ] No credentials are committed
[ ] API health endpoint works
[ ] Code is ready for review
```

The Pull Request is not merged until the required CI checks have passed and the changes have been reviewed.

---

# 9. Continuous Integration

The CI workflow is defined in:

```text
.github/workflows/ci.yml
```

The workflow runs automatically when a Pull Request targets `main`.

### CI Pipeline

```text
Pull Request
     ↓
Checkout Code
     ↓
Setup Python
     ↓
Install Dependencies
     ↓
Run pytest
     ↓
Build Docker Image
     ↓
CI Success
```

The CI pipeline performs two important validations:

### Unit Tests

```bash
pytest
```

### Docker Build Validation

```bash
docker build .
```

The Docker image is built during CI to verify that the Dockerfile is valid.

The image is **not pushed to the registry during Pull Request CI**.

This keeps CI focused on validation rather than publishing release artifacts.

---

# 10. Deliberate CI Failure

As part of the exercise, a test was intentionally modified to fail.

For example:

```python
assert data["status"] == "wrong"
```

The change was committed and pushed to the feature branch.

The Pull Request then triggered GitHub Actions.

Expected result:

```text
Pull Request
     ↓
GitHub Actions
     ↓
pytest
     ↓
FAILED
```

This demonstrates that the CI pipeline can detect defective changes before they are merged into `main`.

The test was then corrected:

```python
assert data["status"] == "healthy"
```

The fix was committed using:

```bash
git commit -m "fix: correct health endpoint test"
```

After pushing the fix, CI successfully passed.

---

# 11. Branch Protection

The `main` branch is protected to prevent direct development.

The selected branch protection requirements include:

* Pull Request required before merging
* Successful CI checks required
* Direct pushes to `main` prevented
* Code review required before merging

This ensures that changes enter `main` through the controlled workflow:

```text
Feature Branch
      ↓
Pull Request
      ↓
CI
      ↓
Review
      ↓
main
```

---

# 12. Pull Request Merge Strategy

The project uses:

**Squash and Merge**

Squash merging combines the commits from a Pull Request into a single commit on `main`.

This provides a cleaner and easier-to-understand project history while preserving the Pull Request as the main review and discussion record.

---

# 13. Dockerization

The application is containerized using Docker.

The Dockerfile uses an explicit Python base image rather than:

```dockerfile
FROM python:latest
```

The Dockerfile follows common Docker best practices including:

* Explicit Python version
* `WORKDIR`
* Dependency installation
* `--no-cache-dir`
* Efficient Docker layer ordering
* `EXPOSE`
* Appropriate application startup command

A simplified build order is:

```text
COPY requirements.txt
        ↓
Install dependencies
        ↓
COPY application source
```

This improves Docker build caching because dependency layers can be reused when only application source code changes.

---

# 14. Docker Ignore

The `.dockerignore` file excludes unnecessary files from the Docker build context.

Examples include:

```text
.git
.github
__pycache__
*.pyc
.venv
.venvs
.env
```

This reduces the build context and prevents unnecessary or sensitive files from being copied into the image.

---

# 15. Local Docker Build

The initial application version is:

```text
1.0.0
```

The version is stored in:

```text
VERSION
```

The Docker image is built using:

```bash
docker build -t student-ml-api:1.0.0 .
```

The container is started with:

```bash
docker run -d \
  --name student-ml-api \
  -p 5000:5000 \
  student-ml-api:1.0.0
```

The API can then be tested using:

```bash
curl http://localhost:5000/health
```

Expected result:

```json
{
  "status": "healthy",
  "application": "student-ml-api",
  "version": "1.0.0"
}
```

---

# 16. Docker Inspection

The following Docker commands were used to inspect the application container.

### List images

```bash
docker images
```

### List running containers

```bash
docker ps
```

### View container logs

```bash
docker logs student-ml-api
```

### Inspect container configuration

```bash
docker inspect student-ml-api
```

### Access the container

```bash
docker exec -it student-ml-api sh
```

The inspection was used to identify:

* Container ID
* Image ID
* Exposed port
* Running command
* Application working directory

---

# 17. Container Registry

The project uses **GitHub Container Registry (GHCR)** to store Docker images.

The registry follows this naming convention:

```text
ghcr.io/<username>/student-ml-api:<version>
```

Example:

```text
ghcr.io/<username>/student-ml-api:1.0.0
```

The registry provides a central location for storing and distributing immutable, versioned Docker artifacts.

---

# 18. Semantic Versioning

The project uses semantic version tags.

Examples:

```text
v1.0.0
v1.1.0
v2.0.0
```

After version 1.0.0 was merged into `main`, the tag was created:

```bash
git checkout main
git pull
git tag v1.0.0
git push origin v1.0.0
```

The relationship is:

```text
Git Tag
v1.0.0
   ↓
Docker Image
student-ml-api:1.0.0
```

---

# 19. Automated Release Workflow

The release workflow is defined in:

```text
.github/workflows/release.yml
```

Unlike CI, the release workflow runs when a semantic-version tag is pushed.

Example trigger:

```text
v1.0.0
v1.1.0
v2.0.0
```

The workflow performs:

```text
Git Tag
   ↓
Checkout
   ↓
Run Tests
   ↓
Authenticate to Registry
   ↓
Build Docker Image
   ↓
Extract Version
   ↓
Tag Docker Image
   ↓
Push Image
```

The Docker version is automatically derived from the Git tag.

For example:

```text
Git tag:
v1.1.0

Docker tag:
1.1.0
```

The workflow does not manually hard-code the release version.

---

# 20. Docker Image Tags

The release process publishes:

```text
student-ml-api:1.0.0
student-ml-api:latest
```

For version 1.1.0, the registry contains:

```text
student-ml-api:1.0.0
student-ml-api:1.1.0
student-ml-api:latest
```

After releasing 1.1.0:

```text
latest → 1.1.0
```

The previous version remains available:

```text
1.0.0
```

This allows older known-good artifacts to be retrieved when required.

---

# 21. Artifact Reproducibility

The local Docker image for version 1.0.0 can be removed:

```bash
docker rmi student-ml-api:1.0.0
```

The image can then be retrieved from the registry:

```bash
docker pull ghcr.io/<username>/student-ml-api:1.0.0
```

The downloaded image can be run again:

```bash
docker run -d \
  --name student-ml-api \
  -p 5000:5000 \
  ghcr.io/<username>/student-ml-api:1.0.0
```

The API is verified using:

```bash
curl http://localhost:5000/health
```

This demonstrates that the application can be reproduced from the published container artifact without rebuilding the source code.

---

# 22. Version 1.1.0

A second feature branch was created:

```bash
git checkout -b feature/model-metadata
```

The `/health` endpoint was updated to expose application and model metadata.

Expected response:

```json
{
  "status": "healthy",
  "application": "student-ml-api",
  "application_version": "1.1.0",
  "model_version": "model-1"
}
```

The corresponding tests were updated.

The change followed the same professional workflow:

```text
feature/model-metadata
        ↓
Commit
        ↓
Push
        ↓
Pull Request
        ↓
CI
        ↓
Code Review
        ↓
Merge
```

Direct development on `main` was not used.

---

# 23. Version 1.1.0 Release

After the Pull Request was merged, the release tag was created:

```bash
git checkout main
git pull
git tag v1.1.0
git push origin v1.1.0
```

This triggered the release workflow.

The registry should contain:

```text
student-ml-api
├── 1.0.0
├── 1.1.0
└── latest
```

The `latest` tag points to the newest release:

```text
latest → 1.1.0
```

while version 1.0.0 remains available.

---

# 24. Rollback

To demonstrate rollback, version 1.1.0 is treated as a problematic release.

Instead of rebuilding the application or cloning the source code again, the known-good 1.0.0 image is retrieved from the registry:

```bash
docker pull ghcr.io/<username>/student-ml-api:1.0.0
```

The 1.0.0 image can then be run:

```bash
docker run -d \
  --name student-ml-api-rollback \
  -p 5000:5000 \
  ghcr.io/<username>/student-ml-api:1.0.0
```

The API is verified:

```bash
curl http://localhost:5000/health
```

The rollback is fast because the previously built and tested Docker artifact already exists in the registry.

No source-code modification or image rebuild is required.

---

# 25. CI vs Release Workflow

The project intentionally separates CI and release responsibilities.

## CI Workflow

Triggered by:

```text
Pull Request → main
```

Responsibilities:

* Checkout source code
* Install dependencies
* Run tests
* Validate Docker build

CI does **not** publish Docker images.

## Release Workflow

Triggered by:

```text
Git Tag
```

Responsibilities:

* Checkout source code
* Run tests
* Authenticate with registry
* Build Docker image
* Generate version tag
* Publish Docker image

### Comparison

| CI                  | Release                  |
| ------------------- | ------------------------ |
| Pull Request        | Semantic Git tag         |
| Validates code      | Publishes artifact       |
| Runs tests          | Runs tests               |
| Builds Docker image | Builds Docker image      |
| Does not push image | Pushes image             |
| Prevents bad merges | Creates release artifact |

Publishing an image from every Pull Request is generally undesirable because Pull Requests may contain incomplete, experimental, or unapproved changes. The registry should primarily contain reviewed and released artifacts.

---

# 26. Image Metadata

The Docker image includes OCI metadata to improve artifact traceability.

Relevant metadata can include:

```text
Application Version
Git Commit SHA
Repository
Build Date
```

This allows an image to be associated with the source code that produced it.

The metadata can be inspected using:

```bash
docker inspect <image>
```

This provides an additional traceability mechanism beyond Docker tags.

---

# 27. Commit-Specific Image Tag

In addition to version and latest tags, the release process can publish a commit-specific tag.

Example:

```text
student-ml-api:1.1.0
student-ml-api:latest
student-ml-api:92f4abc
```

A commit-specific tag makes it possible to identify the exact source commit associated with an image.

This is useful for:

* Debugging
* Auditing
* Reproducibility
* Incident investigation
* Deployment traceability

---

# 28. Docker Build Cache

The Dockerfile is structured so that dependencies are installed before application source code is copied.

Preferred structure:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
```

If only `app.py` changes, Docker can reuse the dependency installation layer.

However, if `requirements.txt` changes, the dependency installation layer must be rebuilt.

This improves CI/CD performance by avoiding unnecessary dependency installation.

---

# 29. Failure Analysis

The project includes deliberate failure scenarios to demonstrate troubleshooting.

Each failure is documented using:

```text
Symptom
Root Cause
Evidence
Correction
```

Examples of failures considered include:

* Failed pytest
* Failed Docker build
* Incorrect container port
* Application bound to `127.0.0.1`
* Invalid registry credentials
* Registry push denied
* Incorrect Docker image tag
* Missing Python dependency

Failure analysis demonstrates that CI/CD systems are not only automation tools but also mechanisms for detecting and diagnosing problems early.

---

# 30. Traceability

The complete artifact chain is:

```text
Pull Request
     ↓
Commit
     ↓
Merge into main
     ↓
Git Tag
     ↓
Docker Image
     ↓
Docker Image Digest
```

For example:

```text
PR: #<PR_NUMBER>

Merge Commit: <MERGE_COMMIT_SHA>

Git Tag: v1.1.0

Docker Image:
ghcr.io/<username>/student-ml-api:1.1.0

Image Digest:
sha256:<IMAGE_DIGEST>
```

The actual values should be taken from the GitHub repository and container registry.

This ensures that a released Docker artifact can be traced back to the source-code change that produced it.

---

# 31. Registry Verification

After the release workflow completes, the container registry should contain:

```text
student-ml-api
│
├── 1.0.0
├── 1.1.0
└── latest
```

The image digest can be obtained from the registry or Docker commands.

Example:

```text
sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The digest provides an immutable identifier for the image artifact.

---

# 32. Reproducibility

The project demonstrates reproducibility using the container registry.

The same Docker image can be:

```text
Built once
    ↓
Stored in Registry
    ↓
Pulled later
    ↓
Run in another environment
```

This is preferable to rebuilding an application from source because rebuilding may produce differences caused by dependency changes, environment differences, or build-time conditions.

The registry therefore acts as the source of released deployment artifacts.

---

# 33. Why Not Directly Push to Main?

Direct development on `main` is avoided because it can introduce unreviewed or broken changes into the primary branch.

The Pull Request workflow provides:

* Code review
* Automated validation
* Discussion
* Change visibility
* Controlled integration
* Auditability

Therefore:

```text
Feature Branch → PR → CI → Review → main
```

is safer than:

```text
Developer → main
```

---

# 34. Why Version Docker Images?

Using only:

```text
student-ml-api:latest
```

does not provide sufficient release traceability.

Versioned images provide explicit references such as:

```text
student-ml-api:1.0.0
student-ml-api:1.1.0
```

This allows teams to identify exactly which release is being deployed and makes rollback easier.

---

# 35. Why Use a Container Registry?

A container registry provides centralized storage for Docker images.

It allows teams to:

* Store release artifacts
* Distribute images
* Deploy images to different environments
* Retrieve previous versions
* Support rollback
* Maintain artifact history

In this project, GitHub Container Registry is used.

---

# 36. Why Use Secrets?

Registry credentials should never be hard-coded into GitHub Actions workflows.

Sensitive credentials should be stored using GitHub Secrets.

This prevents credentials from being exposed through:

* Source code
* Git history
* Pull Requests
* Workflow files

The release workflow authenticates with the registry using secure credentials provided through GitHub's secret-management mechanism.

---

# 37. Demonstration Workflow

The complete project can be demonstrated using the following sequence:

```text
Clone Repository
      ↓
Inspect Git History
      ↓
Inspect Pull Requests
      ↓
Inspect GitHub Actions
      ↓
Inspect Release Tags
      ↓
Pull Docker Image
      ↓
Run Container
      ↓
Test API
      ↓
Inspect Container
      ↓
Demonstrate Rollback
```

---

# 38. Final MLOps Pipeline

```text
                    Developer
                        │
                        ▼
                 Feature Branch
                        │
                        ▼
                  Git Commit
                        │
                        ▼
                 Pull Request
                        │
                        ▼
              ┌──────────────────┐
              │   GitHub Actions │
              │       CI         │
              │                  │
              │  • Unit Tests    │
              │  • Docker Build  │
              └────────┬─────────┘
                       │
                       ▼
                  Code Review
                       │
                       ▼
                  Merge to main
                       │
                       ▼
                Semantic Tag
                   v1.1.0
                       │
                       ▼
              Release Workflow
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
            Tests          Docker Build
              │                 │
              └────────┬────────┘
                       ▼
              Container Registry
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        1.0.0        1.1.0       latest
                       │
                       ▼
                 Deployment
                       │
                       ▼
                   Rollback
                 if required
```

---

# 39. Key Learning Outcomes

After completing this exercise, the following concepts are demonstrated:

* Git provides source-code version control.
* Feature branches isolate development work.
* Pull Requests provide controlled code integration.
* CI validates changes before merging.
* Docker creates reproducible application artifacts.
* Semantic versioning identifies releases.
* Git tags connect source-code versions with releases.
* Container registries store and distribute Docker artifacts.
* Image digests provide immutable artifact identification.
* OCI metadata improves traceability.
* Commit-specific image tags identify exact source versions.
* CI and release workflows should have separate responsibilities.
* Previously built artifacts can be reused for rollback.
* Docker layer caching improves build performance.

---

# 40. Core Principle

The central principle demonstrated by this project is:

> **Git manages the evolution of source code. Pull Requests control how changes enter the main branch. CI verifies those changes. Docker converts approved source code into a reproducible artifact. The container registry stores and distributes versioned artifacts.**

The complete relationship is:

```text
Source Code
     ↓
Feature Branch
     ↓
Pull Request
     ↓
CI Validation
     ↓
Code Review
     ↓
main
     ↓
Git Tag
     ↓
Docker Build
     ↓
Container Registry
     ↓
Versioned Artifact
     ↓
Deployment / Rollback
```

This workflow provides a traceable and reproducible foundation for a production-oriented MLOps system.
