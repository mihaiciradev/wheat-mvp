# AWS plan

No AWS resource has been created. Do not create one from this document. Deployment waits until the MVP measurements work locally and the owner confirms credit balance, expiration, and which services the credits cover.

## Intended shape, when approved

| Need | Choice | Why |
| --- | --- | --- |
| API and CPU vision | One small EC2 instance, stopped when idle | Matches a single FastAPI process. Avoids a cluster. |
| Images | S3 behind `ImageStore` | Keeps bytes out of the database and out of Git |
| Records | SQLite on the instance disk, or a small PostgreSQL if more than one writer appears | Start with the simpler one that the prototype already targets |
| Web | Static hosting or the same instance | Decide when the UI is more than a placeholder |
| GPU | Not planned | No benchmark shows a need |

## Rules

- No GPU instances.
- No always-on oversized machines. Prefer a stopped or scheduled instance over a idle cluster.
- No credentials in Git. Use instance roles for S3.
- Build and test the Docker or systemd command locally before launching an instance.
- Write down the expected monthly cost before applying a change, and stop if credits do not cover that service.

DJI products are not part of this plan. Aerial images, if they arrive later, are files in the same store.
