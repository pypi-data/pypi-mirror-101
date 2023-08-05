# -*- coding: utf-8 -*-

"""Tests for cvsser"""

import cvsser
import pytest

# Test usage as a guide only
def test_guide():
    assert cvsser.VectorString(guide_only=True).guide["v3.1"]["E"]["name"] == 'Exploit Code Maturity'

# Test valid CVSS v2.0 string
v2_sample = "AV:N/AC:L/Au:S/C:P/I:P/A:N"
def test_valid_v2():
    assert cvsser.VectorString(v2_sample).availability_impact == 'N'
    assert cvsser.VectorString(v2_sample).to_dict(style='verbose', parentheticals='both', include='all')["AR"]["value"] == 'Not Defined (ND)'

# Test valid CVSS v3.0 string
v3_sample = "CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C"
def test_valid_v3():
    assert cvsser.VectorString(v3_sample).av == 'L'
    assert cvsser.VectorString(v3_sample).to_dict(style='default', include='all')["MUI"]["value"] == 'X'

# Test invalid CVSS v3.0 string
v3_invalid = "CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H/E:U/RL:O/RC:"
def test_invalid_v3():
    with pytest.raises(ValueError) as execinfo:
        vs = cvsser.VectorString(v3_invalid)







