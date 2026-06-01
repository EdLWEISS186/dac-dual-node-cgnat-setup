from ipaddress import ip_address, ip_network


PROVIDER_HINTS = [
    {
        "provider_guess": "OVHcloud",
        "asn_hint": "AS16276",
        "provider_type": "VPS / Dedicated",
        "country_hint": "France / Europe",
        "confidence": "HIGH",
        "prefixes": [
            "51.68.0.0/16",
            "51.75.0.0/16",
            "51.77.0.0/16",
            "51.89.0.0/16",
            "54.36.0.0/16",
            "57.128.0.0/17",
            "91.134.0.0/16",
            "141.94.0.0/16",
            "145.239.0.0/16",
            "146.59.0.0/16",
            "147.135.0.0/16",
            "149.202.0.0/16",
            "152.228.0.0/16",
            "164.132.0.0/16",
            "176.31.0.0/16",
            "178.32.0.0/15",
            "188.165.0.0/16",
            "213.186.32.0/19",
            "213.251.128.0/18"
        ],
        "notes": "Static prefix heuristic based on commonly observed OVHcloud ranges. Treat as enrichment, not verified ASN lookup."
    },
    {
        "provider_guess": "Hetzner",
        "asn_hint": "AS24940",
        "provider_type": "VPS / Dedicated",
        "country_hint": "Germany / Finland",
        "confidence": "HIGH",
        "prefixes": [
            "65.21.0.0/16",
            "88.99.0.0/16",
            "91.107.0.0/16",
            "95.216.0.0/16",
            "136.243.0.0/16",
            "138.201.0.0/16",
            "144.76.0.0/16",
            "157.90.0.0/16",
            "159.69.0.0/16",
            "162.55.0.0/16",
            "167.235.0.0/16",
            "168.119.0.0/16",
            "176.9.0.0/16",
            "178.63.0.0/16",
            "188.34.0.0/16",
            "195.201.0.0/16"
        ],
        "notes": "Static prefix heuristic based on commonly observed Hetzner ranges."
    },
    {
        "provider_guess": "DigitalOcean",
        "asn_hint": "AS14061",
        "provider_type": "VPS",
        "country_hint": "Global",
        "confidence": "HIGH",
        "prefixes": [
            "134.122.0.0/16",
            "138.68.0.0/16",
            "139.59.0.0/16",
            "143.110.0.0/16",
            "157.230.0.0/16",
            "159.65.0.0/16",
            "161.35.0.0/16",
            "164.90.0.0/16",
            "167.99.0.0/16",
            "178.128.0.0/16",
            "188.166.0.0/16",
            "206.189.0.0/16"
        ],
        "notes": "Static prefix heuristic based on common DigitalOcean ranges."
    },
    {
        "provider_guess": "Vultr",
        "asn_hint": "AS20473",
        "provider_type": "VPS",
        "country_hint": "Global",
        "confidence": "HIGH",
        "prefixes": [
            "45.32.0.0/16",
            "45.63.0.0/16",
            "64.176.0.0/16",
            "95.179.0.0/16",
            "108.61.0.0/16",
            "140.82.0.0/16",
            "144.202.0.0/16",
            "149.28.0.0/16",
            "155.138.0.0/16",
            "199.247.0.0/16",
            "207.148.0.0/16",
            "216.128.0.0/16"
        ],
        "notes": "Static prefix heuristic based on common Vultr ranges."
    },
    {
        "provider_guess": "Linode / Akamai Connected Cloud",
        "asn_hint": "AS63949",
        "provider_type": "VPS",
        "country_hint": "Global",
        "confidence": "HIGH",
        "prefixes": [
            "45.33.0.0/16",
            "45.56.0.0/16",
            "66.175.0.0/16",
            "72.14.176.0/20",
            "96.126.96.0/19",
            "139.144.0.0/16",
            "172.104.0.0/15",
            "173.230.128.0/17",
            "192.46.208.0/20",
            "198.58.96.0/19"
        ],
        "notes": "Static prefix heuristic for Linode/Akamai Connected Cloud ranges."
    },
    {
        "provider_guess": "Contabo",
        "asn_hint": "AS51167",
        "provider_type": "VPS",
        "country_hint": "Germany / Global",
        "confidence": "HIGH",
        "prefixes": [
            "62.171.128.0/17",
            "161.97.0.0/16",
            "173.212.192.0/18",
            "207.180.192.0/18",
            "213.136.82.0/23"
        ],
        "notes": "Static prefix heuristic based on common Contabo ranges."
    },
    {
        "provider_guess": "AWS",
        "asn_hint": "AS16509",
        "provider_type": "Cloud",
        "country_hint": "Global",
        "confidence": "MEDIUM",
        "prefixes": [
            "3.0.0.0/8",
            "13.0.0.0/8",
            "18.0.0.0/8",
            "35.0.0.0/8",
            "52.0.0.0/8",
            "54.0.0.0/8"
        ],
        "notes": "Broad static AWS heuristic. Large ranges can overlap by region/use case; verify ASN for high-confidence reporting."
    },
    {
        "provider_guess": "Google Cloud",
        "asn_hint": "AS15169",
        "provider_type": "Cloud",
        "country_hint": "Global",
        "confidence": "MEDIUM",
        "prefixes": [
            "34.0.0.0/8",
            "35.184.0.0/13",
            "104.196.0.0/14",
            "146.148.0.0/17"
        ],
        "notes": "Broad Google Cloud heuristic. Verify ASN for high-confidence reporting."
    },
    {
        "provider_guess": "Microsoft Azure",
        "asn_hint": "AS8075",
        "provider_type": "Cloud",
        "country_hint": "Global",
        "confidence": "MEDIUM",
        "prefixes": [
            "20.0.0.0/8",
            "40.64.0.0/10",
            "52.224.0.0/11"
        ],
        "notes": "Broad Azure heuristic. Verify ASN for high-confidence reporting."
    },
    {
        "provider_guess": "Oracle Cloud Infrastructure",
        "asn_hint": "AS31898",
        "provider_type": "Cloud",
        "country_hint": "Global",
        "confidence": "MEDIUM",
        "prefixes": [
            "129.146.0.0/16",
            "130.61.0.0/16",
            "132.145.0.0/16",
            "140.238.0.0/16",
            "150.136.0.0/16"
        ],
        "notes": "Static OCI heuristic."
    },
    {
        "provider_guess": "Alibaba Cloud",
        "asn_hint": "AS45102",
        "provider_type": "Cloud",
        "country_hint": "China / Asia",
        "confidence": "MEDIUM",
        "prefixes": [
            "39.96.0.0/12",
            "47.88.0.0/13",
            "47.96.0.0/12",
            "8.208.0.0/12"
        ],
        "notes": "Static Alibaba Cloud heuristic."
    },
    {
        "provider_guess": "Tencent Cloud",
        "asn_hint": "AS132203",
        "provider_type": "Cloud",
        "country_hint": "China / Asia",
        "confidence": "MEDIUM",
        "prefixes": [
            "43.128.0.0/12",
            "49.51.0.0/16",
            "101.32.0.0/12",
            "129.226.0.0/16",
            "150.109.0.0/16"
        ],
        "notes": "Static Tencent Cloud heuristic."
    },
    {
        "provider_guess": "Scaleway",
        "asn_hint": "AS12876",
        "provider_type": "Cloud / VPS",
        "country_hint": "France / Europe",
        "confidence": "MEDIUM",
        "prefixes": [
            "51.15.0.0/16",
            "62.210.0.0/16",
            "163.172.0.0/16"
        ],
        "notes": "Static Scaleway heuristic."
    },
    {
        "provider_guess": "Leaseweb",
        "asn_hint": "AS60781",
        "provider_type": "VPS / Dedicated",
        "country_hint": "Netherlands / Global",
        "confidence": "MEDIUM",
        "prefixes": [
            "85.17.0.0/16",
            "95.211.0.0/16",
            "209.58.128.0/18"
        ],
        "notes": "Static Leaseweb heuristic."
    },
    {
        "provider_guess": "IONOS",
        "asn_hint": "AS8560",
        "provider_type": "VPS / Hosting",
        "country_hint": "Germany / Europe",
        "confidence": "MEDIUM",
        "prefixes": [
            "74.208.0.0/16",
            "82.165.0.0/16",
            "217.160.0.0/16"
        ],
        "notes": "Static IONOS heuristic."
    }
]


def detect_provider_hint(ip: str) -> dict:
    result = {
        "ip": ip,
        "provider_guess": "Unknown",
        "asn_hint": None,
        "provider_type": "Unknown",
        "country_hint": "Unknown",
        "confidence": "LOW",
        "detection_method": "static_prefix_heuristic",
        "notes": "No static provider hint matched. Use live ASN lookup for verification."
    }

    if not ip:
        return result

    try:
        parsed_ip = ip_address(ip)
    except ValueError:
        result["notes"] = "Invalid IP format."
        return result

    for provider in PROVIDER_HINTS:
        for prefix in provider["prefixes"]:
            if parsed_ip in ip_network(prefix):
                return {
                    "ip": ip,
                    "provider_guess": provider["provider_guess"],
                    "asn_hint": provider["asn_hint"],
                    "provider_type": provider["provider_type"],
                    "country_hint": provider["country_hint"],
                    "confidence": provider["confidence"],
                    "detection_method": "static_prefix_heuristic",
                    "matched_prefix": prefix,
                    "notes": provider["notes"]
                }

    return result
