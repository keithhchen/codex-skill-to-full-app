# Client Layer Reference

Use this reference when selecting or implementing the model client that talks to public OpenAI-compatible model services.

## Role

The client layer is not the agent runtime. It only sends requests to a model service and receives responses.

It should standardize:

- `baseURL`
- `apiKey`
- `model`
- `messages`
- `response_format`
- `tools`
- `tool_calls`
- streaming behavior, if used
- provider-specific parameter differences

## Decision Guide

| Choice | Use when | Avoid when |
| --- | --- | --- |
| OpenAI SDK | You need the simplest OpenAI-compatible API client | You need stateful workflows, tool execution, or UI helpers built in |
| Vercel AI SDK | You are building a TypeScript / Next.js app with streaming UX, structured output, or tool UI | You are not in a JS/TS web app |
| LiteLLM | You need one internal gateway over many model providers | You expect it to manage product workflow or app state |
| Custom wrapper | You need a stable internal interface over provider quirks | The app can use an existing SDK cleanly |

## OpenAI SDK As Compatibility Client

In an agnostic app, `openai` often means "OpenAI-compatible client", not "OpenAI-only".

```ts
import OpenAI from "openai";

export function createModelClient() {
  return new OpenAI({
    apiKey: process.env.MODEL_API_KEY,
    baseURL: process.env.MODEL_BASE_URL,
  });
}

export async function callModel({
  skillMarkdown,
  userInput,
  tools,
}: {
  skillMarkdown: string;
  userInput: string;
  tools?: OpenAI.Chat.ChatCompletionTool[];
}) {
  const client = createModelClient();

  return client.chat.completions.create({
    model: process.env.MODEL_NAME!,
    messages: [
      { role: "system", content: skillMarkdown },
      { role: "user", content: userInput },
    ],
    response_format: { type: "json_object" },
    tools,
  });
}
```

The OpenAI SDK gives a request/response shape. It does not execute tools, store state, or run evals.

## Vercel AI SDK

Use Vercel AI SDK when the app is TypeScript-first and the UI benefits from streaming, structured output, or tool-aware rendering.

Typical fit:

- Next.js app
- dashboard
- review UI
- streaming generation
- structured output with schema validation
- OpenAI-compatible provider adapter

Keep the Skill as separate text and pass it into the model call as instructions. Do not rewrite the Skill as UI copy.

## LiteLLM

Use LiteLLM as a gateway:

```text
App -> LiteLLM proxy -> DeepSeek / Kimi / GLM / Qwen / other provider
```

Good for:

- central provider routing
- central key management
- logging and budget controls
- switching providers without app code churn

Do not treat LiteLLM as the full runtime. The app still needs tool execution, state, review, and evals.

## Provider Adapter Interface

Create one internal interface and map provider quirks behind it:

```ts
export type ModelProviderConfig = {
  provider: "deepseek" | "kimi" | "glm" | "qwen" | "custom";
  baseURL: string;
  apiKey: string;
  model: string;
};

export type ModelRequest = {
  system: string;
  user: string;
  tools?: unknown[];
  responseFormat?: "json_object" | "json_schema";
};

export type ModelResponse = {
  text?: string;
  json?: unknown;
  toolCalls?: Array<{
    id: string;
    name: string;
    arguments: unknown;
  }>;
  raw: unknown;
};
```

## Implementation Rules

- Keep provider config in environment variables or encrypted settings.
- Never hardcode API keys.
- Keep model names configurable.
- Validate final JSON in app code even when using JSON mode.
- Log provider, model, latency, token usage if available, validation status, and tool-call count.
- Fail closed when JSON parsing, schema validation, or approval checks fail.

