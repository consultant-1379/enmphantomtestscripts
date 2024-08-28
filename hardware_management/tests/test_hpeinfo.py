import hpeinfo


def test_getLMS_firmware():
    assert hpeinfo.getLMS_Firmware =="2.72"
def teset_getLMS_bios():
    assert hpeinfo.BiosVersion == "U32 v2.22 (11/13/2019)"

