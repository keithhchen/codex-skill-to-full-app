# Deployment Reference

Use this reference when the app needs to run outside the developer machine.

Deployment is the operating path: build, configure, ship, monitor, roll back. Product infrastructure is covered separately in `product-infrastructure.md`.

## Deployment Checklist

- Runtime: Node/Python version, package manager, build command, start command.
- Env/secrets: model key, provider base URL, database URL, auth secrets, storage credentials.
- Build artifact: static output, serverless functions, container image, or long-running server.
- CI/CD: Git push, CLI deploy, Docker image, or platform pipeline.
- Environments: development, preview/staging, production.
- Network: domain, HTTPS, CORS, OAuth callback URLs, webhook URLs.
- Health: `/healthz`, `/api/providers/test`, `/api/db/test`.
- Logs: build logs, runtime logs, model/tool validation errors.
- Rollback: prior deployment, image tag, or platform rollback.

## Docker

Add Docker when:

- deploying to container platforms
- runtime dependencies need pinning
- Python/Node/native dependencies mix
- the target platform is Railway/Render/Fly/Alibaba SAE/Tencent CloudBase Run

Minimum Node Dockerfile:

```Dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

Minimum Python/FastAPI Dockerfile:

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Rules:

- add `.dockerignore`
- never bake secrets into image
- read `PORT` from env when platform supplies it
- keep lockfiles committed
- include a health route

Sources:

- https://docs.docker.com/guides/nodejs/
- https://docs.docker.com/reference/dockerfile/
- https://docs.docker.com/build/building/variables/

## International Deployment Platforms

| Platform | Deploy method | Integration style | Best for | Watch-outs |
| --- | --- | --- | --- | --- |
| Vercel | Git import, CLI `vercel --prod`, Drop, deploy hooks, REST API | framework detection, serverless/functions, env per local/preview/prod, marketplace storage, cron | Next.js/front-end-heavy apps, previews, fast demos | external persistence; serverless duration/runtime limits; long jobs need queue/workflow |
| Cloudflare Pages/Workers | Git, direct upload, C3/Wrangler CLI | Pages Functions/Workers, bindings for D1/R2/KV/Queues, Cron Triggers, edge env/secrets | edge-first apps, static + functions, global delivery | Node compatibility differs; data products are bindings, not normal env URLs |
| Netlify | Git deploy, Netlify CLI/API | static hosting, Functions, Scheduled Functions, env variables | frontend apps with simple functions and cron | less natural for long-running server apps |
| Railway | GitHub/autodeploy, CLI, Dockerfile/Nixpacks/Railpack | services, variables, managed Postgres/Redis, volumes, health checks, domains | classic web services, containers, simple full-stack backend | cost visibility and service topology matter |
| Render | Git deploy, Docker/native build, Blueprint `render.yaml` | Web Services, private services, background workers, cron jobs, managed Postgres, env groups | Heroku-like apps, Docker apps, background workers | free/cold-start and region limits; cron as separate service |
| Fly.io | `fly launch`, `fly deploy`, Dockerfile + `fly.toml` | Machines/VM-style deployment, secrets, volumes, services, release commands | containerized apps needing a real server model | more infra concepts than Vercel/Render |
| Firebase Hosting/App Hosting | Firebase CLI, GitHub integration | Hosting, App Hosting, Cloud Functions, Firestore/Auth/Storage integration | Firebase-native apps, mobile/web products | NoSQL-first unless using SQL Connect; Google ecosystem assumptions |

Sources:

- Vercel deployments/env/cron/storage: https://vercel.com/docs/deployments, https://vercel.com/docs/environment-variables, https://vercel.com/docs/cron-jobs, https://vercel.com/docs/storage
- Cloudflare Pages/Workers: https://developers.cloudflare.com/pages/, https://developers.cloudflare.com/workers/runtime-apis/bindings/
- Netlify functions/scheduled/env: https://docs.netlify.com/build/functions/get-started/, https://docs.netlify.com/build/functions/scheduled-functions/, https://docs.netlify.com/build/functions/environment-variables/
- Railway deployments/variables: https://docs.railway.com/deployments/reference, https://docs.railway.com/variables
- Render services/Docker/cron/Postgres: https://render.com/docs/web-services, https://render.com/docs/docker, https://render.com/docs/cronjobs, https://render.com/docs/postgresql-creating-connecting
- Fly.io: https://fly.io/docs/reference/fly-launch/, https://fly.io/docs/launch/deploy/, https://fly.io/docs/reference/configuration/, https://fly.io/docs/languages-and-frameworks/dockerfile/
- Firebase: https://firebase.google.com/docs/hosting, https://firebase.google.com/docs/functions

## Domestic Deployment Platforms

| Platform | Deploy method | Integration style | Best for | Watch-outs |
| --- | --- | --- | --- | --- |
| Alibaba Cloud SAE | code package or container image, ACR image deploy, console/toolkit | managed app hosting, env/config maps, logs, scaling, monitoring | Java/Node/Python containerized web apps in Alibaba Cloud | VPC, image registry, RAM permissions, domain/ICP path |
| Alibaba Function Compute | console/CLI/API, custom container or runtime, HTTP/event function | HTTP triggers, timers, OSS/SMQ/EventBridge integrations, env vars | webhook receivers, scheduled jobs, event processors | serverless lifecycle, cold starts, permissions |
| Tencent CloudBase Run | local code deploy, image deploy, CloudBase CLI `tcb cloudrun deploy` | container service, env vars, PORT convention, domain/log config | lightweight container web apps, Tencent/WeChat ecosystem | stateless service requirement; platform-specific deployment flow |
| Tencent CloudBase Functions / SCF | console/CLI, function upload, triggers | HTTP/API Gateway/COS/timer triggers, env vars, logs | cron, webhook, file-event processing | trigger config, retry policy, role permissions |
| Tencent EdgeOne Makers | Git/CLI deploy, folder/zip upload | Pages/Makers Functions, KV, env/secrets, edge deployment | static/full-stack edge apps, Vercel/Cloudflare-like frontends in Tencent ecosystem | KV/eventual consistency; runtime constraints; newer platform surface |
| Huawei CodeArts Deploy | pipeline/deployment tasks | deployment orchestration across hosts, containers, serverless | enterprise CI/CD where Huawei Cloud is already standard | more deployment orchestration than lightweight app hosting |

Sources:

- Alibaba SAE: https://www.alibabacloud.com/help/en/sae/application-deployment-overview
- Alibaba SAE env/config maps: https://www.alibabacloud.com/help/en/sae/manage-and-use-configuration-items-k8s-configmap
- Alibaba Function Compute: https://www.alibabacloud.com/help/en/functioncompute/fc-2-0/user-guide/manage-functions, https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/creating-a-web-function
- Tencent CloudBase Run: https://cloud.tencent.com/document/product/1243/77197, https://docs.cloudbase.net/run/develop/developing-guide, https://docs.cloudbase.net/run/develop/languages-frameworks/next
- Tencent CloudBase Functions/SCF: https://docs.cloudbase.net/cloud-function/introduce, https://cloud.tencent.com/document/product/583/30228, https://cloud.tencent.com/document/product/583/9708
- Tencent EdgeOne Makers: https://pages.edgeone.ai/document/deployment-overview, https://pages.edgeone.ai/document/pages-functions-overview, https://pages.edgeone.ai/document/edgeone-cli, https://www.tencentcloud.com/document/product/1145/62764
- Huawei CodeArts Deploy: https://www.huaweicloud.com/product/clouddeploy.html

## Platform Selection

Use these defaults:

- Next.js product app: Vercel first, Cloudflare/EdgeOne if edge or China path matters.
- Full-stack server with Postgres: Railway or Render internationally; SAE or CloudBase Run domestically.
- Python/FastAPI AI app: Docker + Railway/Render/Fly internationally; Docker + SAE/CloudBase Run domestically.
- Static/marketing plus light functions: Vercel, Netlify, Cloudflare Pages, EdgeOne Makers.
- Scheduled/background work: platform cron for simple jobs; queue/workflow service for long or retry-heavy jobs.

## Deployment Artifacts To Add

Depending on stack, add:

```text
.env.example
Dockerfile
.dockerignore
vercel.json
wrangler.toml
render.yaml
fly.toml
railway.json or railway service settings
edgeone.json
health route
provider test route
database migration command
eval command
```

## AI-Native Deployment Checks

Before marking deployed:

- health route works
- provider test route works
- database connection works
- auth callback URL matches deployed domain
- webhook URL is public and signature-verified
- cron/queue target endpoint is deployed
- eval smoke test passes against production-like env
- logs include run id, model/provider, tool count, validation status, review status
- rollback path is known

