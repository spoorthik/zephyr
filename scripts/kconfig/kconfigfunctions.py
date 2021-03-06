#
# Copyright (c) 2018-2019 Linaro
# Copyright (c) 2019 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import os

# Types we support
# 'string', 'int', 'hex', 'bool'

doc_mode = os.environ.get('KCONFIG_DOC_MODE') == "1"
bin_dir = os.environ.get('PROJECT_BINARY_DIR')
conf_file = os.path.join(bin_dir, 'include', 'generated',
                         'generated_dts_board.conf') if bin_dir else None

dt_defines = {}
if (not doc_mode) and conf_file and os.path.isfile(conf_file):
    with open(conf_file, 'r', encoding='utf-8') as fd:
        for line in fd:
            if '=' in line:
                define, val = line.split('=')
                dt_defines[define] = val.strip()

def _dt_units_to_scale(unit):
    if not unit:
        return 0
    if unit in {'k', 'K'}:
        return 10
    if unit in {'m', 'M'}:
        return 20
    if unit in {'g', 'G'}:
        return 30

def dt_int_val(kconf, _, name, unit=None):
    """
    This function looks up 'name' in the DTS generated "conf" style database
    and if its found it will return the value as an decimal integer.  The
    function will divide the value based on 'unit':
        None        No division
        'k' or 'K'  divide by 1024 (1 << 10)
        'm' or 'M'  divide by 1,048,576 (1 << 20)
        'g' or 'G'  divide by 1,073,741,824 (1 << 30)
    """
    if doc_mode or name not in dt_defines:
        return "0"

    d = dt_defines[name]
    if d.startswith(('0x', '0X')):
        d = int(d, 16)
    else:
        d = int(d)
    d >>= _dt_units_to_scale(unit)

    return str(d)

def dt_hex_val(kconf, _, name, unit=None):
    """
    This function looks up 'name' in the DTS generated "conf" style database
    and if its found it will return the value as an hex integer.  The
    function will divide the value based on 'unit':
        None        No division
        'k' or 'K'  divide by 1024 (1 << 10)
        'm' or 'M'  divide by 1,048,576 (1 << 20)
        'g' or 'G'  divide by 1,073,741,824 (1 << 30)
    """
    if doc_mode or name not in dt_defines:
        return "0x0"

    d = dt_defines[name]
    if d.startswith(('0x', '0X')):
        d = int(d, 16)
    else:
        d = int(d)
    d >>= _dt_units_to_scale(unit)

    return hex(d)


functions = {
        "dt_int_val": (dt_int_val, 1, 2),
        "dt_hex_val": (dt_hex_val, 1, 2),
}
