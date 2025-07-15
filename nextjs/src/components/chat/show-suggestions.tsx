import { useCopilotChatSuggestions } from "@copilotkit/react-ui";
import { useChatStore } from "./state";

export default function ChatShowSuggestions() {
  const { username, cartId } = useChatStore();

  useCopilotChatSuggestions(
    {
      instructions:
        "Suggest the most relevant next actions. You need to login in order to manage your cart. When showing product prompt to show two products. When showing cart also suggest to remove one item.",
      minSuggestions: 1,
      maxSuggestions: 3,
    },
    [username, cartId]
  );

  return null;
}
