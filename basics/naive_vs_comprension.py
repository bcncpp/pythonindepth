from typing import Iterable, Set
import re
import timeit
from functools import partial

# Add named capture group for account_id
ARN_REGEX = r"^arn:aws:[\w-]+:[\w-]*:(?P<account_id>\d{12}):.+$"

def generate_fake_arns(service="s3", region="us-east-1", resource_type="bucket", resource_prefix="test-bucket", count=10000):
    arns = []
    for i in range(count):
        account_id = f"{100000000000 + i}"  # 12-digit account ID
        resource_name = f"{resource_prefix}-{i}"
        arn = f"arn:aws:{service}:{region}:{account_id}:{resource_type}/{resource_name}"
        arns.append(arn)
    return arns

def collect_account_ids_from_arns(arns: Iterable[str]) -> Set[str]:
    collected_account_ids = set()
    for arn in arns:
        matched = re.match(ARN_REGEX, arn)
        if matched is not None:
            account_id = matched.groupdict()["account_id"]
            collected_account_ids.add(account_id)
    return collected_account_ids

def collect_account_ids_from_arns_1(arns: Iterable[str]) -> tuple[str]:
    data =  (
        matched.groupdict()["account_id"]
        for arn in arns
        if (matched := re.match(ARN_REGEX, arn))
    )
    return data

"""
 The partial() is used for partial function application which “freezes” some portion of a function’s arguments and/or keywords resulting in a new object with a simplified signature. For example, partial() can be used 
 to create a callable that behaves like the int() function where the base argument defaults to two:
"""

if __name__ == "__main__":
    fake_arns = generate_fake_arns()
    bad_code = partial(collect_account_ids_from_arns, fake_arns)
    clean_code = partial(collect_account_ids_from_arns_1, fake_arns)
    bad_code_timing = timeit.timeit(bad_code, number=100)
    print(f"Bad code timing: {bad_code_timing:.6f} seconds")
    clean_code_timing = timeit.timeit(clean_code, number=100)
    print(f"Clean code timing: {clean_code_timing:.6f} seconds")
