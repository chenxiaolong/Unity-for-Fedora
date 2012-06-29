#!/usr/bin/env bash

SPECFILE=utouch-frame.spec
MULTILIB=true
MULTILIB_PACKAGES=('utouch-frame' 'utouch-frame-devel')
DO_NOT_INSTALL=('utouch-frame-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
