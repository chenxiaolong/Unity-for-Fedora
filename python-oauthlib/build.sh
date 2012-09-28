#!/usr/bin/env bash

SPECFILE=python-oauthlib.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
