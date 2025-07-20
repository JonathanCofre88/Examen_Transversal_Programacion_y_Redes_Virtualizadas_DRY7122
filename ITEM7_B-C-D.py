---
- name: VER COMANDOS SHOW EN ROUTER
  hosts: CSR1kv
  gather_facts: false
  connection: local

  tasks:
   - name: VER COMANDO SHOW INTERFACES - IP
     ios_command:
       commands:
        - show ip interface brief
     register: interfaz
   - name: GUARDAR RESULTADOS DE COMANDOS SHOW INTERFAZ - IP
     copy:
       content: "{{ interfaz.stdout[0] }}"
       dest: "./ITEM7_B_INT-IP_{{ inventory_hostname }}.txt"

   - name: VER COMANDO SHOW RUNNING-CONFIG
     ios_command:
       commands:
        - show running-config
     register: run
   - name: GUARDAR RESULTADOS SHOW RUNNING-CONFIG
     copy:
       content: "{{ run.stdout[0] }}"
       dest: "./ITEM7_C_SH-RUN_{{ inventory_hostname }}.txt"

   - name: VER COMANDO SHOW VERSION
     ios_command:
       commands:
        - show version
     register: version
   - name: GUARDAR RESULTADOS DE COMANDOS SHOW VERSION
     copy:
       content: "{{ version.stdout[0] }}"
       dest: "./ITEM7_D_SH-VER{{ inventory_hostname }}.txt"

