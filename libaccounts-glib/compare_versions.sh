#!/usr/bin/env bash

SPECFILE=libaccounts-glib.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_googlecode_version accounts-sso libaccounts-glib)"
echo -e "Ubuntu version:    $(get_ubuntu_version libaccounts-glib ${1:-raring})"
