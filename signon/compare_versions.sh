#!/usr/bin/env bash

SPECFILE=signon.spec

source "$(dirname ${0})/../version_checker.sh"

echo -e "spec file version: $(get_spec_version)"
echo -e "Upstream version:  $(get_googlecode_version accounts-sso signon)"
echo -e "Ubuntu version:    $(get_ubuntu_version signon ${1:-raring})"
