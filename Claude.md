# Claude.md - LyfBits Semantic Content Store Modernization Guide

## Project Overview

This guide is based on the analysis of the LyfBits semantic content store - a comprehensive file and data object management system with filesystem-like organization, metadata extraction, and search capabilities. The original implementation used Java 8+, Maven, Spring Framework, AWS services (DynamoDB, S3, ElasticSearch), and a sophisticated infrastructure automation toolchain.

## Core Architecture Patterns Learned from Legacy Codebase

### 1. Multi-Module Maven Structure
```
source/
├── Core/           # Framework and business logic
├── Tools/          # Infrastructure automation tools
├── Website/        # Web application (WAR)
├── Objects/        # Protobuf/data objects
├── WebComponents/  # Frontend components
└── Probes/         # Health checks and monitoring
```

### 2. Environment-Based Configuration Strategy
- **DESKTOP**: Development environment with local resources and test prefixes
- **PROD**: Production environment with role-based AWS authorization
- Properties-based configuration per environment (`DESKTOP.properties`, `PROD.properties`)
- Spring XML configuration with property placeholders and environment-specific beans

### 3. Comprehensive AWS Integration Patterns
- **Bootstrap Configuration**: Centralized configuration management with environment-aware settings
- **Client Factory Pattern**: Unified AWS client creation with endpoint configuration
- **Resource Name Resolution**: Environment-aware resource naming (tables, buckets, queues)
- **Encryption at Rest**: KMS integration for data keys and blob encryption

### 4. Testing Strategy
- **Unit Tests**: JUnit for isolated component testing
- **Integration Tests**: TestNG with environment-specific resource creation
- **Base Test Classes**: Common setup with AWS client initialization
- **Environment Isolation**: DESKTOP prefix for test resources, separate from PROD

## Modernization Guidelines for New JDK 21 + Spring Boot Project

### Project Structure
```
src/
├── main/
│   ├── java/
│   │   └── com/yourcompany/yourproject/
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
│   │   └── com/yourcompany/yourproject/
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

### Configuration Management (application.yml)
```yaml
spring:
  profiles:
    active: dev
    
app:
  aws:
    region: us-west-2
    kms:
      master-key-id: ${AWS_KMS_MASTER_KEY_ID:}
  
  storage:
    s3:
      bucket-prefix: ${ENVIRONMENT:dev}
    
  search:
    enabled: true
    elasticsearch:
      host: ${ELASTICSEARCH_HOST:localhost}
      port: ${ELASTICSEARCH_PORT:9200}

---
spring:
  config:
    activate:
      on-profile: dev
      
app:
  aws:
    use-role-based-auth: false
    access-key: ${AWS_ACCESS_KEY_ID:}
    secret-key: ${AWS_SECRET_ACCESS_KEY:}
  
  database:
    table-suffix: DESKTOP

---
spring:
  config:
    activate:
      on-profile: prod
      
app:
  aws:
    use-role-based-auth: true
  
  database:
    table-suffix: PROD
```

### Core Domain Classes
```java
// Data Object (inspired by original DataObject.java)
@Entity
@Table(name = "data_objects")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DataObject {
    
    @Id
    private String objectId;
    
    @Column(nullable = false)
    private String userId;
    
    @Column(nullable = false)
    private String name;
    
    @Column(nullable = false)
    private String type;
    
    @Version
    private Long version;
    
    @Builder.Default
    @ElementCollection
    @CollectionTable(name = "data_object_tags")
    private Set<String> tags = new HashSet<>();
    
    @Lob
    private String notes;
    
    @Lob
    private byte[] data;
    
    @CreationTimestamp
    private LocalDateTime created;
    
    @UpdateTimestamp
    private LocalDateTime modified;
    
    @Builder.Default
    private Boolean deleted = false;
    
    @Column(nullable = false)
    private String parentId;
}

// Configuration class (modernized from SpringBootstrapFactory)
@Configuration
@ConfigurationProperties(prefix = "app")
@Data
public class AppConfiguration {
    
    private Aws aws;
    private Storage storage;
    private Search search;
    private Database database;
    
    @Data
    public static class Aws {
        private String region = "us-west-2";
        private boolean useRoleBasedAuth = true;
        private String accessKey;
        private String secretKey;
        private Kms kms;
        
        @Data
        public static class Kms {
            private String masterKeyId;
        }
    }
    
    @Data
    public static class Storage {
        private S3 s3;
        
        @Data
        public static class S3 {
            private String bucketPrefix;
        }
    }
    
    @Data
    public static class Search {
        private boolean enabled = true;
        private Elasticsearch elasticsearch;
        
        @Data
        public static class Elasticsearch {
            private String host = "localhost";
            private int port = 9200;
        }
    }
    
    @Data
    public static class Database {
        private String tableSuffix;
    }
}
```

### AWS Service Configuration
```java
@Configuration
@EnableConfigurationProperties(AppConfiguration.class)
public class AwsConfiguration {
    
    @Bean
    public AwsCredentialsProvider credentialsProvider(AppConfiguration config) {
        if (config.getAws().isUseRoleBasedAuth()) {
            return InstanceProfileCredentialsProvider.create();
        } else {
            return StaticCredentialsProvider.create(
                AwsBasicCredentials.create(
                    config.getAws().getAccessKey(),
                    config.getAws().getSecretKey()
                )
            );
        }
    }
    
    @Bean
    public DynamoDbClient dynamoDbClient(AwsCredentialsProvider credentialsProvider, 
                                        AppConfiguration config) {
        return DynamoDbClient.builder()
            .credentialsProvider(credentialsProvider)
            .region(Region.of(config.getAws().getRegion()))
            .build();
    }
    
    @Bean
    public S3Client s3Client(AwsCredentialsProvider credentialsProvider,
                            AppConfiguration config) {
        return S3Client.builder()
            .credentialsProvider(credentialsProvider)
            .region(Region.of(config.getAws().getRegion()))
            .build();
    }
}
```

### Service Layer Pattern
```java
// Data Object Service (inspired by DataObjectManager)
@Service
@Transactional
@RequiredArgsConstructor
@Slf4j
public class DataObjectService {
    
    private final DataObjectRepository repository;
    private final BlobStorageService blobStorageService;
    private final SearchService searchService;
    private final SecurityContext securityContext;
    
    public DataObject createObject(CreateDataObjectRequest request) {
        String userId = securityContext.getCurrentUserId();
        
        DataObject dataObject = DataObject.builder()
            .objectId(UUID.randomUUID().toString())
            .userId(userId)
            .name(request.getName())
            .type(request.getType())
            .tags(request.getTags())
            .notes(request.getNotes())
            .data(request.getData())
            .parentId(request.getParentId())
            .build();
            
        DataObject saved = repository.save(dataObject);
        
        // Async search indexing
        searchService.indexObjectAsync(saved);
        
        log.info("Created data object {} for user {}", saved.getObjectId(), userId);
        return saved;
    }
    
    public Optional<DataObject> findByIdAndUserId(String objectId, String userId) {
        return repository.findByObjectIdAndUserIdAndDeletedFalse(objectId, userId);
    }
    
    public Page<DataObject> findByUserId(String userId, Pageable pageable) {
        return repository.findByUserIdAndDeletedFalse(userId, pageable);
    }
}
```

### Testing Strategy
```java
// Integration Test Base Class (modernized from BaseIntegrationTest)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@Testcontainers
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
public abstract class BaseIntegrationTest {
    
    @Container
    protected static final PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @Container
    protected static final LocalStackContainer localstack = new LocalStackContainer(DockerImageName.parse("localstack/localstack:latest"))
            .withServices(LocalStackContainer.Service.DYNAMODB, LocalStackContainer.Service.S3);
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        
        registry.add("app.aws.endpoint.dynamodb", 
            () -> localstack.getEndpointOverride(LocalStackContainer.Service.DYNAMODB).toString());
        registry.add("app.aws.endpoint.s3", 
            () -> localstack.getEndpointOverride(LocalStackContainer.Service.S3).toString());
    }
    
    @BeforeEach
    void setUp() {
        // Initialize test data
    }
}

// Specific Integration Test
class DataObjectServiceIntegrationTest extends BaseIntegrationTest {
    
    @Autowired
    private DataObjectService dataObjectService;
    
    @Test
    @WithMockUser(username = "testuser")
    void shouldCreateAndRetrieveDataObject() {
        // Test implementation
        CreateDataObjectRequest request = CreateDataObjectRequest.builder()
            .name("Test Document")
            .type("document")
            .tags(Set.of("test", "document"))
            .data("test data".getBytes())
            .parentId("ROOT")
            .build();
            
        DataObject created = dataObjectService.createObject(request);
        assertThat(created.getObjectId()).isNotNull();
        
        Optional<DataObject> retrieved = dataObjectService.findByIdAndUserId(
            created.getObjectId(), "testuser");
        assertThat(retrieved).isPresent();
    }
}
```

### Frontend Build Configuration (Maven)
```xml
<plugin>
    <groupId>com.github.eirslett</groupId>
    <artifactId>frontend-maven-plugin</artifactId>
    <version>1.12.1</version>
    <executions>
        <execution>
            <id>install node and npm</id>
            <goals>
                <goal>install-node-and-npm</goal>
            </goals>
            <configuration>
                <nodeVersion>v18.17.0</nodeVersion>
                <npmVersion>9.6.7</npmVersion>
            </configuration>
        </execution>
        <execution>
            <id>npm install</id>
            <goals>
                <goal>npm</goal>
            </goals>
            <configuration>
                <arguments>install</arguments>
            </configuration>
        </execution>
        <execution>
            <id>webpack build</id>
            <goals>
                <goal>npm</goal>
            </goals>
            <configuration>
                <arguments>run build</arguments>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### TypeScript Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "dist/js",
    "rootDir": "src/ts"
  },
  "include": ["src/ts/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### SASS Configuration (package.json scripts)
```json
{
  "scripts": {
    "build-css": "sass src/scss:../main/resources/static/css --style compressed",
    "build-js": "tsc && webpack",
    "build": "npm run build-css && npm run build-js",
    "watch": "npm run build-css -- --watch & npm run build-js -- --watch"
  },
  "devDependencies": {
    "sass": "^1.67.0",
    "typescript": "^5.2.0",
    "webpack": "^5.88.0",
    "bootstrap": "^5.3.0"
  }
}
```

## Key Modernization Benefits

1. **Configuration**: YAML-based Spring Boot configuration replaces XML
2. **Testing**: Testcontainers for integration tests instead of requiring AWS resources
3. **Security**: Built-in Spring Security instead of custom implementations
4. **Data Access**: Spring Data JPA with modern repository patterns
5. **Build Process**: Unified Maven build with frontend integration
6. **Java 21 Features**: Records, pattern matching, virtual threads where appropriate
7. **Observability**: Built-in Spring Boot actuator endpoints
8. **DevOps**: Docker support and cloud-native patterns

## Migration Strategy

1. **Phase 1**: Set up new Spring Boot project structure
2. **Phase 2**: Migrate core domain models and business logic
3. **Phase 3**: Implement AWS integration with modern SDK v2
4. **Phase 4**: Migrate frontend to TypeScript/SASS with Bootstrap
5. **Phase 5**: Set up comprehensive testing with Testcontainers
6. **Phase 6**: Add monitoring, security, and deployment automation

This guide preserves the sophisticated patterns from your original LyfBits implementation while modernizing to current Java/Spring ecosystem standards.