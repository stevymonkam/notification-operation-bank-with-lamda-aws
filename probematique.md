### **Amélioration des notifications de transactions bancaires : Déploiement d’une application sur AWS Lambda et DynamoDB**


**Problématique :**
Avant l’implémentation de notre solution, le service **EAZYCard** rencontrait un défi majeur en matière de notification des utilisateurs finaux. Bien que la banque notifiait les transactions à l’entreprise via une application dédiée, ces notifications étaient exclusivement accessibles à l’équipe interne de gestion, empêchant ainsi les utilisateurs finaux de recevoir des informations cruciales en temps réel. Cette **manque de réactivité** dans les notifications de transactions bancaires posait des problèmes de transparence et de sécurité, tout en nuisant à l’expérience client. 

**Solution proposée :**
Pour résoudre ce problème, nous avons conçu et déployé une solution robuste basée sur **AWS Lambda** et **DynamoDB**, offrant une architecture sans serveur et hautement scalable qui permet de notifier instantanément les utilisateurs finaux lors de chaque transaction bancaire effectuée. 

En exploitant **AWS Lambda**, nous avons permis une gestion des notifications en **temps réel**, capable de s’adapter automatiquement à un volume croissant de transactions, tout en réduisant considérablement les coûts opérationnels grâce à la facturation à l’usage. **DynamoDB**, une base de données NoSQL performante et scalable, permet de stocker et traiter rapidement les informations des transactions pour garantir des notifications instantanées à chaque utilisateur concerné.

### **Impact de la solution :**
- **Accessibilité des notifications en temps réel** : Les utilisateurs finaux reçoivent désormais des notifications instantanées de leurs transactions, améliorant ainsi la transparence et l’engagement client.
- **Scalabilité** : Que ce soit pour des milliers ou des millions de transactions par jour, la solution s’adapte automatiquement à la demande sans perte de performance, assurant la fiabilité du service à long terme.
- **Réduction des coûts** : L’architecture sans serveur permet de **réduire les coûts** en ne payant que pour les ressources effectivement utilisées, sans investissements en infrastructure dédiée.
- **Amélioration de la sécurité** : Les notifications instantanées permettent aux utilisateurs de détecter plus rapidement toute activité suspecte sur leurs comptes, renforçant ainsi la sécurité des transactions.
- **Maintenance simplifiée** : L’utilisation d’AWS Lambda réduit la charge de maintenance, car il n’y a pas de gestion de serveur ou d’infrastructure complexe à maintenir.
