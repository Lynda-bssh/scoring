# Scoring
## Projet OpenClassroom parcours Data Scientist

## Description du projet
L'organisme de prêt "Prêt à dépenser" souhaite mettre en place une interface à destination des conseillers clientèle, afin de les aider à décider d'accorder ou non un prêt à un client donné.
Dans cette perspective, il s'agit de mettre en place un modèle de scoring permettant de décider, en fonction des informations connues du client, s'il existe un risque suffisamment fort d'insolvabilité pour refuser le prêt.
Il doit être tenu compte du fait que le coût d'un prêt accordé à un "mauvais payeur" est significativement plus grand (10 fois) que le coût d'un prêt refusé à un "bon payeur".


az webapp config set --resource-group <projet_7_rg> --name <my-app-ascoring> --startup-file "<0454dfb8-7cbd-4653-8010-9f6d59d08ea8>"