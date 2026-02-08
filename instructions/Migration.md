# Backend Migration

We are going to utilize Claude Code to migrate a backend written in Python for a web application to Asp .NET Core 10.0. We are doing this because, at this point, we have validated that conceptually the overall use of Claude Code to create a full blown enterprise SaaS is viable. The Python backend was also written by Claude Code. However, the code is not as well structured, nor does it have the readability or quality that a true, well written, well operated, high scale SaaS will need. The raw ideas we have outlined below are primarily raw instructions to guide the migration.
### General Advice

- Frameworks: Use well known frameworks for functionality over rolling your own. Well known frameworks as outlined below are well tested, actively maintained, are rich in functionality and enable rapid development over cusotm code.
- Templates: Consider using templates well. For example, the text of an email can be in code or it could be a in a file with placeholders that a template engine processes. 
- Composition over Inheritance: Prefer composition over inheritance. For example, we assemble a 'car' out of wheels, engine, chassis, steering etc. We don't need to invent an "abstract" vehicle concept and inherit from it to adhere to some weird stylistic notions. Keep it simple.
- Standard Patterns: Use standard design, integration and architecture patterns over non-standard constructs. For example, where appropriate, use the Decorator pattern. Where appropriate, use async and await methods. Where appropriate use singletons.
- Object Orientation: While we do want to avoid inheritance, that doesn't mean we shouldn't use object orientation. In this scenario, when I say object orientation, what I mean really is this idea that we "program in the domain" of the system. In other words, if there is an entity called Checklist that the User interacts with, then we might actually have a Checklist type and a User type. They might have methods that enable a checklist to be loaded, written, modified from a database, exported etc. This allows us to think about the functionaiity in that sense, versus thinking about the Checklist simply as a "data transfer object" which there is a separate set of functions such as loadChecklist, saveChecklist etc.
- Modern C#: Use modern C# effectively while maintaining readability and maintainability. There is a balance between brevity given how much syntactic sugar C# provides, readability of that brevity and maintainability when that brevity needs to be broken to include more complex functionality. Be judicious. But be wise. For example, if a Span for memory intensive operations such as caching makes sense, use it.
- Abstractions: Avoid too many abstractions. There is no need to implement for example, complex IoC if a Service Locator pattern will suffice. There is no need to create many abstract classes and interfaces if a simple class will do. 
- Context: I have found it useful in the past to include a "Context" type that more or less acts as a strongly typed propoerty bag. Over time, as additional data that is relevant nut not directly related needs to be passed in, we can pass it in the context. For example, imagine a "metrics" container that needs to be passed down through the stack that accumulates and writes the metrics out automatically. 

### C# Specific Nuances

- Prefer Native Solutions: .Net comes with an extensive standard library optimized for most general purpose use cases. Only use a specialized framework when needed preferring to use the framework capabilities first.
- Cancellation: Since the product we are building is user facing, "canceling" of long running operations may become important. When you implement logn running background operations, keep in mind that user initiated cancellation will need to be handled.
- Async & Await: C# provides asynchronous IO out of the box. Prefer to use async IO as much as possible to enable high throughout with low resource consumption.

### File Organization

- Business Logic: As far as possible keep business logic separate from data models, controllers and APis. For example, if there is an option to send an email when a checklist is completed, consider decomposing it as "Email", "Checklist" and "ChecklistEvent" (of type completed) to which a ChecklistEvetnListener subscribes, looks up any configuration, composes the Email and invokes Email.Send(). In other words, reading the code should feel like reading a book.
- Data Models: Model in the domain; keep the data model separate from the API controllers separate from the utility classes separate from the event handlers and so on.
- Queries & ORMs: Keep queries separate from code. Load the appropriate query string via lookup as needed. Parametrize it corrctly for security reasons versus using inlined SQL or other types of query expressions.
- Folder Structure: Use an appropriate folder structure. For example, a root folder with the entrypoints and basic configuration and then perhaps a models folders, a controllers folder, an utils folder, a data folder, a configuration folder and so on.

### Build & Performance

- Performance: Pay attention to performance. As a startup, we want to minimize resource usage so our compute, memory and network costs are lowered. If responses can be gzipped, do it. If requests can be encoded more efficiently do it. 
- Build: Use a framework & OS native build process. For example, for Asp.Net Core with Typescript, we might consider MSBuild for .NET builds, tsc for Typescript builds and Bash for orchestrating both. Product structured outputs that make sense in an output folder that is excluded from Git.
### Scaffolding Crud

- Avoid Magic: Frameworks like Asp.NET Core also perform a lof of magic. For example, attributes are used to signal various types of interventions via reflection for auth, validation, error handling etc. In general, we want to all code paths to understandable and debuggable by someone just using a simple debugger. So avoid magic as much as possible. It must be possible to read the code and understand the flow of logic and what is being done without a lot of context.
- Reduce Boilerplate: End to end frameworks like .NET Core tend to generate tons of unnecessary boilerplate that add unnecessary capabilities and complexity. These create confusion. Avoid this and start with the most minimal scaffolding necessary.

### Logging & Commenting

- Logging: Consult logging.md to understand how to do logging. Use a well known logging library such as serilog. Be conscious that we might need to log at different levels of granularity event at a per user level depending on the reported issue. Being able to turn on debug logs for a specific user, or request / response logging for an erratic node, or trace logging for all outgoing API calls to some other service are important considerations. Being able to turn this on dynamically via env vars, config vars, etc. is important. Of course, the primary concern right now is logging itself but in the future these will become important.
- Commenting: Comment the code extensively. Make sure every method and type is well documented. Do not document the "how" but document the why and what. For example, don't talk about how a method may implement the fibonacci series, but talk about why we felt a need to implement that like this. Document the inputs, outputs and failure modes. Document the validations performed and constraints on the inputs and outputs. Document APIs with error codes returned and what they might mean.
