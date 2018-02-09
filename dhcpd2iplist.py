# Parse an ISC DHCPD leases file to find active addresses
#
# TODO: Check times. This currently only checks for active leases, but they
# may have expired without the leases file updating (for example, after a copy
# of the file has sat for a while before processing).

import sys
addrs = []
inlease = False
for line in sys.stdin:
    if line.startswith("#"):
        continue
    if len(line) == 0:
        continue
    if line.startswith("lease"):
        # TODO error checking
        inlease = True
        address = line.split()[1]
        state = None
    if  line.strip().startswith("binding state "):
        state = line.split()[2].strip(";")
    if line.strip() == "}":
        if not inlease:
            raise Exception("parse error")
        inlease = False
        if state is None:
            raise Exception("Missing state?")
        if state == "active":
            if address in addrs:
                print >>sys.stderr, "Address", address, "already in list"
            else:
                addrs.append(address)
        elif state == "free":
            if address in addrs:
                print >>sys.stderr, "Address", address, "removed"
                addrs.remove(address)
        else:
            raise Exception("Unknown state '%s'" % state)
for i in sorted(addrs):
    print i


