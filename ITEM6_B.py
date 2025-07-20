---
- name: RESPALDO CONFIGURACION
 hosts: CSR1kv
 gather_facts: false
 connection: local

 tasks:
  - name: RESPALDO CONFIGURACION
    ios_command:
      commands:
        - show running-config 

    register: config
  - name: VER RESPALDO DE CONFIGURACION
    copy:
      content: "{{ config.stdout[0] }}"
      dest: "./Respaldo_{{ inventory_hostname }}.txt"

