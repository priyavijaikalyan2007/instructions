# Introduction

The backend services will always be written in Java for all application layer, business logic, data layer, ORM, background processing and more. This file provides instructions for how to setup a backend service whether it is API only or it is API + web UI. Maven will be the preferred build tool and Eclipse will be the preferred IDE. The following sections provide instructions on how to setup the backend project structure. Project hosti
## Setup

### Environment-Based Configuration Strategy

Software, especially web services, undergo promotions through multiple levels. For example, from the local development environment to a CI environment, then to a staging environment and finally to a production environment.
Configuration such as key names, table names, connection strings, component wiring and more depend on the environment. To enable such a setup, we will use a properties-based configuration which is per environment. Typically, these will be named `DESKTOP.properties`, `TEST.properties`, `STAGING.properties` and `PROD.properties`. Resources might in fact even be named with the prefix of the environment name so that there can be no ambiguity between the resources targeted even if keys were accidentally shared between the different environments.
 
- **DESKTOP**: Development environment with local resources and test prefixes
- **PROD**: Production environment with role-based AWS authorization

### Inversion of Control with Spring

We will use a Spring YAML configuration for managing inversion of control with property placeholders and environment-specific beans.

### Comprehensive AWS Integration Patterns

- **Bootstrap Configuration**: Centralized configuration management with environment-aware settings.
- **Client Factory Pattern**: Unified AWS client creation with endpoint configuration.
- **Resource Name Resolution**: Environment-aware resource naming (tables, buckets, queues).
- **Encryption at Rest**: KMS integration for data keys and blob encryption.

### Testing Strategy

- **Unit Tests**: JUnit for isolated component testing
- **Integration Tests**: TestNG with environment-specific resource creation.
- **Base Test Classes**: Common setup with AWS client initialization.
- **Environment Isolation**: Environment prefix for test resources, separate from production. For example, the table Account will be named `DESKTOPAccount` in local testing while in production it will be named `PRODAccount`.

### Project Structure for Each Service

```
src/
├── main/
│   ├── java/
│   │   └── com/outcrop/yourproject/
│   │       ├── config/           # Spring configuration
│   │       ├── controller/       # REST controllers
│   │       ├── service/          # Business logic
│   │       ├── repository/       # Data access
│   │       ├── model/           # Domain objects
│   │       ├── dto/             # Data transfer objects
│   │       ├── infrastructure/   # AWS, external integrations
│   │       └── security/        # Authentication/authorization
│   └── resources/
│       ├── application.yml      # Main configuration
│       ├── application-dev.yml  # Development profile
│       ├── application-prod.yml # Production profile
│       └── static/             # Frontend assets
├── test/
│   ├── java/
│   │   └── com/outcrop/yourproject/
│   │       ├── unit/           # Unit tests
│   │       ├── integration/    # Integration tests
│   │       └── testcontainers/ # Container-based tests
│   └── resources/
└── frontend/                   # TypeScript/SASS assets
    ├── src/
    │   ├── ts/                # TypeScript files
    │   └── scss/              # SASS stylesheets
    └── dist/                  # Built frontend assets
```

Note that `yourcompany` will always be `outcrop` and `yourproject` will depend on the main project name which will be found in the file `project.name` in the root of the Git repository.

### Maven Configuration (pom.xml)
```xml
<properties>
    <java.version>21</java.version>
    <spring-boot.version>3.2.0</spring-boot.version>
    <lombok.version>1.18.30</lombok.version>
    <testcontainers.version>1.19.0</testcontainers.version>
    <typescript.maven.plugin.version>1.1</typescript.maven.plugin.version>
    <sass.maven.plugin.version>3.7.2</sass.maven.plugin.version>
</properties>

<dependencies>
    <!-- Core Spring Boot -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    
    <!-- AWS SDK v2 -->
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>bom</artifactId>
        <version>2.21.0</version>
        <type>pom</type>
        <scope>import</scope>
    </dependency>
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>dynamodb</artifactId>
    </dependency>
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>s3</artifactId>
    </dependency>
    
    <!-- Lombok for boilerplate reduction -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>${lombok.version}</version>
        <scope>provided</scope>
    </dependency>
    
    <!-- Testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-bom</artifactId>
        <version>${testcontainers.version}</version>
        <type>pom</type>
        <scope>import</scope>
    </dependency>
</dependencies>
```
