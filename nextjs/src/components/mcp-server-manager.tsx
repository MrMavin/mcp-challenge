"use client";

import { useCopilotChat } from "@copilotkit/react-core";
import { useEffect } from "react";
import { useChatStore } from "./chat/state";

function McpServerManager() {
  const { userId } = useChatStore();

  const { setMcpServers } = useCopilotChat();

  useEffect(() => {
    setMcpServers([
      {
        endpoint: process.env.NEXT_PUBLIC_MCP_ENDPOINT!,
        apiKey: userId!,
      },
    ]);
  }, [setMcpServers, userId]);

  return null;
}

export default McpServerManager;
