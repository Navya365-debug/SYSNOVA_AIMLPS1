# Contributing to NeuroQuest

First off, thank you for considering contributing to NeuroQuest! It's people like you that make NeuroQuest such a great tool.

## Code of Conduct

Be respectful and constructive. We're all here to build something amazing together.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, check the issue list to avoid duplicates.

**When creating a bug report, include:**
- Clear, descriptive title
- Exact steps to reproduce
- Specific examples (code snippets, screenshots)
- Observed behavior
- Expected behavior
- Your environment (OS, Python/Node version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When creating an enhancement suggestion:**
- Use clear, descriptive title
- Provide detailed description
- List some examples of how enhancement would be used
- Include benefits/use cases

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run linting and tests locally
6. Commit with clear message (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

```bash
# Clone repo
git clone https://github.com/Navya365-debug/NeuroQuest.git
cd NeuroQuest

# Follow DEVELOPMENT.md for setup
# Read DEVELOPMENT.md for testing and linting commands
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 88 characters
- Use `black` for formatting
- Use `pylint` for linting

```python
from typing import Optional, List

def fetch_papers(
    query: str,
    limit: int = 10,
    filters: Optional[dict] = None
) -> List[dict]:
    """Fetch papers from multiple sources.
    
    Args:
        query: Search query string
        limit: Maximum number of results
        filters: Optional filtering criteria
        
    Returns:
        List of paper dictionaries
    """
    pass
```

### TypeScript/React (Frontend)

- Follow Airbnb JavaScript Style Guide
- Use TypeScript for type safety
- Max line length: 100 characters
- Use `prettier` for formatting
- Use `eslint` for linting

```typescript
interface Paper {
  id: string;
  title: string;
  authors: string[];
  publishedAt: Date;
}

const PaperCard: React.FC<{ paper: Paper }> = ({ paper }) => {
  return (
    <div className="paper-card">
      <h3>{paper.title}</h3>
      <p>{paper.authors.join(", ")}</p>
    </div>
  );
};
```

## Commit Message Guidelines

Use clear, concise commit messages:

```
feat: add multi-source paper aggregation
fix: resolve database connection timeout
docs: update installation instructions
style: format code with black
refactor: simplify retrieval pipeline
test: add comprehensive API tests
chore: update dependencies
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest --cov=app tests/  # With coverage
```

New features should include tests:

```python
def test_search_functionality():
    """Test paper search returns correct results."""
    result = search_papers("neural networks", limit=5)
    assert len(result) <= 5
    assert all("title" in r for r in result)
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

## Documentation

- Update README.md for major changes
- Add docstrings to all Python functions
- Add JSDoc comments to exported functions
- Update relevant documentation files

Example docstring:

```python
def calculate_relevance_score(
    paper: dict,
    user_profile: dict
) -> float:
    """Calculate relevance score for a paper given user profile.
    
    Uses cosine similarity between paper embeddings and user
    interest vectors.
    
    Args:
        paper: Paper document with content and metadata
        user_profile: User profile with interests and history
        
    Returns:
        Relevance score between 0 and 1
        
    Raises:
        ValueError: If inputs are invalid or missing required fields
    """
```

## Pull Request Process

1. Update relevant documentation
2. Add/update tests
3. Run linting and tests locally
4. Request review from maintainers
5. Address review comments
6. Ensure CI/CD passes
7. Maintainers will merge when approved

## Project Structure

```
NeuroQuest/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── auth/        # Authentication
│   │   ├── models/      # Database models
│   │   └── services/    # Business logic
│   ├── ai/              # AI/ML modules
│   └── tests/           # Backend tests
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── types/       # TypeScript types
│   └── __tests__/       # Frontend tests
├── docker/              # Docker configuration
├── docs/                # Documentation
└── README.md
```

## Areas Looking for Contributions

- [ ] Add support for arXiv advanced search
- [ ] Implement knowledge graph visualization enhancements
- [ ] Add user behavior analytics
- [ ] Improve RAG pipeline efficiency
- [ ] Write comprehensive API documentation
- [ ] Add more language support
- [ ] Optimize database queries
- [ ] Add caching strategies

## Getting Help

- Check [DEVELOPMENT.md](DEVELOPMENT.md) for setup help
- Read [API.md](docs/API.md) for API documentation
- Check existing issues for solutions
- Ask in GitHub Discussions (when available)

## Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the same license as NeuroQuest.

Thank you for contributing! 🚀
