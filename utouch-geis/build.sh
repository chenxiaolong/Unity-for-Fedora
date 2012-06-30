#!/usr/bin/env bash

SPECFILE=utouch-geis.spec
MULTILIB=true
MULTILIB_PACKAGES=('utouch-geis' 'utouch-geis-devel')
DO_NOT_INSTALL=('utouch-geis-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
