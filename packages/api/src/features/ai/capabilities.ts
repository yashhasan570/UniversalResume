import type { AIProvider } from "@universal-resume/ai/types";
import { isDirectAiProvider } from "@universal-resume/ai/types";

type AiProviderCapabilityInput = {
	provider: AIProvider;
	baseURL?: string | null;
};

export function isDirectOpenAIProvider(input: Pick<AiProviderCapabilityInput, "provider" | "baseURL">) {
	return input.provider === "openai" && isDirectAiProvider(input);
}
