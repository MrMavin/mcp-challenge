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
        // Forward any headers provided by CopilotKit (e.g. auth tokens)
        headers: (config as any).headers,
      });

      // Establish the SSE connection before CopilotKit starts querying tools
      await client.connect();

      return client;
    },
    middleware: {
      onAfterRequest: ({ inputMessages, outputMessages }) => {
        console.log(JSON.stringify({ inputMessages, outputMessages }, null, 2));
      },
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
