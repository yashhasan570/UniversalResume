import { isIP } from "node:net";
import { attachDatabasePool, ipAddress, waitUntil } from "@vercel/functions";
import { configureAgentStreamLifetime } from "@universal-resume/api/features/agent/streams";
import { initializeAuth } from "@universal-resume/auth/config";
import { getPool } from "@universal-resume/db/client";
import { TRUSTED_IP_HEADERS } from "@universal-resume/utils/rate-limit";
import { createApp } from "./http/app";

configureAgentStreamLifetime(waitUntil);
attachDatabasePool(getPool());
const app = createApp({
	serveStatic: false,
	trustedClient: (request) => request.headers.get("x-real-ip") ?? "unknown",
});

export default {
	async fetch(request: Request) {
		await initializeAuth();
		const ip = ipAddress(request);
		const headers = new Headers(request.headers);
		for (const name of TRUSTED_IP_HEADERS) headers.delete(name);
		headers.delete("x-real-ip");
		if (ip && isIP(ip)) {
			headers.set("x-real-ip", ip);
			headers.set("x-forwarded-for", ip);
		}
		return app.fetch(new Request(request, { headers }));
	},
};
