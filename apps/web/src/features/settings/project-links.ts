import type { IconName } from "@universal-resume/ui/components/icon";
import { t } from "@lingui/core/macro";

/** The project's own pages, under Settings on desktop and as rows on the phone's Settings root. */
export const getProjectLinks = (): { href: string; label: string; icon: IconName }[] => [
	{ href: "https://docs.universalresume.app", label: t`Docs`, icon: "book-open" },
	{ href: "https://github.com/universal-resume/universal-resume", label: t`Source`, icon: "code" },
	{ href: "https://github.com/universal-resume/universal-resume/issues", label: t`Report a bug`, icon: "bug" },
	{ href: "https://opencollective.com/universal-resume/donate", label: t`Donate`, icon: "hand-heart" },
];
