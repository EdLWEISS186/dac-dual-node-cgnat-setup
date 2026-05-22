# Advanced CGNAT Dual-Node Setup

Detailed guide for running stable DAC nodes behind CGNAT using Dual-Node Single Machine architecture.

---

## Network Topology

    Internet
       └── Router (CGNAT)
             └── Single Physical Machine
                   ├── Windows (Node 1 - Primary)
                   └── WSL2 Ubuntu (Node 2 - Secondary)

---

## Why This Setup Excels

- Bypasses many CGNAT restrictions through internal peering
- Maximizes hardware resources on a single machine
- Provides redundancy
- Improves overall stability

---

## Key Configurations

- Static peering (internal + external)
- Fast syncmode strategy
- Auto-restart scripts
- Resource optimization between Windows and WSL2

---

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Low peer count | CGNAT restrictions | Use static peering + internal connection |
| Frequent disconnects | Resource contention | Optimize allocation + auto-restart |
| Slow synchronization | Storage / bandwidth | Use NVMe SSD + `fast` syncmode |
| High CPU/RAM usage | Dual nodes competing | Fine-tune limits between OS |

---

## Best Practices

- Maintain high uptime
- Monitor resource usage continuously
- Implement auto-restart on both OS
- Use internal IP for peering
- Keep nodes updated
- Backup configuration files

---

## References

- DAC Dual Node CGNAT Setup Repository
