from google_sheets import get_sheet_values
from collections import defaultdict
from opportunity_parsing import *

result = defaultdict(list)
vals = get_sheet_values('1s_EC5hn-A-yKFUYWKO3RZ768AVW9FL-DKNZ3QBb0tls', 'Recommendations')
headers = parse_headers(vals)


# for key, *values in data:
#     result[key].extend(values)