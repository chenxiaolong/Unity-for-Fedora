#!/usr/bin/env bash

SPECFILE=signon-plugin-oauth2.spec
MULTILIB=false
DO_NOT_INSTALL=('signon-plugin-oauth2-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
