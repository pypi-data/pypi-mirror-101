
test0:
  test.fail_with_changes:
    - name: asdfasdf

test1:
  file.managed:
    - name: /tmp/x.conf
    - source: salt://odoo/templates/odoo.service
