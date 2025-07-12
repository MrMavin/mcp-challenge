import { ChatAuthenticateUser } from "@/components/chat/authenticate-user";
import { ChatShowProducts } from "@/components/chat/show-products";
import McpServerManager from "@/components/mcp-server-manager";
import { ToolRenderer } from "@/components/tool-renderer";
import { CopilotChat } from "@copilotkit/react-ui";

export default function ChatInterface() {
  return (
    <div className="flex h-screen p-4">
      <McpServerManager />
      <ChatAuthenticateUser />
      <ChatShowProducts />
      <CopilotChat
        instructions={`You are a shopping assistant with access to login, products and cart tools.
          
Help the user with their shopping needs. Make sure that they're authenticated before allowing them to add items to their cart.

Do not talk technically to the user and make sure to use simple language. Make sure to always read MCP requirements before doing requests.`}
        className="flex-grow rounded-lg w-full"
      />
      <ToolRenderer />
    </div>
  );
}
