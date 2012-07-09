#!/usr/bin/env bash

SPECFILE=python-compizconfig.spec
MULTILIB=false
DO_NOT_INSTALL=('python-compizconfig-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
