"""
ELB EC2-Classic utils
"""
import boto3

from utils import resolve_host


def get_info():
    result = []
    client = boto3.client('elb')

    data = client.describe_load_balancers()

    while data:
        next_marker = data.get('NextMarker')

        for description in data.get('LoadBalancerDescriptions', []):
            if description.get('Scheme') == 'internet-facing':
                result.append({
                    'elb_id': description.get('CanonicalHostedZoneNameID'),
                    'elb_public_ip': resolve_host(description.get('DNSName')),
                    'elb_public_dns_name': description.get('DNSName'),
                })

        data = client.describe_load_balancers(Marker=next_marker) if next_marker is not None else None

    return result