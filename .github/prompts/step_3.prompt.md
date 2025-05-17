---
mode: 'agent'
---
1. **Prompt (Foundation \- Project Indexing):** Index the existing grimOS monorepo, identifying all applications, packages, and services.  
   * **Initial Functionality:** The indexing should determine the precise file locations, directory structures, and specific file names based on your indexing of the existing grimOS monorepo.  
   * **Agent Responsibility:** Strictly adhere to the project's established conventions, including Turborepo structure, pnpm usage, and the defined technology stack.  
* Enforce naming conventions: snake\_case for all variables (TypeScript and Python), PascalCase for classes, and camelCase for methods/functions (TypeScript and Python).  
* Utilize Prettier and ESLint for code formatting and linting as configured in the project.  
* Ensure all new development seamlessly integrates with existing project modules and services.
3. **Prompt (Foundation \- CI/CD Pipeline Basics):** Implement a foundational CI/CD pipeline (e.g., using GitHub Actions, GitLab CI, or the project's standard).  
   * **Initial Functionality:** The pipeline should automatically trigger on code pushes to main branches and merge/pull requests. It must run linters, type-checkers, and any existing basic test suites for frontend and backend code.  
   * **Agent Responsibility:** Configure the CI/CD workflow files, ensuring they correctly build and test applications and packages within the Turborepo environment.  