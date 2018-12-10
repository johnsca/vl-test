from charms.reactive import when_not, is_flag_set

from charms.layer import status


@when_not('always')
def update_status():
    if not is_flag_set('vault.connected'):
        status.blocked('missing relation to vault')
        return
    if not is_flag_set('layer.vaultlocker.configured'):
        status.waiting('waiting for vaultlocker config')
        return
    ready, missing = [], []
    for storage in ('secrets',
                    'secrets/0',
                    'multi-secrets',
                    'multi-secrets/0',
                    'multi-secrets/1',
                    'multi-secrets/2'):
        if is_flag_set('layer.vaultlocker.{}.ready'.format(storage)):
            ready.append(storage)
        else:
            missing.append(storage)
    status.active('ready: {}; missing: {}'.format(','.join(ready),
                                                  ','.join(missing)))
