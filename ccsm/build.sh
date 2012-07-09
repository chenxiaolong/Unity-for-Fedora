#!/usr/bin/env bash

SPECFILE=ccsm.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
