# App Layer Reference

Use this reference when designing the actual product surface around the Skill runtime.

## Role

The app layer owns:

- user interface
- input forms and upload flows
- API routes
- state persistence
- authentication and permissions
- human review
- history and trace viewing
- settings and provider config
- deployment and observability

The app should make the loop visible enough that users can trust and correct it.

## Minimum AI-Native App Surface

Avoid a generic chatbot as the default. Build a workflow surface:

1. Intake screen: user provides structured input.
2. Run screen: app shows runtime progress and tool observations.
3. Review screen: user sees output, evidence, warnings, and approval buttons.
4. History screen: previous runs, status, corrections, eval result.
5. Settings screen: provider/model, Skill version, permissions.

## API Routes

Typical routes:

```text
POST   /api/runs                 create a run
GET    /api/runs/:id             read run state and trace
POST   /api/runs/:id/approve     approve a gated action
POST   /api/runs/:id/reject      reject or request correction
POST   /api/evals/run            run eval set
GET    /api/skills               list available skills
GET    /api/skills/:id           inspect skill metadata
POST   /api/providers/test       test configured provider
```

Keep side-effectful routes behind approval and permission checks.

## Data Model

Minimum tables or collections:

```text
skills
  id
  name
  version
  skill_markdown
  references_path
  created_at

runs
  id
  skill_id
  user_id
  provider
  model
  status
  input_json
  output_json
  validation_status
  review_status
  created_at
  completed_at

tool_calls
  id
  run_id
  tool_name
  arguments_json
  result_json
  status
  created_at

reviews
  id
  run_id
  reviewer_id
  decision
  comment
  corrected_output_json
  created_at

eval_cases
  id
  skill_id
  name
  input_json
  expected_behavior
  tags

eval_results
  id
  eval_case_id
  run_id
  passed
  score
  notes
  created_at
```

For a very small app, these can start as local JSON files or SQLite. For multi-user apps, use a real database.

## UI Requirements

Show:

- input summary
- generated output
- confidence or uncertainty notes
- evidence/sources/tool observations
- validation errors
- approval state
- human correction field
- rerun/correct button
- run history

Do not hide the runtime entirely. Users need to see why the app produced an answer.

## Secrets And Provider Settings

Use environment variables or secure secret storage:

```text
MODEL_PROVIDER=deepseek
MODEL_BASE_URL=https://api.deepseek.com
MODEL_API_KEY=...
MODEL_NAME=...
```

Do not store API keys in client-side code, localStorage, logs, or exported traces.

## Permission Model

Classify tools:

| Tool type | Example | Default permission |
| --- | --- | --- |
| Read-only | search database, fetch URL, read uploaded CSV | allow after user submits run |
| Draft-only | draft email, generate report, prepare quote | allow, require review before use |
| Side effect | send email, update CRM, publish page | require explicit human approval |
| Sensitive | financial/legal/compliance conclusion | require review and evidence |

## Deployment And Observability

For first useful version:

- deploy one environment
- configure provider env vars
- log run id, provider, model, latency, validation result
- capture errors around model call, tool call, JSON validation, and approval
- provide a way to replay a run with same input and Skill version

For production:

- add auth
- rate limits
- audit logs
- cost tracking
- retries with idempotency
- alerting for provider errors
- versioned Skills and eval sets

## First Useful Version Boundary

A good V1:

- has one clear user
- accepts one structured input type
- produces one reviewable artifact
- has no autonomous external side effects
- saves history
- has at least three eval cases
- can swap provider config without rewriting app logic

