#!/usr/bin/env bash

SPECFILE=compizconfig-backend-gconf.spec
MULTILIB=false
DO_NOT_INSTALL=('compizconfig-backend-gconf-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
