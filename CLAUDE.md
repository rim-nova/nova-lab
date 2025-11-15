# CLAUDE.md - AI Assistant Guide for NovaLab

## Project Overview

**NovaLab** is an AI-powered analytics tool that transforms natural language into data cleaning, analysis, visualizations, and machine learning workflows. The goal is to make data science accessible, fast, and powerful for all users regardless of technical expertise.

**Repository:** rim-nova/nova-lab
**License:** MIT
**Author:** Tanzina Afrin Rimi
**Current Stage:** Initial Development (Greenfield Project)

---

## Repository Structure

```
nova-lab/
├── README.md              # Project description and overview
├── LICENSE                # MIT License
├── CLAUDE.md             # This file - AI assistant guidance
└── [To be developed]     # Project structure will evolve
```

### Expected Future Structure

As development progresses, the repository should follow this structure:

```
nova-lab/
├── src/                   # Source code
│   ├── core/             # Core analytics engine
│   ├── nlp/              # Natural language processing
│   ├── ml/               # Machine learning models
│   ├── visualization/    # Data visualization components
│   └── api/              # API endpoints
├── tests/                # Test suites
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── docs/                 # Documentation
├── examples/             # Usage examples
├── scripts/              # Build and deployment scripts
├── config/               # Configuration files
└── data/                 # Sample datasets (gitignored)
```

---

## Technology Stack Considerations

Since this is a greenfield project, here are recommended technology stacks for different approaches:

### Option 1: Python-Based Stack
- **Language:** Python 3.11+
- **Data Processing:** pandas, numpy, polars
- **ML/AI:** scikit-learn, TensorFlow/PyTorch, transformers
- **NLP:** spaCy, NLTK, Hugging Face transformers
- **Visualization:** matplotlib, plotly, seaborn
- **API:** FastAPI or Flask
- **Testing:** pytest, unittest

### Option 2: Node.js/TypeScript Stack
- **Language:** TypeScript 5.x
- **Data Processing:** danfo.js, Apache Arrow
- **ML/AI:** TensorFlow.js, ONNX Runtime
- **NLP:** compromise, natural, OpenAI API
- **Visualization:** D3.js, Chart.js, Plotly.js
- **API:** Express, NestJS, or tRPC
- **Testing:** Jest, Vitest

### Option 3: Hybrid Approach
- **Backend:** Python for ML/data processing
- **Frontend:** TypeScript/React for UI
- **API:** GraphQL or REST
- **Communication:** gRPC or HTTP/WebSocket

---

## Development Principles

### 1. Code Quality Standards

- **Type Safety:** Use type hints (Python) or TypeScript
- **Documentation:** All public APIs must have docstrings/JSDoc
- **Testing:** Minimum 80% code coverage
- **Linting:** Use appropriate linters (pylint/ruff for Python, ESLint for TS)
- **Formatting:** Black (Python) or Prettier (TS/JS)

### 2. Git Workflow

- **Branch Naming:**
  - Feature branches: `feature/<description>`
  - Bug fixes: `fix/<issue-number>-<description>`
  - AI assistant branches: `claude/<session-id>`

- **Commit Messages:**
  - Use conventional commits: `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
  - Example: `feat(nlp): add query parser for natural language`

- **Pull Requests:**
  - Must pass all CI checks
  - Require code review for main branch
  - Include tests for new features
  - Update documentation as needed

### 3. Architecture Patterns

- **Modularity:** Keep components loosely coupled
- **Dependency Injection:** Use DI for testability
- **Clean Architecture:** Separate business logic from infrastructure
- **API-First:** Design APIs before implementation
- **Error Handling:** Consistent error handling across modules

---

## Key Features to Implement

### Core Capabilities

1. **Natural Language Query Processing**
   - Parse user queries in natural language
   - Convert to data operations
   - Support complex analytical questions

2. **Data Cleaning & Preprocessing**
   - Handle missing values
   - Detect and remove outliers
   - Data type inference and conversion
   - Data validation

3. **Data Analysis**
   - Descriptive statistics
   - Correlation analysis
   - Time series analysis
   - Grouping and aggregation

4. **Visualization Generation**
   - Auto-suggest appropriate charts
   - Interactive visualizations
   - Export capabilities (PNG, SVG, PDF)

5. **Machine Learning**
   - Auto-ML capabilities
   - Model selection and tuning
   - Feature engineering
   - Model evaluation and comparison

---

## AI Assistant Guidelines

### When Working on This Codebase

1. **Always Check Dependencies First**
   - Before adding code, check if package.json/requirements.txt exists
   - Verify the chosen tech stack before making assumptions
   - Ask for clarification if the direction is unclear

2. **Maintain Consistency**
   - Follow existing code style and patterns
   - Match the architecture of existing components
   - Use the same testing framework throughout

3. **Security Considerations**
   - Never commit API keys or secrets
   - Validate all user inputs
   - Use parameterized queries for databases
   - Implement proper authentication/authorization
   - Be mindful of injection attacks (SQL, command, XSS)

4. **Performance Optimization**
   - Profile before optimizing
   - Consider memory usage for large datasets
   - Use streaming for big data processing
   - Implement caching where appropriate
   - Use async/await for I/O operations

5. **Documentation Requirements**
   - Update README.md for major features
   - Add inline comments for complex logic
   - Create/update API documentation
   - Include usage examples
   - Document configuration options

6. **Testing Strategy**
   - Write tests before or alongside code (TDD encouraged)
   - Test edge cases and error conditions
   - Use fixtures for test data
   - Mock external dependencies
   - Integration tests for critical paths

---

## Common Development Workflows

### Adding a New Feature

1. Create a feature branch from main
2. Design the API/interface first
3. Write tests for the feature
4. Implement the feature
5. Update documentation
6. Run full test suite
7. Create pull request
8. Address review comments
9. Merge to main

### Bug Fixing

1. Reproduce the bug with a test case
2. Create a fix branch
3. Fix the bug
4. Ensure test passes
5. Check for similar issues
6. Create pull request with test

### Refactoring

1. Ensure good test coverage exists
2. Make incremental changes
3. Run tests after each change
4. Update documentation if APIs change
5. Commit frequently with clear messages

---

## File Naming Conventions

### Python
- Modules: `snake_case.py`
- Classes: `PascalCase`
- Functions/Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

### TypeScript/JavaScript
- Files: `kebab-case.ts` or `PascalCase.tsx` (for React components)
- Classes/Components: `PascalCase`
- Functions/Variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE` or `camelCase` for config objects

---

## Configuration Management

### Environment Variables

Store sensitive configuration in environment variables:
- Database URLs
- API keys
- Service credentials
- Feature flags

### Configuration Files

Use appropriate config files:
- `.env.example` - Template for environment variables
- `config.yaml` or `config.json` - Application configuration
- `.env` - Local environment (gitignored)

---

## Data Privacy & Ethics

Given the analytics nature of this tool:

1. **User Data:**
   - Never store user data without consent
   - Provide clear data retention policies
   - Allow users to delete their data
   - Encrypt sensitive data

2. **Model Fairness:**
   - Test for bias in ML models
   - Document model limitations
   - Provide interpretability features
   - Allow human oversight

3. **Transparency:**
   - Explain how analyses are performed
   - Show confidence scores
   - Provide source citations

---

## Performance Benchmarks

As the project develops, maintain benchmarks for:
- Query processing time
- Data loading speed
- Model training time
- Visualization rendering
- API response times

Target metrics (to be refined):
- Query response: < 2 seconds for typical queries
- Data upload: Handle files up to 1GB
- Visualization: < 500ms render time
- API: 95th percentile < 200ms

---

## Deployment Considerations

### Development Environment
- Local development setup
- Hot reloading
- Debug mode enabled
- Sample data included

### Staging Environment
- Production-like configuration
- Test data (anonymized)
- Performance monitoring
- Integration testing

### Production Environment
- Scalability (horizontal scaling)
- Load balancing
- Caching (Redis/Memcached)
- CDN for static assets
- Database replication
- Automated backups
- Monitoring and alerting

---

## Dependencies to Consider

### Core Dependencies
- Data processing library (pandas/polars or equivalent)
- ML framework (scikit-learn/TensorFlow or equivalent)
- NLP library (spaCy/transformers or equivalent)
- Visualization library
- Web framework
- Database client

### Development Dependencies
- Testing framework
- Code formatter
- Linter
- Type checker
- Documentation generator
- Pre-commit hooks

---

## Current State & Next Steps

### Current State (as of 2025-11-15)
- ✅ Repository initialized
- ✅ README.md created
- ✅ MIT License added
- ✅ CLAUDE.md created
- ⏳ Technology stack to be determined
- ⏳ Project structure to be defined

### Immediate Next Steps

1. **Define Technology Stack**
   - Choose primary programming language
   - Select framework and libraries
   - Set up development environment

2. **Project Setup**
   - Initialize package manager (npm/pip/poetry)
   - Create directory structure
   - Set up linting and formatting
   - Configure git hooks

3. **Core Architecture**
   - Design system architecture
   - Define API contracts
   - Plan database schema
   - Create initial modules

4. **Development Infrastructure**
   - Set up CI/CD pipeline
   - Configure testing framework
   - Set up documentation system
   - Create development guidelines

---

## Questions for Clarification

When working on this project, consider these questions:

1. **Target Users:** Who is the primary audience? (Data scientists, analysts, business users?)
2. **Deployment:** Web app, desktop app, CLI, or API service?
3. **Data Sources:** What data formats/sources should be supported? (CSV, JSON, SQL databases, APIs?)
4. **Scale:** Expected data volume and concurrent users?
5. **AI Integration:** Which LLM/AI service for NLP? (OpenAI, Anthropic, open-source?)
6. **Visualization:** Interactive dashboards or static reports?

---

## Resources & References

### Documentation
- [Project README](README.md)
- [License](LICENSE)

### External Resources
- pandas documentation: https://pandas.pydata.org/docs/
- scikit-learn: https://scikit-learn.org/
- Plotly: https://plotly.com/
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/

---

## Changelog

### 2025-11-15
- Initial CLAUDE.md created
- Repository structure defined
- Development guidelines established

---

## Contact & Support

For questions or issues:
- GitHub Issues: [Repository Issues](https://github.com/rim-nova/nova-lab/issues)
- Maintainer: Tanzina Afrin Rimi

---

**Note to AI Assistants:** This is a greenfield project in its initial stages. When implementing features:
1. Propose the technology stack if not yet defined
2. Follow best practices for the chosen stack
3. Keep the architecture flexible and maintainable
4. Prioritize user experience and simplicity
5. Document all decisions and trade-offs
