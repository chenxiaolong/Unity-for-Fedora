#!/usr/bin/env bash

SPECFILE=utouch-evemu.spec
MULTILIB=true
MULTILIB_PACKAGES=('utouch-evemu' 'utouch-evemu-devel')
DO_NOT_INSTALL=('utouch-evemu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
