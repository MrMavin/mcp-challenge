import {
  useCopilotAction,
  CatchAllActionRenderProps,
} from "@copilotkit/react-core";
import McpToolCall from "./mcp-tool-call";

/**
 * Renders tool calls for debugging purposes
 *
 * @returns A tool call component
 */
export function ToolRenderer() {
  useCopilotAction({
    name: "*",
    render: ({ name, status, args, result }: CatchAllActionRenderProps<[]>) => (
      <McpToolCall status={status} name={name} args={args} result={result} />
    ),
  });

  return null;
}
