from flask import redirect, request, url_for
import urllib.parse


def redirectTo(redirectUri: str):
    if not 'x-original-host' in request.headers:
        return redirect(redirectUri)

    # manipulate redirectUrl as per reverse proxy host
    originalHost = request.headers['x-original-host']
    originalRequestScheme = 'https://' if (
        'x-arr-ssl' in request.headers) else 'http://'
    redirectUri = urllib.parse.urljoin(
        originalRequestScheme+originalHost, redirectUri)

    return redirect(redirectUri)
