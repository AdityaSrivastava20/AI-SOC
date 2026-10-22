from urllib.parse import urlparse


def extract_url_features(url: str):

    parsed_url = urlparse(url)

    hostname = parsed_url.hostname or ""
    path = parsed_url.path or ""
    query = parsed_url.query or ""

    features = {
        "url_length": len(url),

        "hostname_length": len(hostname),

        "path_length": len(path),

        "query_length": len(query),

        "dot_count": url.count("."),

        "hyphen_count": url.count("-"),

        "special_characters": sum(
            1 for char in url
            if char in "@#$%&*=+_?"
        ),

        "has_https": 1 if parsed_url.scheme == "https" else 0,

        "is_ip_address": 1 if (
            len(hostname.split(".")) == 4
            and all(
                part.isdigit()
                for part in hostname.split(".")
            )
        ) else 0,

        "suspicious_word_count": sum(
            1
            for word in [
                "login",
                "verify",
                "account",
                "secure",
                "update",
                "password",
                "bank",
                "free",
                "confirm"
            ]
            if word in url.lower()
        )
    }

    return features