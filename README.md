# grimOS Platform

grimOS (Grimoire™) is a comprehensive AI-powered operating system that brings together agents, workflows, interoperability, and natural language interaction to transform enterprise operations. The platform consists of several core modules:

# Architecture Overview (Based on System Architecture Document)

grimOS employs a modular and layered architecture designed for scalability, maintainability, and flexibility. The core design principles include a microservices approach, event-driven communication, and clear separation of concerns across different tiers.

## High-Level Architecture

The grimOS architecture can be visualized with the following logical layers and tiers:

### Overview Diagram

*(Based on the conceptual diagram described in the System Architecture Document)*



## Architecture Overview
 
grimOS uses a modern, microservices-based architecture with the following components:

- **Presentation Tier**: Next.js frontend with React, shadcn/ui, Tailwind CSS
- **API Tier**: Universal API Fabric & API Gateway
- **Application Tier**: Microservices including Cognitive Core, Composable Runes, etc.
- **Messaging & Event Bus**: Apache Kafka for event-driven communication
- **Data Tier**: PostgreSQL, Redis, ChromaDB (vector database), and more

The core modules are implemented as separate microservices within the `services` directory.

## Project Structure

- `/apps/backend`: Main backend application
- `/apps/frontend`: Next.js frontend application
- `/services`: Microservices implementations of the core modules
  - `/services/ai`: Cognitive Core service
  - `/services/composable-runes`: Workflow engine service
  - `/services/interoperability`: Integration service
  - `/services/api-gateway`: API Gateway service
- `/packages`: Shared libraries and utilities
- `/docs`: Documentation and specifications
- `/charts`: Kubernetes deployment configurations
- `/deploy`: Deployment scripts and configurations
- `/apps/web`: Website and landing page for the platform (likely using a different framework or simpler setup than the main frontend)
- `/packages/shared`: Shared TypeScript utilities, components, and types used across frontend and backend
- `/packages/shared-python`: Shared Python utilities and libraries used across Python services
- `/services/api-gateway`: Acts as the entry point for external requests, routing them to the appropriate microservices.
- `/services/auth`: Handles user authentication and authorization (part of the User Module).
- `/services/bitbrew`: This service's purpose is not explicitly defined in the main module list but appears to be a service within the `services` directory. Further analysis of its code would be needed to determine its function and dependencies.
- `/services/event-consumer`: Likely consumes events from the Kafka message bus for various purposes (e.g., triggering actions, updating databases).
- `/services/protos`: Contains Protocol Buffer definitions for gRPC communication between services.
- `/services/stats`: Likely handles statistics collection and reporting.
- `/services/user`: Manages user-related data and logic (the main part of the User Module).

## Module Dependencies

* The API Gateway depends on the other microservices to route requests.
* The Frontend application communicates with the services through the API Gateway.
* Services likely communicate with each other via gRPC (using definitions in `/services/protos`) and/or the Kafka message bus.
* Services interact with the Data Tier (PostgreSQL, Redis, ChromaDB).

<a href="https://blazity.com/">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/assets/blazity-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="/assets/blazity-logo-light.svg">
  <img alt="Logo" align="right" height="80" src="/assets/blazity-logo-light.svg">
</picture>
</a>

> [!NOTE] > **Blazity** is a group of Next.js architects. We help organizations architect, optimize, and deploy high-performance Next.js applications at scale. Contact us at [contact@blazity.com](https://blazity.com) if you’d like to talk about your project.

## Documentation

There is a separate documentation that explains its functionality, highlights core business values and technical decisions, provides guidelines for future development, and includes architectural diagrams.

We encourage you to [visit our docs (docs.blazity.com)](https://docs.blazity.com) to learn more

## Integrated features

### Boilerplate

With this template you will get all the boilerplate features included:

* [Next.js 15](https://nextjs.org/) - Performance-optimized configuration using App Directory
* [Tailwind CSS v4](https://tailwindcss.com/) - Utility-first CSS framework for efficient UI development
* [ESlint 9](https://eslint.org/) and [Prettier](https://prettier.io/) - Code consistency and error prevention
* [Corepack](https://github.com/nodejs/corepack) & [pnpm](https://pnpm.io/) as the package manager - For project management without compromises
* [Strict TypeScript](https://www.typescriptlang.org/) - Enhanced type safety with carefully crafted config and [ts-reset](https://github.com/total-typescript/ts-reset) library
* [GitHub Actions](https://github.com/features/actions) - Pre-configured workflows including bundle size and performance tracking
* Perfect Lighthouse score - Optimized performance metrics
* [Bundle analyzer](https://www.npmjs.com/package/@next/bundle-analyzer) - Monitor and manage bundle size during development
* Testing suite - [Jest](https://jestjs.io/), [React Testing Library](https://testing-library.com/react), and [Playwright](https://playwright.dev/) for comprehensive testing
* [Storybook](https://storybook.js.org/) - Component development and documentation
* Advanced testing - Smoke and acceptance testing capabilities
* [Conventional commits](https://www.conventionalcommits.org/) - Standardized commit history management
* [Observability](https://opentelemetry.io/) - Open Telemetry integration
* [Absolute imports](https://nextjs.org/docs/advanced-features/module-path-aliases) - Simplified import structure
* [Health checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) - Kubernetes-compatible monitoring
* [Radix UI](https://www.radix-ui.com/) - Headless components for customization
* [CVA](http://cva.style/) (Class Variance Authority) - Consistent design system creation
* [Renovate BOT](https://www.whitesourcesoftware.com/free-developer-tools/renovate) - Automated dependency and security updates
* [Patch-package](https://www.npmjs.com/package/patch-package) - External dependency fixes without compromises
* Component relationship tools - Graph for managing coupling and cohesion
* [Semantic Release](https://github.com/semantic-release/semantic-release) - Automated changelog generation
* [T3 Env](https://env.t3.gg/) - Streamlined environment variable management

### Infrastructure & deployments

#### Vercel

Easily deploy your Next.js app with [Vercel](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=github&utm_campaign=next-enterprise) by clicking the button below:

[![Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https://github.com/Blazity/next-enterprise)

#### Custom cloud infrastructure

**next-enterprise** offers dedicated infrastructure as code (IaC) solutions built with Terraform, designed specifically for deploying Next.js applications based on our extensive experience working with enterprise clients.

Learn more in our [documentation (docs.blazity.com)][docs] how to quickstart with the deployments using simple CLI.

#### Available cloud providers and theirs features:

* **AWS (Amazon Web Services)**
  * Automated provisioning of AWS infrastructure
  * Scalable & secure setup using:
    * VPC - Isolated network infrastructure
    * Elastic Container Service (ECS) - Container orchestration
    * Elastic Container Registry (ECR) - Container image storage
    * Application Load Balancer - Traffic distribution
    * S3 + CloudFront - Static asset delivery and caching
    * AWS WAF - Web Application Firewall protection
    * Redis Cluster - Caching
  * CI/CD ready - Continuous integration and deployment pipeline

_... more coming soon_

### Team & maintenance

**next-enterprise** is backed and maintained by [Blazity](https://blazity.com), providing up to date security features and integrated feature updates.

#### Active maintainers

* Igor Klepacki ([neg4n](https://github.com/neg4n)) - Open Source Software Developer
* Tomasz Czechowski ([tomaszczechowski](https://github.com/tomaszczechowski)) - Solutions Architect & DevOps
* Jakub Jabłoński ([jjablonski-it](https://github.com/jjablonski-it)) - Head of Integrations

#### All-time contributors

[bmstefanski](https://github.com/bmstefanski)

## License

MIT

[docs]: https://docs.blazity.com/next-enterprise/deployments/enterprise-cli
