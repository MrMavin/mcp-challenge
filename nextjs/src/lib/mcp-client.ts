import { MCPTool, MCPClient as MCPClientInterface } from "@copilotkit/runtime";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import type { JSONRPCMessage } from "@modelcontextprotocol/sdk/types.js";

export interface McpClientOptions {
  serverUrl: string;
  headers?: Record<string, string>;
  onMessage?: (message: Record<string, unknown>) => void;
  onError?: (error: Error) => void;
  onOpen?: () => void;
  onClose?: () => void;
}

/**
 * McpClient - A Model Context Protocol client implementation
 *
 * This class implements the Model Context Protocol (MCP) client, which allows for
 * standardized communication with MCP servers. It's designed to be compatible with
 * CopilotKit's runtime by exposing the required interface.
 */
export class MCPClient implements MCPClientInterface {
  private client: Client;
  private transport: SSEClientTransport;
  private serverUrl: URL;
  private onMessage: (message: Record<string, unknown>) => void;
  private onError: (error: Error) => void;
  private onOpen: () => void;
  private onClose: () => void;
  private isConnected = false;
  private headers?: Record<string, string>;

  // Cache for tools to avoid repeated fetches
  private toolsCache: Record<string, MCPTool> | null = null;

  constructor(options: McpClientOptions) {
    const isDebug = process.env.DEBUG === "true";

    this.serverUrl = new URL(options.serverUrl);
    this.headers = options.headers;

    this.onMessage =
      options.onMessage ||
      ((message) => {
        if (isDebug) {
          console.log("Message received:", JSON.stringify(message, null, 2));
        }
      });

    this.onError =
      options.onError ||
      ((error) => console.error("Error:", JSON.stringify(error, null, 2)));

    this.onOpen =
      options.onOpen ||
      (() => {
        if (isDebug) {
          console.log("Connection opened");
        }
      });
    this.onClose =
      options.onClose ||
      (() => {
        if (isDebug) {
          console.log("Connection closed");
        }
      });

    // Initialize the SSE transport with headers
    this.transport = new SSEClientTransport(this.serverUrl, {
      requestInit: {
        headers: this.headers,
      },
    });

    // Initialize the client
    this.client = new Client({
      name: "cpk-mcp-client",
      version: "0.0.1",
    });

    // Set up event handlers
    this.transport.onmessage = this.handleMessage.bind(this);
    this.transport.onerror = this.handleError.bind(this);
    this.transport.onclose = this.handleClose.bind(this);
  }

  private handleMessage(message: JSONRPCMessage): void {
    try {
      this.onMessage(message as Record<string, unknown>);
    } catch (error) {
      this.onError(
        error instanceof Error
          ? error
          : new Error(`Failed to handle message: ${error}`)
      );
    }
  }

  private handleError(error: Error): void {
    this.onError(error);
    if (this.isConnected) {
      this.isConnected = false;
    }
  }

  private handleClose(): void {
    this.isConnected = false;
    this.onClose();
  }

  public async connect(): Promise<void> {
    try {
      await this.client.connect(this.transport);

      this.isConnected = true;

      this.onOpen();
    } catch (error) {
      console.error("Failed to connect to MCP server:", error);

      this.onError(error instanceof Error ? error : new Error(String(error)));

      throw error;
    }
  }

  public async tools(): Promise<Record<string, MCPTool>> {
    try {
      if (this.toolsCache) {
        return this.toolsCache;
      }

      // we are getting tools from the mcp server that
      // will later be standardized to our internal format
      const rawToolsResult = await this.client.listTools();

      let toolsToProcess: object[] = [];

      if (Array.isArray(rawToolsResult)) {
        toolsToProcess = rawToolsResult;
      } else if (rawToolsResult?.tools && Array.isArray(rawToolsResult.tools)) {
        toolsToProcess = rawToolsResult.tools;
      }

      if (toolsToProcess.length === 0) {
        throw new Error("No tools found");
      }

      const toolsMap: Record<string, MCPTool> = {};

      toolsToProcess.forEach((tool: any) => {
        toolsMap[tool.name] = {
          description: tool.description,
          schema: tool.inputSchema || {},
          execute: async (args: Record<string, unknown>) => {
            return this.callTool(tool.name, args);
          },
        };
      });

      this.toolsCache = toolsMap;

      return toolsMap;
    } catch (error) {
      console.error("Error fetching tools:", error);
      return {};
    }
  }

  public async close(): Promise<void> {
    try {
      // Clear the tools cache
      this.toolsCache = null;

      // Close the transport connection
      await this.transport.close();
      this.isConnected = false;
      console.log("Disconnected from MCP server");
    } catch (error) {
      console.error("Error disconnecting from MCP server:", error);
      this.onError(error instanceof Error ? error : new Error(String(error)));
    }
  }

  public async callTool(
    name: string,
    args: Record<string, unknown>
  ): Promise<any> {
    try {
      const processedArgs = this.processToolArguments(args);

      return this.client.callTool({
        name: name,
        arguments: processedArgs,
      });
    } catch (error) {
      console.error(`Error calling tool ${name}:`, error);
      throw error;
    }
  }

  /**
   * Unified argument processor that handles all necessary transformations in one place
   * - Flattens nested parameter structures
   * - Handles path parameters for FastAPI compatibility
   * - Processes string-encoded JSON
   *
   * @param args The original arguments passed to the tool
   * @returns Processed arguments ready for MCP tool calls
   */
  private processToolArguments(
    args: Record<string, unknown>
  ): Record<string, unknown> {
    const result: Record<string, unknown> = {};

    // Step 1: Extract and flatten any params objects
    // We're not doing a deep recursive extraction to avoid unexpected behavior
    // We specifically just handle the common patterns we've observed
    let paramsToProcess = { ...args };

    // Handle double-nested params: { params: { params: { actual data } } }
    if (args.params && typeof args.params === "object") {
      const paramsObj = args.params as Record<string, unknown>;

      // Check for double-nesting
      if ("params" in paramsObj && typeof paramsObj.params === "object") {
        console.log("Extracted from double-nested params");
        paramsToProcess = {
          ...args,
          ...(paramsObj.params as Record<string, unknown>),
        };
      } else {
        // Single nesting - flatten params to root
        console.log("Extracted from single-nested params");
        paramsToProcess = { ...args, ...paramsObj };
      }
    }

    // Step 2: Process each argument and convert any string-encoded JSON
    for (const [key, value] of Object.entries(paramsToProcess)) {
      // Skip the original params object since we've already processed it
      if (key === "params") continue;

      // Handle potential JSON strings
      if (typeof value === "string") {
        try {
          // Try to parse as JSON, but keep as string if it fails
          const parsedValue = JSON.parse(value);
          result[key] = parsedValue;
        } catch (e) {
          // Not valid JSON, keep as string
          result[key] = value;
        }
      } else {
        // Keep non-string values as-is
        result[key] = value;
      }
    }

    return result;
  }
}
