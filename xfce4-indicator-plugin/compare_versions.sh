#!/usr/bin/env bash

SPECFILE=xfce4-indicator-plugin.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
UPSTREAM_VER=$(wget -q "http://goodies.xfce.org/projects/panel-plugins/xfce4-indicator-plugin" -O - | sed -n 's/.*xfce4-indicator-plugin-\(.*\)\.tar\..*/\1/p' | head -n 1)
echo -e "Upstream version:  ${UPSTREAM_VER}"
echo -e "Ubuntu version:    $(get_ubuntu_version xfce4-indicator-plugin ${1:-raring})"
