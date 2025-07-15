import { useCopilotAction } from "@copilotkit/react-core";
import { useCopilotReadable } from "@copilotkit/react-core";
import { useCallback, useState } from "react";

export function ChatCartIdStore() {
  const [cartId, setCartId] = useState<string | null>(null);

  const updateCartId = useCallback((cartId: string) => {
    setCartId(cartId);
  }, []);

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
      console.log(args);
      if (status === "complete" && args.cartId && cartId !== args.cartId) {
        console.log("KEK");
        updateCartId(args.cartId);
      }

      return <></>;
    },
  });

  return null;
}
