# Open transit architecture design rationale

## Entity identifiers

For identifiers, we use RFC4122 compliant UUIDs version 4, represented as base57 strings.

In binary form they take up 16 bytes. In string representation - 22 characters. 

UUIDs were chosen because they are most widely known and standardized. 
They can handle arbitrary large datasets without collisions.
Auto-incrementing integers do not fit our requirements.

Base58 representation was chosen because it's more human-friendly and shorter than the
canonical hexadecimal representation (e.g. `6ba604a7-4fd9-4630-a0ed-4575fc3ca815`).
The character set is `23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz`
(no `0`, `1`, `I`, `O`, `l`). The canonical representation should not be used.
