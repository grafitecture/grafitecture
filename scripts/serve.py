#!/usr/bin/env python3
"""Local stand-in for Vercel, for the checks in CI and on your machine: serves public/ with cleanUrls, the redirects
(including `has` host/query conditions) and headers from vercel.json, 404.html with status 404, and gzip.
Usage: python3 scripts/serve.py [port]        (default 8080; standard library only)"""
import gzip, http.server, json, pathlib, re, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
CFG = json.loads((ROOT / "vercel.json").read_text())
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
         ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".avif": "image/avif", ".woff": "font/woff",
         ".woff2": "font/woff2", ".xml": "application/xml", ".txt": "text/plain; charset=utf-8", ".ico": "image/x-icon",
         ".json": "application/json", ".webmanifest": "application/manifest+json", ".md": "text/markdown; charset=utf-8"}


def to_re(src):
    # vercel path-to-regexp subset: :param*, :param, (.*)
    s = re.escape(src).replace(r"\(\.\*\)", "(.*)")
    s = re.sub(r":(\w+)\\\*", r"(?P<\1>.*)", s)
    s = re.sub(r":(\w+)", r"(?P<\1>[^/]+)", s)
    return re.compile("^" + s + "$")


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body=b"", ctype=None, extra=None, path="/"):
        self.send_response(code)
        hdrs = {}
        for rule in CFG.get("headers", []):
            if to_re(rule["source"]).match(path):
                for h in rule["headers"]:
                    hdrs[h["key"]] = h["value"]
        hdrs.update(extra or {})
        if ctype:
            hdrs["Content-Type"] = ctype
        if body and "gzip" in self.headers.get("Accept-Encoding", "") and len(body) > 512:
            body = gzip.compress(body)
            hdrs["Content-Encoding"] = "gzip"
        hdrs["Content-Length"] = str(len(body))
        for k, v in hdrs.items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        u = urllib.parse.urlsplit(self.path)
        path = urllib.parse.unquote(u.path)
        q = urllib.parse.parse_qs(u.query)
        host = (self.headers.get("Host") or "").split(":")[0]
        def has_ok(r):
            for c in r.get("has", []):
                if c["type"] == "host" and not re.fullmatch(c["value"], host):
                    return False
                if c["type"] == "query" and (c["key"] not in q or ("value" in c and c["value"] not in q[c["key"]])):
                    return False
            return True
        for r in CFG.get("redirects", []):
            m = to_re(r["source"]).match(path)
            if m and has_ok(r):
                dest = r["destination"]
                for k, v in m.groupdict().items():
                    dest = dest.replace(":" + k + "*", v).replace(":" + k, v)
                code = r.get("statusCode") or (308 if r.get("permanent", True) else 307)
                return self.send(code, b"", None, {"Location": dest}, path)
        if CFG.get("cleanUrls") and path.endswith(".html"):
            clean = path[:-5]
            if clean.endswith("/index"):
                clean = clean[:-5]
            return self.send(308, b"", None, {"Location": clean or "/"}, path)
        cands = [PUB / path.lstrip("/")]
        if path.endswith("/"):
            cands = [PUB / path.lstrip("/") / "index.html"]
        elif CFG.get("cleanUrls"):
            cands.append(PUB / (path.lstrip("/") + ".html"))
        for f in cands:
            if f.is_file() and PUB in f.resolve().parents or f.resolve() == PUB:
                if f.is_file():
                    return self.send(200, f.read_bytes(), TYPES.get(f.suffix, "application/octet-stream"), None, path)
        nf = PUB / "404.html"
        return self.send(404, nf.read_bytes() if nf.exists() else b"Not found", TYPES[".html"], None, path)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"serving public/ on http://127.0.0.1:{port}", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
