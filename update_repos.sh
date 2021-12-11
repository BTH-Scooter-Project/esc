#!/usr/bin/env bash

# Current version
VERSION="1.0.0"
E_NO_ARGS=65

declare -a repos

#
# Message to display for usage and help.
#
function usage
{
    local txt=(
		"Utility $SCRIPT for doing stuff."
		"Usage: $SCRIPT [options] <command> [arguments]"
		""
		"Command:"
		"  push     Push all repository changes to github"
		"  pull     Pull all repository changes from github"
		"  <empty>  Run pull and then push."
		""
		"Options:"
		"  -h, --help,     Print help."
		"  -v, --version,  Print version."
    )

    printf "%s\\n" "${txt[@]}"
}


#
# Message to display when bad usage.
#
function badUsage
{
    local message="$1"
    local txt=("For an overview of the command, execute:" "$SCRIPT --help")

    [[ -n $message ]] && printf "%s\\n" "$message"

    printf "%s\\n" "${txt[@]}"
}




#
# Message to display for version.
#
function version
{
    local txt=("$SCRIPT version $VERSION")

    printf "%s\\n" "${txt[@]}"
}

function git-push
{
	cd "$1"
	git push
	cd ..
}

function git-pull
{
	cd "$1"
	git pull
	cd ..
}

function main
{
	repos=("esc" "api" "databas" "test")

	cd ..
	printf "** Updating repos **\\n\\n"
	echo "Command: $1"
	while (( $# ))
	do
		case "$1" in
			--help | -h)
				usage
				exit 0
			;;

			--version | -v)
				version
				exit 0
			;;

			"pull" \
			| "push")
				command=$1
				shift
				for repo in ${repos[@]}
				do
					git-"$command" "$repo"
				done
			;;

			*)
				badUsage "Option/command not recognized."
				exit 1
			;;
		esac
	done
	exit 0
}

printf "$@\\n"
if [[ $# -eq 0 ]]
then
	main "push" "pull"
	exit 0
fi
main "$@"