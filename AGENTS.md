# Introduction

First, read `README.md` to understand the situation, background and problem statement we are addressing and the solution we are building. Then continue from here.

# Structure

This folder contains the root of an enterprise SaaS. This SaaS follows a super-app model where the index.html in the `frontend/` folder contains the main frontend shell of the application. Each individual application's frontend code is contained in a separate sub-folder within `frontend/` such as `tenant/`. The backend is Asp.Net Core 10.0 application whose code is in the `api/` folder. All APIs are served by this backend; all frontend routes are served as static files middleware in this application as well. Thus, `api/` and `frontend/` are combined together as a single standalone Asp.NET Core 10.0 application and deployed together in a single Docker container deployed on GCP Cloud Run.

# Sub-Applications

- "Tenant": Tenant administration is a key aspect of any enterprise B2B SaaS. Consult the file "specs/tenant.prd.md" for the polished product requirements document regarding tenant and user administration.

# Key Enterprise Features

✅ Multi-tenant with PostgreSQL RLS hosted on supabase.com (PostgreSQL 17.6)
✅ Auth0 OAuth2 integration for social and enterprise SSO.
✅ Multi-provider AI (OpenAI, Anthropic, Gemini, Deepseek).  
✅ AOT compilation for performance (Typescript & .NET Core 10.0).
✅ Distroless container for security (Docker).
✅ 80+ REST API endpoints (API driven frontend).
✅ Integrated frontend serving (Single Monolithic Server).
✅ SDKs in multiple languages to enable integration.
✅ Bulk endpoints for data ingestion & extraction.
✅ Complete RBAC & FGAC for access control.
✅ Separation of "personal projects", "open source collaborations" and "enterprise work" via multiple workspace with single identity.
✅ Extensive workspace level settings and global user level settings.
✅ Extensive tenant management capabilities.
✅ Data encryption in transit and at rest.
✅ Tenant sharding and per tenant encyrption keys.
✅ Customer Managed Encryption Key support.
✅ Sanitized logging.
✅ Extensive immutable audit logging.

# Instructions

## Stack

**Hybrid Model**: Single server serves both APIs and web pages
- Backend: ASP.NET Core 10.0 (Self-contained deployment)
- Frontend: Vanilla HTML + Javascript (small) + TypeScript (large) + Bootstrap 5 in the folder `./frontend/`
- Frontend Scripts: TypeScript (in the folder `./typescript/` which when compiled with Vite copies compiled files to `./frontend/`)
  - **NOTE**: For all non-trivial frontend scripting, you MUST use TypeScript. The moment any inline Javascript becomes more than 10 lines of code, you should migrate to TypeScript. It is best to write TypeSCript from the beginning.
- Database: PostgreSQL 17.6 with Dotnet EF Core. Mirgation and other SQL scripts are placed in `./sql/`.
- Image Size: ~280-300MB (runtime-deps base + runtime + frontend)
- Deployment: Self-contained (includes .NET runtime) to Cloud Run on Google Cloud Platform.
- **Swagger UI** - http://localhost:8080/swagger. 

## Folder & File Structure

+ typescript/        - All Typesript that will be compiled into Javascript goes here. All compiled output should be placed in frontend/
+ frontend/          - All frontend code (HTML, Javasript, CSS) goes here.
+ api/               - Asp.net Core 10.0 project and code for the monolith backend server. This monolith serves both static routes & APIs.
+ playwrighttests/   - .Net Core 10.0 based Playwright UI tests. 
+ integrationtests/  - .Net Core 10.0 based system integration tests.
+ unittests/         - .Net Core 10.0 based unit tests.
+ sql/               - All SQL code for database creation, modification, updates, migration should be placed here.
+ specs/             - All product specifications (both raw, product requirements etc.) will be found here.
+ playbooks/         - All generated documentation, guides, tutorials etc. relevant to product development and testing should be placed here.
+ docs/              - All product documentation relevant to customers or users or integrators should be placed here.

## Operating Style
Use a V-V-P-V-I-T-T-C loop for your core workflow. The workflow is as follows. For all software engineering tasks, you MUST strictly adhere to the following sequence:

+ **Validate (Request):** Analyze the prompt for ambiguity. Restate the core requirement and constraints to ensure alignment before acting.
+ **Verify (State):** Inspect the current codebase context. Read relevant files to confirm the environment is clean and assumptions about the existing code are correct.
+ **Plan:** Draft a concrete, step-by-step technical plan. Identify exactly which files will be modified and how.
+ **Verify (Plan):** Review the plan against project conventions (e.g., `CODING_STYLE.md`) and safety guidelines. Ensure the approach is idiomatic and low-risk.
+ **Implement Code:** Execute the planned changes using atomic, focused edits.
+ **Implement Tests:** Implement specific unit or integration tests that verify the new functionality or fix. Treat tests as a mandatory part of the implementation.
+ **Test Changes:** Execute the new tests *and* relevant regression tests. Ensure everything passes locally.
+ **Commit:** Stage the verified changes and create a commit with a concise, conventional message (e.g., `fix: ...`, `feat: ...`).

## (CRITICAL) Thinking
I urge you to think along the lines of Steve Jobs, Douglas Normal, Jonathan Ivy and others. The details are important in making sure the software and documentation we provide our users offer an amazing, consistent, thoughtful and complete end to end experience.

## Development (CRITICAL)
- You must adhere to the language conventions provided in LANGUAGE.md.
- When dealing with secrets of any kind, especially user provided secrets, always consult SECRET_HANDLING.md to understand how to architect that properly.
- Always consult CODING_STYLE when writing code. This is important for maintainability.
- Always consult GOF_PATTERNS.md when writing code. Using patterns appropriately when building code improves maintenance and understanding.
- Always consult DOCUMENTATION.md when generating internal operator or external user facing documentation.
- Always consult MIGRATIONS.md when migrating from one stack to another such as Javascript to TypeScript, Python to .NET Core etc.
- Always consult LOGGING.md so that you add appropriate logging configuration and log statements to all generated code.
- Always consult COMMENTING.md so that you add appropriate comments to all generated code.
- Always consult SECURITY_GUIDELINES.md so that you are aware of how to mitigate security concerns and do not introduce inadvertent security issues.
- Always consult FRONTEND.md when frontend code changes are involved.
- Always consult DELETION.md when adding new types of resources that users will use.
- Always consult UX_UI_GUIDELINES.md when thinking about any new capability or feature. 
- Always consult API_GUIDELINES.md when implementing new APIs.
- Always consult PERFORMANCE.md when implementing backends, frontends or APIs. It is important to keep performance in mind upfront.
- Always consult TESTING.md when you need to write tests. Having maintainable and comprehensive tests is important.
- When creating backend code, consult BACKEND.md.
- When selecting libaries for backend functionality, always consult BACKEND_LIBRARY_SELECTION.md for guidelines and DOTNETFX_SELECTION.md for pre-canned recommendations. 
- When selecting libraries for frontend functionality, always consult FRONTEND_LIBRARY_SELECTION.md for guidelines and FRONTEND_SELECTION.md for pre-canned recommendations.
- Always consult RESTABLE_RESOURCES.md for how to setup resource URLs to be restable and usable by humans.
- Always consult LITERATE_ERRORS.md for how to construct error messages to be usable and meaningful to users and operators.
- Always consult LLM_TECHNIQUES.md and NON_LLM_AIML_TECHNIQUES.md to determine the best approach for infusing any AI or ML feature. It's important to choose the right AI or ML technique instead of one-shotting everything with LLMs. Make sure to consult AIML_SECURITY.md *every time* to make sure AI or ML features especially those involving LLMs do not lead to system compromise or data exfiltration.
- When creating SDKs, consult SDKs.md.
- **When implementing access control, sharing, or permissions, always consult ACCESS_CONTROL.md.** This includes:
  - Defining new permissions and roles
  - Setting resource ownership
  - Adding permission checks to controllers
  - Integrating Share buttons in frontend
  - Writing authorization tests
- Always consult ADDITIONAL_INSTRUCTIONS.md which contain some refinements. 
- Generate a concise summary of changes for each set of changes and commit the Git code. Don't push yet.

## Local Development

### Clean
```bash
./clean.sh
```

### Build
```bash
./build.sh
```

### Test
```bash
./test.sh
```

### Run
```bash
./run.sh
```

### Deploy
```bash
./redeploy.sh
```

## Local Endpoints

After `run.sh` starts, about 1 minute later, the app should be available at `http://localhost:8080`. 
The local database is PostgreSQL. User name is `postgres` and password is `postgres`. Database is `postgres`.

# History and Status
Always keep all provided input from me to you, the agent, in the file CONVERSATION.md. Write the request + your output summary into the CONVERSATION.md file as well. This helps keep track of all refinements and changes over time. If this file already exists, also attempt to read it to understand everything that has been done so far. Leverage the `git log` to understand past changes and refinements. Use agentic markers in all generated files to guide yourself. This combination should give you almost all context about what was achieved.

Always keep the per-application progress and plans in an application specific file inside the `./specs/` directory. For example, as we are working on the *Diagrams* app, keep progress from CONVERSATION.md, your context, your history, the `git log`, bug fixes, refinements in the file `./specs/diagrams.status.md`. This makes it easier to resume sessions working on the app over time or for bug fixes etc. This is going to be shorter context than CONVERSATION.md which is quite large.

