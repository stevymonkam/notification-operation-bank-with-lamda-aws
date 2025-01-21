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