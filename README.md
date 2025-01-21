# Deploying an App on Lambda and DynamoDB for Banking Transaction Notifications

## [Probématique](probematique.md)

![](<Architecture App.png>)


## Services:

### Network
- **API GATEWAY**: Enables you to create, publish, maintain, and secure APIs at scale. It facilitates request routing to backend services, manages authentication and access control, and enables integration of features such as caching and performance monitoring. AWS API Gateway simplifies the development and operation of APIs for cloud-based applications.

### Security
- **SECRET MANAGER**: A service that securely stores and manages secrets (such as passwords and API keys).
- **Identity and Access Management (IAM)**: Defines what users and roles can do with AWS resources.
- **Role**: An IAM role is an entity that defines a set of permissions to perform actions on AWS resources. Unlike users, roles are not associated with a specific person or account, but can be assumed by AWS services, users, or applications. Roles are often used to grant temporary permissions.
- **Permission**: Define what users and roles can do with AWS resources.

### Storage
- **S3 (Simple Storage Service)**: Object storage service for storing and retrieving data at any time.

### Database
- **DynamoDB**: Fully managed NoSQL database that delivers fast, predictable performance at any scale, with a flexible data model and low latency.

### Compute
- **Lambda**: Serverless compute service that executes code in response to events and automatically manages scale, allowing you to pay only for execution time.

### Email
- **SES (Simple Email Service)**: Scalable email service that makes sending and receiving emails easy and inexpensive, often used for notifications and marketing campaigns.

### Event and Application Integration
- **EventBridge**: Enables you to connect different applications and services by facilitating event management and routing, thus promoting an event-driven architecture in the cloud

### Resource Monitoring and Management
- **CLOUDWATCH**: Monitoring service that collects and tracks metrics, logs, and events for AWS resources.
- **Logs Groups**: Groups logs for centralized management and analysis.

## [Process of Implementing Banking Notifications with AWS](process.md)
