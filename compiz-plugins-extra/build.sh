#!/usr/bin/env bash

SPECFILE=compiz-plugins-extra.spec
MULTILIB=false
DO_NOT_INSTALL=('compiz-plugins-extra-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
