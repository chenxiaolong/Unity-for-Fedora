#!/usr/bin/env bash

SPECFILE=utouch-grail.spec
MULTILIB=true
MULTILIB_PACKAGES=('utouch-grail' 'utouch-grail-devel')
DO_NOT_INSTALL=('utouch-grail-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
