import json
import logging
import urllib.request


class ProxyHandler:
    current_proxy_url: str | None = None
    log = logging.getLogger("maufbapi.proxy")

    def get_proxy_url_from_api(self) -> str | None:
        request = urllib.request.Request(self.api_url, method="GET")

        try:
            with urllib.request.urlopen(request) as f:
                response = json.loads(f.read().decode())
        except Exception:
            self.log.exception("Failed to retrieve proxy from API")
        else:
            return response["proxy_url"]

    def update_proxy_url(self) -> bool:
        old_proxy = self.current_proxy_url
        new_proxy = None

        if self.api_url is not None:
            new_proxy = self.get_proxy_url_from_api(self.api_url)
        else:
            new_proxy = urllib.request.getproxies().get("http")

        if new_proxy:
            self.log.debug("Set new proxy URL: %s", new_proxy)
            self.current_proxy_url = new_proxy

        return old_proxy != new_proxy

    def get_proxy_url(self) -> str | None:
        if not self.current_proxy_url:
            self.update_proxy_url()

        return self.current_proxy_url
