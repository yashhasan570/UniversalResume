import { describe, expect, it } from "vite-plus/test";
import {
	getLocaleAlternates,
	getLocaleScript,
	getPreferredLocale,
	isLocale,
	localeSchema,
	localizedUrl,
	supportedLocales,
} from "./locale";

it.each([
	[["de-DE"], "de-DE"],
	[["unsupported", "fr-CA", "de-DE"], "fr-FR"],
	[["de-AT", "fr-FR"], "de-DE"],
	[["de-de"], "de-DE"],
	[["en-GB", "en-US"], "en-GB"],
	[["zu-ZA", "de-DE"], "de-DE"],
	[["zu-ZA"], "en-US"],
	[[], "en-US"],
])("matches ordered language preferences %j to %s", (languages, expected) => {
	expect(getPreferredLocale(languages)).toBe(expected);
});

it("keeps the testing catalog valid without counting it as a supported translation", () => {
	expect(isLocale("zu-ZA")).toBe(true);
	expect(localeSchema.options).toContain("zu-ZA");
	expect(supportedLocales).not.toContain("zu-ZA");
	expect(supportedLocales).toContain("de-DE");
	expect(getLocaleAlternates("https://universalresume.app/")).toHaveLength(supportedLocales.length + 1);
});

it("maps the Armenian locale to its script", () => {
	expect(getLocaleScript("hy-AM")).toBe("armenian");
});

describe("locale URLs", () => {
	it("keeps the default locale on the plain address and puts others in the locale parameter", () => {
		expect(localizedUrl("https://universalresume.app/?locale=de-DE", "en-US")).toBe("https://universalresume.app/");
		expect(localizedUrl("https://universalresume.app/", "de-DE")).toBe("https://universalresume.app/?locale=de-DE");
	});

	it("lists valid hreflang alternates without the pseudo-locale", () => {
		const alternates = getLocaleAlternates("https://universalresume.app/");

		expect(alternates).toContainEqual({ hreflang: "x-default", href: "https://universalresume.app/" });
		expect(alternates).toContainEqual({ hreflang: "sr", href: "https://universalresume.app/?locale=sr-SP" });
		expect(alternates.map((alternate) => alternate.hreflang)).not.toContain("zu-ZA");
	});
});
