import "@/styles/globals.css";
import "@copilotkit/react-ui/styles.css";

import { CopilotKit } from "@copilotkit/react-core";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <Component {...pageProps} />
    </CopilotKit>
  );
}
