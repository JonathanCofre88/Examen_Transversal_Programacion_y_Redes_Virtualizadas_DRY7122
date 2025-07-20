---
- name: CONFIGURAR ROUTER
  hosts: CSR1kv
  gather_facts: false
  connection: local

  tasks:
   - name: EIGRP NOMBRADA
     ios_config:
       lines:
        - router eigrp EXAMENT
        - address-family ipv4 autonomous-system 100
        - af-interface Loopback33
        - passive-interface
        - exit-address-family
        - address-family ipv6 autonomous-system 100
        - af-interface Loopback33
        - passive-interface
        - exit-address-family

   - name: RESULTADO DE EIGRP
     ios_command:
       commands:
        - show running-config | section eigrp 
     register: eigrp

   - name: GUARDAR RESULTADO EIGRP
     copy:
       content: "{{ eigrp.stdout[0] }}"
       dest: "./ITEM7_A-eigrp_{{ inventory_hostname }}.txt"

