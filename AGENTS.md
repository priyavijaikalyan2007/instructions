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

## Development
- Always consult LOGGING.md so that you add appropriate logging configuration and log statements to all generated code.
- Always consult COMMENTING.md so that you add appropriate comments to all generated code.
- Always consult FRONTEND.md when frontend code changes are involved.
- Always consult DELETION.md when adding new types of resources that users will use.
- Always consult UX_UI_GUIDELINES.md when thinking about any new capability or feature. 
- Always consult API_GUIDELINES.md when implementing new APIs.
- Always consult PERFORMANCE.md when implementing backends, frontends or APIs. It is important to keep performance in mind upfront.
- When creating backend code, consult BACKEND.md.
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

# History
Always keep all provided input from me to you, the agent, in the file CONVERSATION.md. Write the request + your output summary into the CONVERSATION.md file as well. This helps keep track of all refinements and changes over time. If this file already exists, also attempt to read it to understand everything that has been done so far. Leverage the `git log` to understand past changes and refinements. Use agentic markers in all generated files to guide yourself. This combination should give you almost all context about what was achieved.

