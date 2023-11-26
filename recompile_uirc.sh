#!/bin/sh

set -x

pyuic5 forms/recordeditor.ui -o nto/forms/compiled/designed_record_editor.py
pyuic5 forms/relationtablechooser.ui -o nto/forms/compiled/relation_table_chooser.py
pyuic5 forms/mainscreen.ui -o nto/forms/compiled/main.py
pyuic5 forms/tableview.ui -o nto/forms/compiled/designed_table_view.py
pyuic5 forms/laborrequeststooltip.ui -o nto/forms/compiled/labor_requests_tooltip.py

pyuic5 forms/entertainmentdashboard.ui -o nto/forms/compiled/entertainment_dashboard.py
pyuic5 forms/educationdashboard.ui -o nto/forms/compiled/education_dashboard.py
pyuic5 forms/enlightenmentdashboard.ui -o nto/forms/compiled/enlightenment_dashboard.py

pyrcc5 resources/resources.qrc -o resources_rc.py
