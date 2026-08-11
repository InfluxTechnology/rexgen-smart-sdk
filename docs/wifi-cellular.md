# WiFi And Cellular Connectivity

Confirmed by direct inspection of a live Rexgen Smart unit (serial console, `imx8mm-smart`, `REX01-A1-B001` family) — every path/interface/service name below is what's actually running, not a generic Linux tutorial.

## Overview

The platform has three independent network paths, plus an automatic failover mechanism between WiFi and cellular:

| Interface | Role | Managed by |
|---|---|---|
| `eth0` | Wired Ethernet | systemd-networkd |
| `wlan1` | WiFi Access Point (2.4GHz, WPA2-PSK) | `hostapd` + `dnsmasq` |
| `wlan0` | WiFi client/station | `wpa_supplicant@wlan0.service` |
| `ppp0` | Cellular (LTE) | `pppd` via `lte-ppp.service`, Quectel EC25 modem |

Both WiFi and cellular are primarily configured through the **ReXgen Netservices Dashboard**, a web UI shipped on the device — not by hand-editing `hostapd.conf`/`wpa_supplicant.conf` directly (those files are generated/rewritten by the dashboard's backend services).

## ReXgen Netservices Dashboard

- **Access:** `http://<device-ip>/` — served by `wifi-dashboard.service` (Flask app at `/opt/influx/netservices/dashboard/app.py`), plain HTTP on port 80 by default. HTTPS can be enabled from the dashboard's own settings (`dashboard.https_enabled` in its config) — see the security note below before doing that.
- **Login:** dashboard-local username/password (stored as a salted `scrypt` hash in `/data/rexgen/config/netservices.conf`, not the device's Linux/SSH credentials).
- **What it configures**, all persisted to a single JSON file at `/data/rexgen/config/netservices.conf`, which the backing services (`wifi-manager.service`, `hostapd`, `dnsmasq`) read from:
  - **AP settings** — the `wlan1` access point's PSK
  - **Client (STA) networks** — a list of SSIDs/PSKs for `wlan0` to join
  - **DNS servers** — resolver list and options
  - **System** — including an **SSH enable/disable toggle** (`system.ssh_enabled`) — this is the supported way to turn off SSH access referenced in [SECURITY.md](../SECURITY.md#hardening-checklist-before-non-lab-deployment)'s hardening checklist
  - Dashboard theme/language, Mender artifact tracking

## WiFi Access Point (`wlan1`)

- Service: `hostapd.service`, running `/usr/sbin/hostapd /etc/hostapd.conf`
- Mode: 2.4GHz (`hw_mode=g`), channel 1, WPA2-PSK (`wpa=2`, `wpa_key_mgmt=WPA-PSK`, `rsn_pairwise=CCMP`)
- SSID: defaults to the device's own ID (e.g. `REX01_A1_B001_SN0000002`) — set per-unit, not a fixed shared value
- The PSK in `/etc/hostapd.conf` (`wpa_psk=...`) is the raw 256-bit derived key, not a plaintext password — the dashboard stores/writes it the same way, never the plaintext passphrase, in `netservices.conf`'s `ap.ap_psk`
- Network: `dnsmasq` (drop-in config at `/etc/dnsmasq.d/rexgen-ap.conf`) serves DHCP + DNS on `wlan1`:
  - Gateway/DNS: `192.168.51.1` (interface address)
  - DHCP range: `192.168.51.2`–`192.168.51.40`, 24h lease
  - `address=/#/192.168.51.1` — wildcard DNS answer, so any hostname resolves to the device itself (captive-portal-style)

There is also an alternate profile, `/etc/hostapd-wifi6.conf` (5GHz/6GHz-capable, `ieee80211ax=1`, WPA3-SAE) — **present on disk but not wired into any active service** on this unit; `hostapd.service` only ever launches with `/etc/hostapd.conf`. Treat it as a template/reference for a WiFi 6 / WPA3 setup, not something active by default.

## WiFi Client / Station Mode (`wlan0`)

- Service: `wpa_supplicant@wlan0.service`, driven by `wifi-manager.service` (`/opt/influx/netservices/services/wifi_manager.py`)
- `/etc/wpa_supplicant.conf` on disk is a minimal template (`update_config=1`, one empty `network={ key_mgmt=NONE }` block) — the dashboard's `wifi_manager.py` rewrites/manages the actual saved-network list dynamically from `netservices.conf`'s `sta.networks` array (each entry: SSID + derived PSK, matching the AP's convention of never storing plaintext)
- To join a network: add it via the dashboard's WiFi settings page, not by hand-editing `wpa_supplicant.conf`

## Cellular (LTE)

- Modem: Quectel **EC25-EUX** (LTE Cat 4), visible on the host as `/dev/serial/by-id/usb-Quectel_EC25-EUX_...-if0{0,1,2,3}-port0` (also enumerated as `/dev/ttyUSB0`–`/dev/ttyUSB3` internally — unrelated to any external USB-serial console cable a developer might use, which is a separate physical connection)
- Service: `lte-ppp.service` → `pppd call quectel-ppp nodetach`
- Peer config: `/etc/ppp/peers/quectel-ppp` — modem on `/dev/ttyUSB3`, 115200 baud, `defaultroute`, `usepeerdns`, persistent (`persist`, `maxfail 0`)
- Auth: `user $LTE_USERNAME` / `password $LTE_PASSWORD` — read from environment; many IoT SIMs (e.g. 1NCE) don't require real credentials, so these can be blank/wildcard depending on your SIM/provider
- Chat script: `/etc/ppp/peers/quectel-chat-connect` runs standard modem bring-up (`ATE0`, `AT+CSQ` signal check, `AT+CPIN?` SIM status, `AT+CGREG?` registration, `AT+CGDCONT=1,"IP",""` — blank APN, i.e. network-assigned) then dials `ATDT*99#`
- There is also an older/alternate `wvdial`-based path (`/etc/wvdial.conf`, `/etc/ppp/peers/wvdial*`) referencing a `1nce`-named dialer profile on `/dev/ttymxc2` — present on disk but **`lte-ppp.service` uses the `quectel-ppp` peer on `/dev/ttyUSB3`, not wvdial**; the wvdial files look like a legacy/alternate configuration for a different modem wiring, not what's currently active

## Automatic WiFi/Cellular Failover

`net-failover.timer` runs `/opt/influx/net_failover.sh` every 20 seconds:

1. Adds a temporary host route to `9.9.9.9` via `wlan0`'s gateway, pings it (2 attempts, 2s timeout).
2. If the ping **fails**: removes any `wlan0` default route and adds a default route via `ppp0` — traffic fails over to cellular.
3. If the ping **succeeds**: removes any `ppp0` default route and ensures `wlan0`'s default route is present (metric 10) — traffic uses WiFi.
4. Logs each switch to `/var/log/net_failover.log`.

This means WiFi (`wlan0`, client mode) is preferred whenever it's reachable; cellular is the automatic fallback, checked roughly every 20 seconds — not something you need to configure manually.

## Security Note

`/opt/influx/netservices/ssl/ca.crt`/`ca.key` (used for the dashboard's optional HTTPS mode) have a fixed on-disk modification timestamp (`2018-03-09`) that doesn't correspond to this device's actual provisioning date — a strong indicator this CA private key is baked into every image rather than generated per-device at first boot. If confirmed (compare across two units), this is the same class of issue as the shared credentials documented in [SECURITY.md](../SECURITY.md#current-credential-posture-influx-image-base): enabling HTTPS on the dashboard today would mean every device in the fleet presents the same CA-signed identity, so a private key compromised from one device (or extracted from the image itself) would let someone impersonate the dashboard's HTTPS on any unit. Until confirmed/fixed, prefer leaving `dashboard.https_enabled` off, or generate a unique cert per device before enabling it.
