// Serves the dataset out of the R2 bucket at /data/* and lets the static
// assets handle everything else. The bucket is written by deploy/update.sh
// on the crawler, never by the site build: the two flows meet only here.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith("/data/")) {
      return env.ASSETS.fetch(request);
    }
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405 });
    }
    const key = url.pathname.slice("/data/".length);
    if (!key || key.includes("..")) {
      return new Response("Not found", { status: 404 });
    }
    const object = await env.DATA.get(key);
    if (object === null) {
      return new Response("Not found", { status: 404 });
    }
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("etag", object.httpEtag);
    // The crawler overwrites these keys nightly, so an hour of edge cache is
    // invisible next to that cadence and keeps repeat downloads off the bucket.
    headers.set("cache-control", "public, max-age=3600");
    if (key.endsWith(".gz")) {
      headers.set("content-type", "application/gzip");
    }
    return new Response(object.body, { headers });
  },
};
