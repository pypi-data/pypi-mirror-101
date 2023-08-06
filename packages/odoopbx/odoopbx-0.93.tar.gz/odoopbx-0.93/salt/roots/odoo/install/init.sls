{%- from "odoo/map.jinja" import odoo with context -%}

include:
  - .server
  - .addons
  - .frontend

odoo-service-start:
  service.running:
    - name: odoo{{ odoo.major_version }}
    - enable: true
    - onlyif:
        - runlevel
    - require:
      - cmd: odoo-addons-init
