"use client";

import { useCopilotChat } from "@copilotkit/react-core";
import { useEffect } from "react";

function McpServerManager() {
  const { setMcpServers, mcpServers } = useCopilotChat();

  useEffect(() => {
    setMcpServers([
      {
        endpoint: "http://localhost:8000/mcp",
      },
    ]);
  }, [setMcpServers]);

  return null;
}

export default McpServerManager;
