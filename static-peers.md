# Static Peer Configuration

Static peers are manually specified to ensure stable, persistent connections without relying on peer discovery — especially critical under CGNAT conditions.

---

## Internal Peers (Windows ↔ WSL)

### WSL Node → Windows Node

```
enode://<WINDOWS_ENODE>@192.168.100.7:28657
```

### Windows Node → WSL Node

```
enode://<WSL_ENODE>@192.168.100.7:30304
```

> **How to obtain enode:** Run `admin.nodeInfo.enode` in the node console of each respective node, then substitute the value above.

---

## Official DAC Testnet Nodes

The following are the DAC authority nodes used as primary external peers:

| # | IP Address       | Role            |
|---|------------------|-----------------|
| 1 | 157.173.127.30   | Authority Node  |
| 2 | 157.173.127.21   | Authority Node  |
| 3 | 157.173.127.31   | Authority Node  |

---

## Configuration File

Add the following to your `static-nodes.json` in each node's datadir:

```json
[
  "enode://<WINDOWS_ENODE>@192.168.100.7:28657",
  "enode://<WSL_ENODE>@192.168.100.7:30304",
  "enode://<OFFICIAL_ENODE_1>@157.173.127.30:30303",
  "enode://<OFFICIAL_ENODE_2>@157.173.127.21:30303",
  "enode://<OFFICIAL_ENODE_3>@157.173.127.31:30303"
]
```

> Replace each `<..._ENODE>` with the actual enode public key obtained from each node or from the official DAC documentation.

---

## Notes

- Internal peers use the Windows host IP (`192.168.100.7`) for both nodes since WSL routes through the host.
- Official node ports may vary — verify against the latest DAC testnet documentation.
- Static peers take priority over dynamic peer discovery.
