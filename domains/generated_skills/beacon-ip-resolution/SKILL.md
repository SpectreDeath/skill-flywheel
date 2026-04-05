---
name: beacon-ip-resolution
description: "Use when: post-processing beacon XML (RSI) files to resolve internal VPN tunnel IPs to external VPS IPs. Triggers: 'IP resolution', 'RSI parsing', 'VPN mapping', 'ifconfig parsing', 'beacon classification'. NOT for: real-time processing (use beacon-management-gateway), or when IPs are already resolved."
---

# Beacon Post-Processing IP Resolution

## Overview

Python post-processing pipeline that reads RSI XML beacon files, extracts network interface information from platform-specific `ifconfig` output, matches interfaces to gateway addresses to identify the correct external IP, and remaps internal VPN tunnel IPs to the actual VPS public IPs.

## Processing Flow

```
[RSI XML File]
       |
  1. Extract IP, addressString, MAC, OS, hiveVersion
       |
  2. Parse ifconfig output (platform-specific)
     - Linux:   "Link encap", "inet addr:", "HWaddr"
     - Solaris: "<" flags, "inet", "ether"
     - MikroTik: "<" flags, "inet addr:\t", "HW addr:\t"
       |
  3. Extract gateway from netstat -rn
     - Linux:   "^0.0.0.0" with "UG"
     - Solaris: "^default" with "UG"
     - MikroTik: "^0.0.0.0" (offset 1) with "UG"
       |
  4. Match gateway subnet to interfaces
       |
  5. Map internal VPN IP to external VPS IP
       |
  6. Write to beacons/ (good) or e_beacons/ (bad)
```

## Platform-Specific ifconfig Parsing

```python
class Interface:
    def __init__(self, name, ipv4_Address, macAddress, ipv6_Address):
        self.name = name
        self.ipv4_Address = ipv4_Address
        self.macAddress = macAddress.lower() if macAddress else macAddress
        self.ipv6_Address = ipv6_Address

# Linux ifconfig format
if 'Link encap' in line:
    interface = line.split()[0]
if 'inet addr' in line:
    ip = line.split()[1].replace('addr:', '')
if 'HWaddr' in line:
    mac = line.split()[4]

# Solaris ifconfig format
if '<' in line and 'flags' in line:
    interface = line.split(':')[0]
if 'inet ' in line and 'inet6' not in line:
    ip = line.split()[1]
if 'ether' in line:
    mac = line.split()[1]

# MikroTik ifconfig format
if ' &lt;' in line:
    interface = line.split(': &lt;')[0]
if 'inet addr:\t' in line:
    ip = line.split()[2]
if 'HW addr:\t' in line:
    mac = line.split()[2]
```

## Gateway-Based IP Matching

```python
# Match gateway subnet to interface IPs
# Gateway: 10.177.76.1 → look for 10.177.76.x interfaces

bestmatch = gateway.split('.')
secondBestMatch = bestmatch[0]+"."+bestmatch[1]+"."+bestmatch[2]
thirdBestMatch = bestmatch[0]+"."+bestmatch[1]

for iface in interfaceList:
    if bestPossibleMatch in iface.getIpv4Address():
        externalIP.append(iface.getIpv4Address())
    elif secondBestMatch in iface.getIpv4Address():
        externalIP.append(iface.getIpv4Address())
```

## Internal-to-External IP Mapping

```python
# VPN tunnel IP → VPS public IP mapping
VPS_MAP = {
    '10.177.76.14': '82.221.131.100',
    '10.177.76.18': '78.138.97.145',
    '10.177.76.22': '192.99.0.128',
    '10.177.76.26': '201.218.252.110',
    '10.177.76.30': '186.193.44.130',
    '10.177.77.34': '190.120.236.211',
    '10.177.77.38': '193.34.145.82',
    '10.177.77.42': '31.210.100.208',
    '10.177.77.46': '103.8.24.143',
    '10.177.77.50': '46.108.130.10',
}

# In postProcessFile:
if '<IP>' in line:
    newIP = VPS_MAP.get(vps_IP, vps_IP)
    outfile.write(line.replace(oldIp, newIP))
```

## Beacon Classification

```python
def postProcessFile(inputFile, goodDir, badDir, results):
    if results['error'] is not None:
        # Bad beacon: old version, no gateway, parsing failure
        os.system("mv %s %s" % (inputFile, badDir))
    else:
        # Good beacon: rewrite with resolved IPs, move to goodDir
        # ... IP replacement logic ...
        os.system("rm %s" % inputFile)
```

## Constraints

- MUST detect platform type from beacon OS field before parsing ifconfig
- MUST handle all three ifconfig output formats (Linux, Solaris, MikroTik)
- MUST classify beacons with missing gateway as bad (unresolvable)
- MUST classify beacons with hiveVersion < 2.4 as bad (missing extraData)
- SHOULD use subnet matching with fallback granularity (full → /24 → /16 → /8)
- MUST log all processing results with timestamp for operational tracking
- MUST preserve original beacon files before modification (copy to beacons/ first)
- ALWAYS update addressString with the gateway-matched interface IP
