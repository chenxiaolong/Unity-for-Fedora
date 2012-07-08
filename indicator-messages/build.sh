#!/usr/bin/env bash

SPECFILE=indicator-messages.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-messages-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
