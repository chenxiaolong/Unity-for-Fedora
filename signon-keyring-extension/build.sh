#!/usr/bin/env bash

SPECFILE=signon-keyring-extension.spec
MULTILIB=false
DO_NOT_INSTALL=('signon-keyring-extension-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
