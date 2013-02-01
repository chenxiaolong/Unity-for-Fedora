#!/usr/bin/env bash

SPECFILE=NetworkManager-gnome-ubuntu-Fedora_17.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version) Fedora $(get_spec_define _fedora_rel).git$(get_spec_define _git_date) Ubuntu $(get_spec_define _ubuntu_ver) $(get_spec_define _ubuntu_rel)"
echo -e "Fedora version:    $(get_fedora_version NetworkManager 17)"
echo -e "Upstream version:  $(get_gnome_version network-manager-applet 0.9)"
echo -e "Ubuntu version:    $(get_ubuntu_version network-manager-applet ${1:-quantal})"
