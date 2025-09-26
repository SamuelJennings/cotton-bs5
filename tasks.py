import subprocess
import time

import requests
from invoke import task


@task
def docs(c):
    # Start Django dev server
    server = subprocess.Popen(
        ["poetry", "run", "python", "manage.py", "runserver", "8001"],  # noqa: S607
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        # Wait for the server to start
        for _ in range(20):
            try:
                resp = requests.get("http://localhost:8001/")  # noqa: S113
                if resp.status_code == 200:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            print("Django server did not start in time.")
            server.terminate()
            return

        # Run shot-scraper
        c.run("shot-scraper html http://localhost:8001/ -o docs/index.html")
    finally:
        server.terminate()
        server.wait()


@task
def prerelease(c):
    """
    Run comprehensive pre-release checks and update all required files.

    This task performs all necessary steps to prepare the repository for release:
    1. Run linting and formatting (including poetry-lock hook)
    2. Run all quality checks and tests
    3. Update requirements.txt

    Use this before running the release task to ensure everything is ready.
    """
    print("🚀 Starting comprehensive pre-release checks...")
    print("=" * 60)

    # Step 1: Run comprehensive linting and type checking (including poetry-lock)
    print("\n🧹 Step 1: Running comprehensive linting and type checking")
    print("🚀 Running pre-commit hooks")
    c.run("poetry run pre-commit run -a")

    print("🚀 Running manual pre-commit hooks (poetry-lock, poetry-export)")
    c.run("poetry run pre-commit run --hook-stage manual -a")

    # Step 2: Check Poetry lock file consistency
    print("\n🔍 Step 2: Checking Poetry lock file consistency")
    print("🚀 Checking Poetry lock file consistency with 'pyproject.toml'")
    c.run("poetry check --lock")

    print("🚀 Checking for obsolete dependencies with deptry")
    c.run("poetry run deptry .")

    # Step 3: Run comprehensive test suite
    print("\n🧪 Step 3: Running comprehensive test suite")
    print("🚀 Running pytest with coverage")
    c.run("poetry run pytest --cov --cov-config=pyproject.toml --cov-report=html")

    # Step 4: Update requirements.txt (final step)
    print("\n📦 Step 4: Updating requirements.txt")
    print("🚀 Exporting Poetry dependencies to requirements.txt")
    c.run("poetry export -o requirements.txt --with=dev --without-hashes")

    print("\n" + "=" * 60)
    print("✅ Pre-release checks completed successfully!")
    print(
        "🎉 Repository is ready for release. You can now run 'invoke release' with the appropriate rule."
    )
    print("   Example: invoke release --rule=patch")


@task
def release(c, rule="", commit_staged=False):
    """
    Create a new git tag and push it to the remote repository.

    .. note::
        This will create a new tag and push it to the remote repository, which will trigger a new build and deployment of the package to PyPI.

    Args:
        rule: Version bump rule (major, minor, patch, etc.)
        commit_staged: If True, commit all staged changes along with the version bump

    RULE	    BEFORE	AFTER
    major	    1.3.0	2.0.0
    minor	    2.1.4	2.2.0
    patch	    4.1.1	4.1.2
    premajor	1.0.2	2.0.0a0
    preminor	1.0.2	1.1.0a0
    prepatch	1.0.2	1.0.3a0
    prerelease	1.0.2	1.0.3a0
    prerelease	1.0.3a0	1.0.3a1
    prerelease	1.0.3b0	1.0.3b1
    """
    if rule:
        # bump the current version using the specified rule
        c.run(f"poetry version {rule}")

    # 1. Get the current version number as a variable
    version_short = c.run("poetry version -s", hide=True).stdout.strip()
    version = c.run("poetry version", hide=True).stdout.strip()

    # 2. commit the changes to pyproject.toml (and optionally staged changes)
    if commit_staged:
        # Check if there are any staged changes
        staged_result = c.run("git diff --cached --name-only", hide=True, warn=True)
        if staged_result.stdout.strip():
            print(f"🚀 Committing staged changes and version bump for v{version_short}")
            c.run(f'git add pyproject.toml && git commit -m "Release v{version_short}"')
        else:
            print(
                f"🚀 No staged changes found, committing only version bump for v{version_short}"
            )
            c.run(f'git commit pyproject.toml -m "Release v{version_short}"')
    else:
        c.run(f'git commit pyproject.toml -m "Release v{version_short}"')

    # 3. create a tag and push it to the remote repository
    c.run(f'git tag -a v{version_short} -m "{version}"')
    c.run("git push --tags")
    c.run("git push origin main")
