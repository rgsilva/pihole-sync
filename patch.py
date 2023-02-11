import os
import os.path

class PatchError(Exception):
    pass


def _disable_dhcp(root: str):
    setup_vars = os.path.join(root, "setupVars.conf")
    if not os.path.isfile(setup_vars):
        raise PatchError("setup vars is missing")

    with open(setup_vars, "r") as f:
        contents = f.read()
    contents = contents.replace("DHCP_ACTIVE=true", "DHCP_ACTIVE=false")
    with open(setup_vars, "w") as f:
        f.write(contents)

    pihole_dhcp = os.path.join(root, "dnsmasq.d/02-pihole-dhcp.conf")
    if os.path.isfile(pihole_dhcp):
        os.remove(pihole_dhcp)

    dhcp_leases = os.path.join(root, "dhcp.leases")
    if os.path.isfile(dhcp_leases):
        with open(dhcp_leases, "w") as f:
            f.write("")


def _disable_ptr(root: str):
    setup_vars = os.path.join(root, "setupVars.conf")
    if not os.path.isfile(setup_vars):
        raise PatchError("setup vars is missing")

    with open(setup_vars, "r") as f:
        contents = f.readlines()
    contents = [line for line in contents if not line.startswith("PIHOLE_PTR=")]
    contents += ["PIHOLE_PTR=NONE\n"]
    contents = "".join(contents)
    with open(setup_vars, "w") as f:
        f.write(contents)


_patches = {
    "disable-dhcp": _disable_dhcp,
    "disable-ptr": _disable_ptr,
}

def run_patches(path: str, wanted: list[str]) -> list[str]:
    applied = []
    for id in wanted:
        if id in _patches:
            _patches[id](path)
            applied.append(id)
    return applied
