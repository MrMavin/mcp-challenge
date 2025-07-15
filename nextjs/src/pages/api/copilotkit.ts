import { NextApiRequest, NextApiResponse } from "next";
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSPagesRouterEndpoint,
} from "@copilotkit/runtime";
import { MCPClient } from "@/lib/mcp-client";

const serviceAdapter = new OpenAIAdapter({
  model: "gpt-4.1",
});

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  const runtime = new CopilotRuntime({
    createMCPClient: async (config) => {
      const client = new MCPClient({
        serverUrl: config.endpoint,
        headers:
          (config.apiKey && { Authorization: `Bearer ${config.apiKey}` }) || {},
      });

      await client.connect();

      return client;
    },
  });

  const handleRequest = copilotRuntimeNextJSPagesRouterEndpoint({
    endpoint: "/api/copilotkit",
    runtime,
    serviceAdapter,
  });

  return await handleRequest(req, res);
};

export default handler;
