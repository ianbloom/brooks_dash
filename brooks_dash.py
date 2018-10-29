# PLACEHOLDER

# first check if there is a 'Devices by Type' folder
    # If not then make one

# Apply apiaccessid.key and apiaccesskey.key to 'Devices by Type'

# Import 'DataSource List' PropertySource

# Devices > Devices by Type: Use API to auto-create dynamic groups as we discussed, with relevant "Auto Assign" verbiage (below is a semi-complete list of the folders with their auto-assign syntax). For example, it should be:
# Devices by Type
# Active Directory
# Apache
# APC
# Aruba
# Brocade
# Checkpoint
# Cisco
# Cisco ASA
# Cisco Nexus
# Cisco UCS
# Cisco CUCM
# Cisco Wireless
# Citrix
# Citrix Netscaler
# Citrix XenApp
# Collectors
# EMC

from api_helpers.super_func import *
from api_helpers.lm_api import *
from pprint import pprint
import argparse
import os
import sys

lm_id      = "wv2NAH8BGTqz7p2YEHHV"
lm_key     = "J}HH5=_Kc]SW53jd=kEc8t3[6P!L!E$ZgX8ui2x("
lm_account = "ianbloom"

# First, let's check if there is a Devices by Type folder
name = 'Devices by Type'
return_dict = SUBGROUP_GETTER_NAME(lm_id, lm_key, lm_account, name)

# Check if there are any items in API response
if(return_dict['body']['total'] == 0):
    # Devices by Type doesn't exist so insttantiate it
    return_dict = SUBGROUP_POSTER_NAME(lm_id, lm_key, lm_account, name)
    d_b_t_id = return_dict['body']['id']
else:
    # Devices by Type does exist so get it's ID
    # Assume no collisions so use first element of items array
    d_b_t_id = return_dict['body']['items'][0]['id']

# Now add dbt_api_id.key and dbt_api_key.key
SUBGROUP_PROPS(lm_id, lm_key, lm_account, d_b_t_id)

