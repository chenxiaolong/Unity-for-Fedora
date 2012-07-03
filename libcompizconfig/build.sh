#!/usr/bin/env bash

SPECFILE=libcompizconfig.spec
MULTILIB=false
DO_NOT_INSTALL=('libcompizconfig-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
