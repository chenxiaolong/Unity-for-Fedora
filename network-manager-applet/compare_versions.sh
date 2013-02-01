#!/usr/bin/env bash

SPECFILE=network-manager-applet-ubuntu-Fedora_18.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) git$(get_spec_define _git_date)"
echo -e "Fedora version:    $(get_fedora_version network-manager-applet 18)"
echo -e "Upstream version:  $(get_gnome_version network-manager-applet 0.9)"
echo -e "Ubuntu version:    $(get_ubuntu_version network-manager-applet ${1:-raring})"
