# Product Infrastructure Reference

Use this reference when the AI-native app needs real product capabilities behind the UI and runtime: persistence, auth, storage, queue, cron, webhooks, and integrations.

These are not "ops" features. They are what make an app a business system.

## Product Infrastructure Layers

| Capability | Why it exists | Typical implementation |
| --- | --- | --- |
| Persistence | run history, review trail, business records, eval results | SQLite, Postgres, Firestore, D1 |
| Auth / permission | user boundary, org/team boundary, approval authority | Clerk, Supabase Auth, Auth.js, Auth0, Firebase Auth, CloudBase Auth |
| Object storage | uploaded files, generated reports, evidence packs | Supabase Storage, Cloudflare R2, Firebase Storage, Alibaba OSS, Tencent COS |
| Queue | long tasks, retries, batch work, async tool execution | Cloudflare Queues, Upstash QStash, Alibaba SMQ/MNS, Tencent SCF async/CKafka |
| Cron / scheduler | weekly tracking, report generation, reminder workflows | Vercel Cron, Cloudflare Cron Triggers, Upstash Schedules, Render Cron, CloudBase/SCF timers |
| Webhooks / integrations | receive/send events to business systems | Clerk webhooks, Supabase database webhooks, app-specific `/api/webhooks/*` routes |

## Selection Rules

- If the app only needs a local demo, start with SQLite and local files.
- If it needs users, history, approvals, or audit, use Postgres.
- If it needs uploads or generated artifacts, add object storage before deployment.
- If the model/tool run can exceed normal request time, add queue/background jobs.
- If the workflow repeats by time, add cron/scheduler.
- If another business system changes state, use webhooks instead of polling.

## International Product Infrastructure

| Platform | How to connect | Good for | Watch-outs |
| --- | --- | --- | --- |
| Supabase | `SUPABASE_URL`, anon/service keys, JS client or Postgres connection string | Postgres, Auth, Storage, Edge Functions, RLS, realtime, database webhooks | RLS must be designed; service key stays server-side; Storage objects are separate from DB backups |
| Firebase | Firebase Web/Admin SDK, project config, service account for server | Auth, Firestore, Storage, Cloud Functions, Hosting, mobile/web apps | Firestore is document DB; relational reporting can be awkward; security rules matter |
| Cloudflare | Worker bindings in `wrangler.toml` for D1/R2/KV/Queues, Cron Triggers | edge apps, D1 state, R2 files, KV config/session-like data, queues/cron | runtime differs from full Node; eventual consistency for KV-like stores |
| Vercel | env vars, Vercel Marketplace integrations, Cron Jobs, Blob/KV/Postgres integrations | Next.js product apps, preview/prod envs, simple cron, storage via integrations | persistence is via attached services; serverless limits matter for long tasks |
| Neon | `DATABASE_URL`, Vercel integration, branches, serverless driver | serverless Postgres, preview DB branches, Vercel apps | auth/storage need other providers; connection pooling/serverless driver choices matter |
| Clerk | publishable/secret keys, middleware, OAuth credentials, webhook signing secret | fast B2B/B2C auth, organizations, roles, hosted account flows | production instance, DNS, OAuth credentials, redirect URLs, webhooks must be configured |
| Auth.js | `AUTH_SECRET`, provider IDs/secrets, adapter DB if needed | app-owned open-source auth in Next.js | more wiring; you own DB adapter/session behavior |
| Auth0 | client id/secret/domain, callback/logout URLs, APIs/roles | enterprise SSO-heavy auth | heavier setup; tenants/apps/callbacks must match environments |
| Upstash | REST or SDK tokens, Redis URL, QStash token | Redis cache/rate limit, serverless queue, retries, schedules | message delivery is async; design idempotency and signing verification |

Sources:

- Supabase: https://supabase.com/docs/guides/database/overview, https://supabase.com/docs/guides/auth, https://supabase.com/docs/guides/storage
- Firebase: https://firebase.google.com/docs/auth, https://firebase.google.com/docs/firestore, https://firebase.google.com/docs/storage, https://firebase.google.com/docs/functions
- Cloudflare: https://developers.cloudflare.com/workers/platform/storage-options/, https://developers.cloudflare.com/d1/, https://developers.cloudflare.com/queues/, https://developers.cloudflare.com/workers/configuration/cron-triggers/
- Vercel: https://vercel.com/docs/storage, https://vercel.com/docs/cron-jobs, https://vercel.com/docs/environment-variables
- Neon: https://neon.com/docs/introduction, https://neon.com/docs/guides/vercel-overview
- Clerk: https://clerk.com/docs/guides/development/deployment/production, https://clerk.com/docs/guides/development/webhooks/overview
- Auth.js: https://authjs.dev/getting-started/deployment
- Upstash: https://upstash.com/docs/redis/overall/getstarted, https://upstash.com/docs/qstash/overall/getstarted, https://upstash.com/docs/qstash/features/schedules

## Domestic Product Infrastructure

| Platform | How to connect | Good for | Watch-outs |
| --- | --- | --- | --- |
| Alibaba Cloud RDS | `DATABASE_URL` to RDS PostgreSQL/MySQL, VPC/security group config | production relational persistence in China | networking/security groups and backups must be set deliberately |
| Alibaba OSS | SDK/API with endpoint, bucket, region, access credentials from env | file uploads, generated reports, evidence packages | RAM permissions, internal vs public endpoint, signed URL policy |
| Alibaba SMQ/MNS | SDK/API endpoint + access credentials; queue/topic model | async job queue, fanout, decoupling producers/consumers | visibility timeout, retries, idempotency, trace/log management |
| Alibaba Function Compute | HTTP/event functions, environment variables, triggers from OSS/SMQ/timers | scheduled jobs, webhook endpoints, lightweight event processing | serverless lifecycle and cold start; permissions via RAM |
| Tencent CloudBase | CloudBase SDK/CLI, cloud functions, database, storage, auth ecosystem | WeChat/Tencent ecosystem, integrated app backend | platform-specific conventions; watch environment separation |
| Tencent COS | SDK/API with bucket, region, secret id/key | object storage in Tencent ecosystem | permission policy and signed URL design |
| Tencent SCF / CloudBase Functions | HTTP/API Gateway/COS/timer triggers, env vars | cron, event processing, webhook receivers | timer format, retry behavior, logs, role permissions |
| Tencent EdgeOne Makers | CLI/Git deploy, Functions, KV, env/secrets | edge/static/full-stack apps, lightweight global/China edge deployment | KV is small-data/eventual-consistency style; functions runtime differs from Node server |

Sources:

- Alibaba SAE/hosting: https://www.alibabacloud.com/help/en/sae/application-deployment-overview
- Alibaba OSS: https://www.alibabacloud.com/help/en/oss/developer-reference/simple-upload-11
- Alibaba RDS PostgreSQL: https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-postgresql/getting-started
- Alibaba SMQ/MNS: https://www.alibabacloud.com/help/en/mns/product-overview/what-is-mns
- Alibaba Function Compute: https://www.alibabacloud.com/help/en/functioncompute/fc-2-0/user-guide/manage-functions
- Tencent CloudBase Run: https://cloud.tencent.com/document/product/1243/77197
- Tencent CloudBase Functions: https://docs.cloudbase.net/cloud-function/introduce
- Tencent COS: https://cloud.tencent.com/document/product/436
- Tencent SCF env/triggers: https://cloud.tencent.com/document/product/583/30228, https://cloud.tencent.com/document/product/583/9708
- Tencent EdgeOne Makers: https://pages.edgeone.ai/document/deployment-overview, https://pages.edgeone.ai/document/pages-functions-overview, https://pages.edgeone.ai/document/kv-storage

## Implementation Patterns

### Pattern A: Next.js + Supabase

Use when you want one provider for Postgres, Auth, Storage, and Edge Functions.

Connect:

```text
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=
```

Build:

- `runs`, `tool_calls`, `reviews`, `eval_cases`, `eval_results` tables.
- RLS policies for user/org data.
- Storage bucket for uploaded inputs and generated artifacts.
- Database webhook or Edge Function only when a row change should trigger external work.

### Pattern B: Next.js + Clerk + Neon + S3-compatible storage

Use when auth should be polished and database should stay plain Postgres.

Connect:

```text
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
CLERK_WEBHOOK_SECRET=
DATABASE_URL=
STORAGE_ENDPOINT=
STORAGE_ACCESS_KEY_ID=
STORAGE_SECRET_ACCESS_KEY=
```

Build:

- sync Clerk users/orgs into local DB through webhooks.
- use DB roles/permissions in app code.
- store file metadata in Postgres and file bytes in object storage.

### Pattern C: Cloudflare Workers + D1 + R2 + Queues + Cron

Use when the app is edge-first and has modest relational needs.

Connect through bindings:

```toml
[[d1_databases]]
binding = "DB"

[[r2_buckets]]
binding = "BUCKET"

[[queues.producers]]
binding = "JOB_QUEUE"

[triggers]
crons = ["0 * * * *"]
```

Build:

- API routes as Workers/Pages Functions.
- D1 for run state.
- R2 for uploads/artifacts.
- Queues for long jobs.
- Cron Triggers for scheduled workflows.

### Pattern D: Domestic Container App + RDS + OSS/COS + Function/Queue

Use when users/customers are China-facing.

Connect:

```text
DATABASE_URL=
OSS_OR_COS_BUCKET=
OSS_OR_COS_REGION=
ACCESS_KEY_ID=
ACCESS_KEY_SECRET=
QUEUE_ENDPOINT=
```

Build:

- container app on Alibaba SAE or Tencent CloudBase Run.
- RDS/Postgres for relational state.
- OSS/COS for files.
- Function Compute/SCF for timer/webhook/event jobs.
- SMQ/MNS or cloud queue for async processing when needed.

## AI-Native Product Infrastructure Requirements

For Skill-to-App work, store:

- source Skill version
- run input
- compiled instruction hash
- model provider/model
- tool calls and observations
- output JSON
- validation result
- human review decision
- correction notes
- eval result

This is the minimum infrastructure that lets the app improve instead of merely generate.

