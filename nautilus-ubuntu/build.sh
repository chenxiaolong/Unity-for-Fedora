#!/usr/bin/env bash

SPECFILE=nautilus-ubuntu.spec
MULTILIB=false
DO_NOT_INSTALL=('nautilus-ubuntu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
