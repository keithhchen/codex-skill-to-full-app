---
name: skill-to-full-app
description: Use when Codex needs to transform a portable Skill, SKILL.md, agent workflow, business SOP, or domain behavior spec into a real AI-native full app. Use for requests such as turning a skill into an app, building a provider-agnostic agent runtime, designing Skill-to-App architecture, converting business judgment into an app with tools/state/evals/human review, or implementing an app over public OpenAI-compatible LLM services. Covers client layer, runtime layer, app layer, product infrastructure, deployment, LLM provider selection, structured output, tool calling, state, approvals, evals, and traces.
---

# Skill To Full App

## Core Principle

Treat the source Skill as a portable behavior spec, not as a one-shot prompt. Build an AI-native app around it: model client, runtime loop, tools, state, validation, human review, evals, traces, and product UI.

Do not collapse the app into a single API call unless the user explicitly asks for a throwaway prototype. A full app must own the runtime around the model.

## Responsibilities

- Inspect the target project and identify which layers already exist: client layer, runtime layer, app framework, product infrastructure, provider config, review flow, evals, and deployment setup.
- Build out missing layers needed for a working vertical slice. Do not assume the runtime already exists.
- If provider credentials are not available, implement env-var based configuration, a provider health-check route or script, and clear run instructions; do not hardcode secrets.
- Default to public OpenAI-compatible model services.
- Default to provider-agnostic architecture: `baseURL`, `apiKey`, `model`, `response_format`, `tools`, and a thin adapter for provider differences.
- Use structured output and tool calling as baseline capabilities.
- Preserve the source Skill as the behavioral core; do not bury its rules inside scattered UI copy or ad hoc prompts.

## Reference Map

Load references only when needed:

- `references/client-layer.md`: choose or implement OpenAI SDK, Vercel AI SDK, LiteLLM, or a custom OpenAI-compatible model client.
- `references/runtime-layer.md`: choose or implement custom runtime, OpenAI Agents SDK, LangGraph, Google ADK, PydanticAI, LlamaIndex Workflows, or Microsoft Agent Framework.
- `references/app-layer.md`: design UI, API routes, data model, auth, secrets, review flows, traces, deployment, and observability.
- `references/product-infrastructure.md`: build or integrate persistence, auth/permissions, object storage, queues, cron/schedulers, webhooks, product integrations, and lightweight domestic/international backend services.
- `references/deployment.md`: build deployment path: Docker, env/secrets, CI/CD, preview/prod environments, domains, HTTPS, health checks, logs, rollback, and domestic/international hosting choices.
- `references/llm-providers.md`: configure public OpenAI-compatible providers such as DeepSeek, Kimi/Moonshot, Z.AI/GLM, and Qwen/DashScope.

Optional validation assets:

- `evals/trigger-evals.json`: examples that should or should not trigger this skill.
- `evals/output-evals.json`: expected qualities for Skill-to-App plans.
- `scripts/audit-app-plan.py`: deterministic checklist for reviewing an architecture plan or final summary.

## Workflow

### 1. Extract The Behavior Spec

Start from the source Skill, SKILL.md, SOP, or user workflow. Extract:

- Job: the one business task this app performs.
- Trigger: when the behavior should run.
- User: who uses the app.
- Inputs: required fields, files, URLs, records, or context.
- Outputs: structured artifact, decision, draft, report, ranking, or action plan.
- Domain rules: how good output is judged.
- Failure modes: bad data, missing fields, uncertainty, hallucination risks, compliance risks.
- Human review: what a person must approve before side effects.
- Eval cases: happy path, bad case, edge case, regression case.

If these are missing, first produce a short Skill hardening pass before app design.

### 2. Define The First Useful Version

Compress the app to one observable workflow:

```text
When [user] provides [input], the app runs [skill behavior], uses [tools/context],
produces [structured output], asks human to review [risk/quality point],
and succeeds when [observable signal].
```

Reject broad platform framing until this sentence is concrete.

### 3. Design The AI-Native Runtime Contract

Define the runtime boundary before writing UI code:

- Input schema: what the app accepts.
- Output schema: what the model must return.
- Tool contracts: tools the model may call, arguments, return shape, and permission level.
- State: what persists across runs.
- Review gates: what must stop for human approval.
- Trace: what gets logged for debugging.
- Evals: what test cases prove the Skill improves behavior.

The app should have a visible loop:

```text
Intent -> Skill Context -> Runtime Plan -> Tool Calls -> Structured Output
-> Validation -> Human Review -> Correction -> Trace/Eval -> Better Artifact
```

### 4. Select Layers

Pick the smallest stack that supports the runtime contract.

Use these defaults before offering a menu:

- TypeScript web app: Next.js or existing repo framework, Vercel AI SDK or OpenAI SDK client, custom loop first, Postgres if multi-user, object storage only if files exist.
- Python-heavy app: FastAPI, OpenAI-compatible client, custom loop or PydanticAI, Postgres for shared state, Docker for deployment.
- Stateful/multi-step workflow: LangGraph if transitions and human gates are explicit; OpenAI Agents SDK when handoffs, guardrails, sessions, and tracing are central.
- RAG/document-heavy app: LlamaIndex Workflows plus Postgres/object storage as needed.
- China-facing deployment: container app on Alibaba SAE or Tencent CloudBase Run, RDS/Postgres, OSS/COS, and domestic auth/integration choices.
- Frontend-heavy international deployment: Vercel or Cloudflare, with product infrastructure selected separately.

Only expand to other options when repo constraints, target users, or deployment environment justify it.

Client layer:

- Use OpenAI SDK for a simple OpenAI-compatible backend client.
- Use Vercel AI SDK for TypeScript / Next.js apps with streaming UI and structured output.
- Use LiteLLM when the organization wants one internal model gateway.

Runtime layer:

- Use a custom loop when the workflow has 1-3 tools and the loop should stay transparent.
- Use OpenAI Agents SDK when tools, handoffs, guardrails, sessions, and tracing matter.
- Use LangGraph when state, branching, retries, or human-in-the-loop gates are central.
- Use Google ADK when building a fuller agent framework or multi-agent pattern.
- Use PydanticAI when typed Python validation is the center of the app.
- Use LlamaIndex Workflows when RAG and document workflows dominate.

App layer:

- Use the existing app framework in the repo when present.
- For new TypeScript web apps, prefer a simple Next.js or Vite app only if the project already supports it.
- For Python-heavy teams, prefer FastAPI plus a simple frontend.
- Keep the first app surface narrow: intake, run, review, history, settings.

Product infrastructure layer:

- Add persistence when the app needs run history, user state, review trails, eval cases, or business records.
- Add auth/permission when output, history, uploaded files, approvals, or provider settings are user-specific.
- Add object storage when the app accepts uploads or generates durable files.
- Add queue/background jobs when runtime steps can exceed request time or need retries.
- Add cron/scheduler when the workflow repeats on a calendar.
- Add webhooks/integrations when business systems must push or receive events.

Deployment layer:

- Build or update the deployment path needed to run the app outside the developer machine.
- Add Docker when the target platform expects containers or runtime dependencies need to be pinned.
- Add env/secrets, CI/CD, preview/prod separation, custom domain, HTTPS, health checks, logs, and rollback when the app is meant to be shared.
- Keep deployment lightweight for V1, but make secrets, state, and recovery explicit.

Load the relevant reference files before making implementation choices.

### 5. Preserve Skill As A First-Class Artifact

Store the Skill text separately from the app code:

- `skills/<skill-name>/SKILL.md`
- `skills/<skill-name>/references/*`
- or a database-backed equivalent for editable skills.

The runtime should compile the Skill into model instructions at run time. Do not duplicate the same rules across route handlers, UI components, and tests.

### 6. Implement A Vertical Slice

Build one end-to-end path before adding breadth:

1. A user submits input.
2. The backend loads the Skill.
3. The runtime builds messages, tools, schemas, and state.
4. The model returns structured output and optional tool calls.
5. The runtime executes tools and appends tool results.
6. The runtime validates final JSON.
7. The UI shows output, evidence, warnings, and approval controls.
8. The app stores run trace, output, review, and correction.
9. One eval compares baseline model behavior with Skill-guided behavior.

### 7. Add Runtime Signals

Every AI-native app needs signals the agent can use to improve:

- schema validation pass/fail
- tool execution results
- missing-field warnings
- confidence or uncertainty tags
- source/evidence links
- human edits
- approval/rejection status
- eval score
- regression history

If there is no signal, the app is just a text generator.

### 8. Test Like A Runtime, Not Like A Prompt

Run tests at four levels:

- Baseline test: same input without Skill vs with Skill.
- Schema test: output validates against expected shape.
- Tool test: tool calls use correct arguments and tool outputs affect the final answer.
- Review test: irreversible or high-risk actions stop for human approval.
- Regression test: known bad cases stay fixed.

Do not mark the app done because the first demo looks good. Mark it done when repeated runs produce valid output and visible traces explain what happened.

If the output is a plan or design document, run:

```bash
python3 skill-to-full-app/scripts/audit-app-plan.py path/to/plan.md
```

Use the result to patch missing layers before presenting the final answer.

## Anti-Patterns

- A single `/chat` endpoint with the Skill pasted into a prompt and no state.
- A response that only recommends platforms without implementing missing layers.
- No output schema.
- No tool execution loop.
- No human approval for external actions.
- No trace of prompts, tool calls, validation, or review.
- No eval cases.
- Provider-specific code scattered throughout the app.
- Skill rules duplicated in UI text, route handlers, and tests.
- A broad "AI platform" scope before one first useful version works.

## Deliverables

When using this skill, produce or implement:

- source Skill hardening notes, if needed
- first useful version statement
- architecture plan across client/runtime/app/provider layers
- runtime contract: schemas, tools, state, approval gates, evals
- implementation of one vertical slice, including missing client, runtime, app, product infrastructure, provider config, trace, review, eval, and deployment pieces as needed
- provider configuration with env vars
- deployment configuration, such as Dockerfile, platform config, env examples, migrations, health check, or deploy notes as appropriate
- tests/evals for baseline, schema, tools, review, and bad cases
- run instructions and remaining production risks

Final responses should summarize the layer choices, changed files, how to run, and which tests/evals passed.

## Quality Bar

A completed Skill-to-App result must answer these questions concretely:

- What behavior from the source Skill became the app's behavioral core?
- What is the first useful version?
- Which client/runtime/app/product-infra/deployment/provider layers were used?
- What did the app build, not merely assume?
- What state persists?
- What tools can the model call, and who approves side effects?
- What structured output is validated?
- What trace/eval proves the Skill improves behavior?
- How can a user run it and verify it?
