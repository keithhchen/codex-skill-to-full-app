# LLM Providers Reference

Use this reference when wiring public OpenAI-compatible model services.

Assume the app uses public OpenAI-compatible API services.

## Generic OpenAI-Compatible Pattern

```ts
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.MODEL_API_KEY,
  baseURL: process.env.MODEL_BASE_URL,
});

const result = await client.chat.completions.create({
  model: process.env.MODEL_NAME!,
  messages: [
    { role: "system", content: skillMarkdown },
    { role: "user", content: userInput },
  ],
  response_format: { type: "json_object" },
  tools,
  tool_choice: "auto",
});
```

Validate final JSON in app code even when the provider supports JSON output.

## Provider Table

| Provider | Base URL | Typical env vars | Notes |
| --- | --- | --- | --- |
| DeepSeek | `https://api.deepseek.com` | `DEEPSEEK_API_KEY`, `MODEL_NAME` | OpenAI-compatible; supports JSON output and tool calling |
| Kimi / Moonshot | `https://api.moonshot.ai/v1` | `MOONSHOT_API_KEY`, `MODEL_NAME` | OpenAI-compatible; supports JSON mode/schema and tool calls |
| Z.AI / GLM | `https://api.z.ai/api/paas/v4/` | `ZAI_API_KEY`, `MODEL_NAME` | OpenAI-compatible; supports structured output and tool calls |
| Qwen / DashScope | workspace or DashScope `compatible-mode/v1` endpoint | `DASHSCOPE_API_KEY`, `MODEL_NAME`, optional `WORKSPACE_ID` | OpenAI-compatible; endpoints vary by region/workspace |

Always verify current model names in the provider console/docs at implementation time.

## DeepSeek

Base URL:

```text
https://api.deepseek.com
```

Example:

```ts
const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: "https://api.deepseek.com",
});

const res = await client.chat.completions.create({
  model: process.env.MODEL_NAME ?? "deepseek-chat",
  messages,
  response_format: { type: "json_object" },
  tools,
});
```

Notes:

- Supports OpenAI-style chat completions.
- Supports JSON output through `response_format`.
- Supports OpenAI-style tool calling.
- Some stricter schema behavior may require provider-specific beta settings; check current docs.

Sources:

- https://api-docs.deepseek.com/
- https://api-docs.deepseek.com/guides/json_mode
- https://api-docs.deepseek.com/guides/tool_calls

## Kimi / Moonshot

Base URL:

```text
https://api.moonshot.ai/v1
```

Example:

```ts
const client = new OpenAI({
  apiKey: process.env.MOONSHOT_API_KEY,
  baseURL: "https://api.moonshot.ai/v1",
});

const res = await client.chat.completions.create({
  model: process.env.MODEL_NAME ?? "kimi-k2",
  messages,
  response_format: {
    type: "json_schema",
    json_schema: {
      name: "skill_output",
      schema: outputSchema,
    },
  },
  tools,
  tool_choice: "auto",
});
```

Notes:

- Supports OpenAI-style API usage.
- Supports structured output through JSON mode/schema.
- Supports tool calls.
- Check current reasoning/thinking-model constraints before using tool calls with a thinking model.

Sources:

- https://platform.kimi.ai/docs/api/overview
- https://platform.kimi.ai/docs/api/chat
- https://platform.kimi.ai/docs/guide/use-kimi-api-to-complete-tool-calls
- https://platform.kimi.ai/docs/guide/migrating-from-openai-to-kimi

## Z.AI / GLM

Base URL:

```text
https://api.z.ai/api/paas/v4/
```

Example:

```ts
const client = new OpenAI({
  apiKey: process.env.ZAI_API_KEY,
  baseURL: "https://api.z.ai/api/paas/v4/",
});

const res = await client.chat.completions.create({
  model: process.env.MODEL_NAME ?? "glm-4",
  messages,
  response_format: { type: "json_object" },
  tools,
});
```

Notes:

- Supports OpenAI SDK-style migration.
- Supports structured output.
- Supports tool call response fields.
- Some coding subscriptions may use a separate coding endpoint; check plan-specific docs.

Sources:

- https://docs.z.ai/api-reference/introduction
- https://docs.z.ai/guides/develop/openai/python
- https://docs.z.ai/guides/capabilities/struct-output
- https://docs.z.ai/api-reference/llm/chat-completion

## Qwen / DashScope

Common endpoints include workspace-specific compatible-mode URLs:

```text
https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
https://dashscope.aliyuncs.com/compatible-mode/v1
https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

Example:

```ts
const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: process.env.DASHSCOPE_BASE_URL,
});

const res = await client.chat.completions.create({
  model: process.env.MODEL_NAME ?? "qwen-plus",
  messages: [
    { role: "system", content: `${skillMarkdown}\nReturn valid JSON only.` },
    { role: "user", content: userInput },
  ],
  response_format: { type: "json_object" },
  tools,
  tool_choice: "auto",
});
```

Notes:

- Supports OpenAI-compatible chat completion.
- JSON output often requires both `response_format` and explicit instruction containing "JSON".
- Supports function/tool calling on supported model families.
- Region/workspace endpoints can differ; keep base URL configurable.

Sources:

- https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope
- https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output
- https://www.alibabacloud.com/help/en/model-studio/qwen-function-calling

## Provider Configuration Object

Use one config shape:

```ts
export const providerConfig = {
  provider: process.env.MODEL_PROVIDER,
  baseURL: process.env.MODEL_BASE_URL,
  apiKey: process.env.MODEL_API_KEY,
  model: process.env.MODEL_NAME,
};
```

Map provider-specific keys at the deployment layer:

```text
MODEL_PROVIDER=deepseek
MODEL_BASE_URL=https://api.deepseek.com
MODEL_API_KEY=${DEEPSEEK_API_KEY}
MODEL_NAME=...
```

## Compatibility Checklist

Before shipping:

- Can the configured model return valid JSON for the output schema?
- Can it return OpenAI-style `tool_calls`?
- Does `tool_choice: "auto"` work as expected?
- Are there provider-specific restrictions on JSON schema, strict mode, or thinking mode?
- Are token usage, latency, and error responses logged?
- Can the app swap provider by changing env vars only?
