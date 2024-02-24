
echo "#####################################################################"
echo ""
echo "Setting up the environment ..."

if [ ! -d lib  ] || [ ! -d bin ]; then
    echo "ERROR: Your installation  is not proper or you are you are sourcing itt from a wrong directory ..."
    echo "Contact  help@edautils.com for any help "
    echo "#####################################################################"
    exit 1
fi


#MAXMEM="2048"
#JAVA_FLAGS=" -ms5m -Xmx${MAXMEM}m "
#export JAVA_FLAGS
EDAUTILS_ROOT=$PWD
export EDAUTILS_ROOT
EDAUTILS_LICENSE_FILE=$EDAUTILS_ROOT/edautils.lic
export EDAUTILS_LICENSE_FILE
PATH="${EDAUTILS_ROOT}/bin:$PATH"
export PATH
unameOut="$(uname -s)"
case "${unameOut}" in
    CYGWIN*)    EDAUTILS_ROOT=`cygpath  -m "$EDAUTILS_ROOT"`;export EDAUTILS_ROOT;;
esac
CLASSPATH=${EDAUTILS_ROOT}/lib/testbenchgenerators.jar 
export CLASSPATH

echo ""
echo "Completed  the environment  setup, you're all set to run the tool(s) ..."
echo ""
echo "#####################################################################"
echo ""

