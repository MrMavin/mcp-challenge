import { useCopilotAction } from "@copilotkit/react-core";
import { useCopilotReadable } from "@copilotkit/react-core";
import { useState } from "react";

export function ChatCartIdStore() {
  const [cartId, setCartId] = useState<string | null>(null);

  useCopilotReadable({
    description:
      "Store the current user's cart id after creating a cart. This is null if the cart has not been created.",
    value: cartId,
  });

  useCopilotAction({
    name: "storeCartId",
    description:
      "Stores the cart id after that we have created our cart successfully.",
    parameters: [
      {
        name: "cartId",
        description: "The cart id to store.",
        type: "string",
        required: true,
      },
    ],
    render: ({ args, status }) => {
      if (status === "complete") {
        setCartId(args.cartId);
      }

      return <></>;
    },
  });

  return null;
}
