# Runtime Layer Reference

Use this reference when designing the agent runtime that executes the Skill.

## Role

The runtime layer turns a model call into an AI-native workflow:

```text
load Skill
compile instructions
attach context/resources
call model
execute tool calls
append observations
validate structured output
ask for human approval when required
store trace
run evals
```

The runtime is where "agentic" behavior actually lives.

## Runtime Options

| Runtime | Use when | Notes |
| --- | --- | --- |
| Thin custom loop | 1-3 tools, simple business workflow, maximum transparency | Best teaching/default V1 |
| OpenAI Agents SDK | tools, handoffs, guardrails, sessions, tracing | Strong runtime primitives; strongest with OpenAI defaults, but has Chat Completions model path |
| LangGraph | state, branching, retries, human-in-the-loop, long workflows | Best for explicit workflow graph |
| Google ADK | full agent framework, multi-agent, A2A-style patterns | Useful when adopting a broader agent framework |
| PydanticAI | Python, typed outputs, validation-first apps | Good when schemas/evals are central |
| LlamaIndex Workflows | RAG/document-heavy workflows | Good for knowledge-base apps |
| Microsoft Agent Framework | .NET/Python enterprise workflows | Good for Microsoft-heavy stacks |

## Thin Custom Loop

Use this when you want the least magic:

```ts
async function runSkill(input: RunInput) {
  const skill = await loadSkill(input.skillId);
  const state = await createRunState(input);

  let messages = compileSkillMessages(skill, input);

  for (let step = 0; step < MAX_STEPS; step++) {
    const modelResult = await modelClient.chat({ messages, tools, responseSchema });
    await traceModelCall(state.runId, modelResult);

    if (modelResult.toolCalls?.length) {
      for (const call of modelResult.toolCalls) {
        assertToolAllowed(call, state.permissions);
        const observation = await executeTool(call);
        await traceToolCall(state.runId, call, observation);
        messages.push(toolResultMessage(call, observation));
      }
      continue;
    }

    const output = validateOutput(modelResult);
    const reviewed = await requireReviewIfNeeded(output, state.policy);
    await saveFinalOutput(state.runId, reviewed);
    return reviewed;
  }

  throw new Error("Runtime exceeded max steps");
}
```

Required primitives:

- `loadSkill`
- `compileSkillMessages`
- `modelClient.chat`
- `executeTool`
- `validateOutput`
- `requireReviewIfNeeded`
- `traceModelCall`
- `traceToolCall`
- `saveFinalOutput`

## OpenAI Agents SDK

Use OpenAI Agents SDK when the product needs runtime primitives that would otherwise be rebuilt:

- agents with instructions and tools
- handoffs between specialist agents
- guardrails
- sessions and memory-like state
- tracing for model calls, tool calls, handoffs, and custom spans
- human approval patterns around tool execution

Use it when runtime ownership matters more than raw provider portability. If the target provider is a non-OpenAI public OpenAI-compatible service, verify the Chat Completions model path and any SDK compatibility constraints before committing.

## LangGraph

Use LangGraph when the workflow should be represented as a state machine or graph:

- classify input
- retrieve context
- run model
- call tools
- branch on validation
- wait for human approval
- retry or correct
- finalize

It is a good fit when you need durable state and explicit control over loop transitions.

## Google ADK

Use Google ADK when building a fuller agent system rather than a single app-owned loop:

- multi-agent orchestration
- tool ecosystem
- model connectors or gateways
- enterprise agent patterns
- A2A-style designs

Keep the Skill as the business behavior spec; do not let framework abstractions replace the domain rules.

## PydanticAI

Use PydanticAI when:

- backend is Python
- structured output quality is critical
- validation errors should drive retries or corrections
- typed data models are core to the product

It is especially useful for business artifacts with strict schemas: reports, audit workpapers, deal memos, finance anomaly review, policy checks.

## Runtime State

Persist enough state to debug and improve:

- run id
- user id
- skill version
- provider/model
- input payload
- compiled instruction hash
- tool calls and observations
- output JSON
- schema validation results
- human review decision
- corrections
- eval result

## Approval Gates

Stop for human review before:

- sending emails/messages
- publishing content
- changing production data
- committing financial/legal/compliance conclusions
- external API calls with side effects
- irreversible workflow transitions

The model may draft or recommend. The app owns approval.

## Eval Harness

Every Skill-to-App runtime should include small evals:

- baseline model output without Skill
- Skill-guided output
- bad case where the model should refuse, flag uncertainty, or ask for missing data
- regression case for a previously fixed error
- schema validation case
- tool-call correctness case

Store eval cases near the Skill or in a dedicated `eval_cases` table.
