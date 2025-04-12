# Session Bot V2

Réécriture du bot Session en Python pur, éliminant la nécessité de WebSocket et TypeScript.

## État du Projet (12/04/2025)

### Réalisé
- Structure de base du projet mise en place
- Système de plugins fonctionnel
- Client Session mock pour les tests
- Configuration Docker

### Prochaines Étapes
1. Migration des plugins existants (notamment `session_bot_phi_local`)
2. Implémentation du système de stockage sécurisé
3. Intégration avec le vrai client Session (libsession-python)

## Structure du Projet
```
session_bot_v2/
├── app/
│   ├── core/           # Composants principaux
│   ├── plugins/        # Système de plugins
│   └── storage/        # (À implémenter) Stockage sécurisé
├── docker-compose.yml
└── Dockerfile
```

## Notes de Développement
- Le mock du client Session est en place pour les tests
- Le système de plugins est basé sur une interface abstraite Python
- Prochaine session : commencer la migration des plugins existants
