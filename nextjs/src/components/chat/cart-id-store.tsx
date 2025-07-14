import { useCopilotAction } from "@copilotkit/react-core";
import { useCopilotReadable } from "@copilotkit/react-core";
import { useState } from "react";

export function ChatCartIdStore() {
  const [cartId, setCartId] = useState<string | null>(null);

  useCopilotReadable({
    description:
      "The current user's cart id. This is null if the cart has not been created.",
    value: cartId,
  });
  console.log(cartId);
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
