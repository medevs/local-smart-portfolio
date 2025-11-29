# Contributing Guidelines

## Commit Message Rules

### ⚠️ IMPORTANT: Maximum 10 Words

All commit messages must be **10 words or less**.

**Note**: `.gitmessage` is a local file (in .gitignore). Each developer should create their own copy if they want to use git commit templates.

**Examples:**
- ✅ "Add user authentication"
- ✅ "Fix login bug"  
- ✅ "Update dependencies"
- ✅ "Cleanup: enhance .gitignore"

- ❌ "Add user authentication with JWT tokens and refresh token support" (too long)
- ❌ "Fix the login bug that was causing users to be unable to log in" (too long)

### Format Guidelines:
- Use imperative mood (Add, Fix, Update, Remove)
- Be concise and descriptive
- Optional prefixes: "Fix:", "Add:", "Update:", "Remove:", "Cleanup:"

---

## Code Style

- Follow existing code patterns
- Use TypeScript for frontend
- Use Python type hints for backend
- Run linters before committing

---

## Pull Requests

- Keep PRs focused on a single feature/fix
- Update documentation if needed
- Test changes locally before submitting

