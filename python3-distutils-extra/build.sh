#!/usr/bin/env bash

SPECFILE=python3-distutils-extra.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
