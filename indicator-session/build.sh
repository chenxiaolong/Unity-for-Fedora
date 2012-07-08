#!/usr/bin/env bash

SPECFILE=indicator-session.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-session-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
