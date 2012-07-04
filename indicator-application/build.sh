#!/usr/bin/env bash

SPECFILE=indicator-application.spec
MULTILIB=false
DO_NOT_INSTALL=('indicator-application-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
