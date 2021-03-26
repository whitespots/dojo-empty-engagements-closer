import requests
import os
import concurrent.futures

dojo_token = os.environ.get('DOJO_TOKEN', '113h5gk24j5h2k4j5h2k4j5')
dojo_base_url = os.environ.get('DOJO_BASE_URL', 'https://dojo.site.com')

auth_headers = {
    'Authorization': f'Token {dojo_token}'
}

engagements_api_url = f'{dojo_base_url}/api/v2/engagements/?limit=400&active=true'
tests_api_url = f'{dojo_base_url}/api/v2/tests/?limit=800'
findings_api_url = f'{dojo_base_url}/api/v2/findings/?limit=80000'

engagements_to_close = requests.get(
    engagements_api_url,
    headers=auth_headers,
).json().get('results')

tests = requests.get(
    tests_api_url,
    headers=auth_headers,
).json()

findings = requests.get(
    findings_api_url,
    headers=auth_headers,
    timeout=60
).json()


def close_ci_engagement(id):
    engagement_close_status = requests.post(
        url=f'{dojo_base_url}/api/v2/engagements/{id}/close/',
        headers=auth_headers
    ).status_code

    if engagement_close_status == 200:
        print(f'Closing {id}: success')
        return True
    else:
        print(f'Closing {id}: failure')
        return False


# Detect only really required for closing engagements
# We don't need to close non-empty engagements
checked_tests = []
engagements_to_keep = []
for finding in findings.get('results'):
    test_id = finding.get('test')
    if test_id not in checked_tests:
        checked_tests.append(test_id)
        try:
            engagement_id = list(filter(lambda item: item.get('id') == test_id, tests.get('results'))).pop().get(
                'engagement')
            engagements_to_keep.append(engagement_id)
        except:
            print('Someone removed the test without removing a finding')

# Remove engagements with completed status and non ci type
for engagement in engagements_to_close:
    if engagement.get('id') in engagements_to_keep or \
            engagement.get('status') == 'Completed' or \
            engagement.get('engagement_type') != 'CI/CD':
        engagements_to_close.remove(engagement)

# Begin closing
print(f'Start closing {len(engagements_to_close)} engagements')
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    list(map(lambda engagement: close_ci_engagement(engagement.get('id')), engagements_to_close))

print('Done')