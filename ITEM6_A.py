---
- name: CONFIGURAR LOOPBACK33 - IPV6
 hosts: CSR1kv
 gather_facts: false
 connection: local

 tasks:
  - name: CONFIGURAR LOOPBACK33 - IPV6
    ios_config:
      parents: "interface loopback33"
      lines:
        - ipv6 address 3001:ABCD:ABCD:1::1/128
        - ipv6 address FE80::1 link-local

