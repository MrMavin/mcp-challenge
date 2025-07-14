import { ChatAuthenticateUser } from "@/components/chat/authenticate-user";
import { ChatShowProducts } from "@/components/chat/show-products";
import McpServerManager from "@/components/mcp-server-manager";
import { ToolRenderer } from "@/components/tool-renderer";
import { CopilotChat } from "@copilotkit/react-ui";
import { ChatCartIdStore } from "@/components/chat/cart-id-store";
import { ChatShowCart } from "@/components/chat/show-cart";

export default function ChatInterface() {
  return (
    <div className="flex h-screen p-4">
      <McpServerManager />
      <ChatAuthenticateUser />
      <ChatShowProducts />
      <ChatShowCart />
      <ChatCartIdStore />
      <CopilotChat
        instructions={`You are a shopping assistant with access to login, products and cart tools.
          
Help the user with their shopping needs. Make sure that they're authenticated before allowing them to add items to their cart. You have the capability to show the login tool if the user is not authenticated.

Always refer to the MCP required parameters for each call. If the MCP is giving you an error, read the response and try again following hints.`}
        className="flex-grow rounded-lg w-full"
      />
      <ToolRenderer />
    </div>
  );
}
