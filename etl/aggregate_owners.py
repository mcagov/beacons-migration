def aggregate_owners(owners):
    result = []

    for owner in owners:
        for to_compare in owners:
            pk_keys = {owner.get('pk_beacon_owner_id')}
            match = _is_same_owner(owner, to_compare)
            if match:
                pk_keys.add(to_compare.get('pk_beacon_owner_id'))

            has_matched_owner = False
            for matched_owners in result:
                owner_details = matched_owners.get('owner')
                has_matched_owner = _is_same_owner(owner, owner_details)
                if has_matched_owner:
                    matched_owners['pk_keys'] |= pk_keys
                    break

            if not has_matched_owner:
                result.append({
                    'pk_keys': pk_keys,
                    'owner': {
                        key: value for key, value in owner.items() if key not in 'pk_beacon_owner_id'
                    }
                })

    return result


def _is_same_owner(owner, to_compare):
    return (owner.get('owner_name') == to_compare.get('owner_name')) and \
           (owner.get('company_name') == to_compare.get('company_name')) and \
           (owner.get('care_of') == to_compare.get('care_of')) and \
           (owner.get('address_1') == to_compare.get('address_1')) and \
           (owner.get('address_2') == to_compare.get('address_2')) and \
           (owner.get('address_3') == to_compare.get('address_3')) and \
           (owner.get('address_4') == to_compare.get('address_4')) and \
           (owner.get('country') == to_compare.get('country')) and \
           (owner.get('post_code') == to_compare.get('post_code')) and \
           (owner.get('phone_1') == to_compare.get('phone_1')) and \
           (owner.get('phone_2') == to_compare.get('phone_2')) and \
           (owner.get('mobile_1') == to_compare.get('mobile_1')) and \
           (owner.get('mobile_2') == to_compare.get('mobile_2')) and \
           (owner.get('fax') == to_compare.get('fax')) and \
           (owner.get('email') == to_compare.get('email'))
