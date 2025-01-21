# Déploiement d’une App sur Lambda et DynamoDB pour des notifications de transaction bancaires

## [Probématique](probematique.md)

![](<Architecture App.png>)

## Services :

### Réseau
- **API GATEWAY** : permet de créer, publier, maintenir et sécuriser des API à grande échelle. Il facilite le routage des requêtes vers des services backend, gère l'authentification et le contrôle d'accès, et permet d'intégrer des fonctions comme la mise en cache et la surveillance des performances. AWS API Gateway simplifie le développement et l'exploitation d'API pour les applications basées sur le cloud.

### Sécurité
- **SECRET MANAGER** : Service qui permet de stocker et de gérer les secrets (comme les mots de passe et les clés API) de manière sécurisée.
- **IAM (Identity and Access Management)** : Définir ce que les utilisateurs et les rôles peuvent faire avec les ressources AWS.
  - **Rôle** : Un rôle IAM est une entité qui définit un ensemble de permissions pour effectuer des actions sur des ressources AWS. Contrairement aux utilisateurs, les rôles ne sont pas associés à une personne ou un compte spécifique, mais peuvent être assumés par des services AWS, des utilisateurs ou des applications. Les rôles sont souvent utilisés pour accorder des permissions temporaires.
  - **Permission** : Définir ce que les utilisateurs et les rôles peuvent faire avec les ressources AWS.
 
### Stockage
- **S3 (Simple Storage Service)** : Service de stockage d'objets pour stocker et récupérer des données à tout moment.

### Base de données
- **DynamoDB** : Base de données NoSQL entièrement gérée qui offre des performances rapides et prévisibles à n'importe quelle échelle, avec un modèle de données flexible et une latence faible.

### Calcul
- **Lambda** : Service de calcul sans serveur qui exécute du code en réponse à des événements et gère automatiquement l'échelle, permettant de payer uniquement pour le temps d'exécution.

### Messagerie
- **SES (Simple Email Service)** : Service de messagerie évolutif qui permet d'envoyer et de recevoir des e-mails facilement et à faible coût, souvent utilisé pour les notifications et les campagnes marketing.

### Evenement et d'intégration d'applications
- **EventBridge** : Permet de relier différentes applications et services en facilitant la gestion et le routage des événements, favorisant ainsi une architecture orientée événements dans le cloud

### Surveillance et Gestion des Ressources
- **CLOUDWATCH** : Service de surveillance qui collecte et suit les métriques, les journaux, et les événements pour les ressources AWS.
  - **Logs Groups** : Regroupe les journaux pour une gestion et une analyse centralisées.

## [Processus d'Implémentation des Notifications d'Opérations Bancaires avec AWS](process.md)


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
