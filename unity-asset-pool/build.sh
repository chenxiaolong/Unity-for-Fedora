#!/usr/bin/env bash

SPECFILE=unity-asset-pool.spec
MULTILIB=false

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
