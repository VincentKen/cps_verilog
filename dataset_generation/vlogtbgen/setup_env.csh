echo "#####################################################################"
echo ""
echo "Setting up the environment ..."

if ( ! ( -d bin ) || ! ( -d lib ) ) then
    echo "ERROR: Your installation  is not proper or you are you are sourcing itt from a wrong directory ..."
    echo "Contact  help@edautils.com for any help "
    echo "#####################################################################"
    exit 1
endif

#setenv MAXMEM 2048
#setenv JAVA_FLAGS " -ms5m -Xmx${MAXMEM}m "

setenv EDAUTILS_ROOT $PWD
setenv EDAUTILS_LICENSE_FILE $EDAUTILS_ROOT/edautils.lic

setenv CLASSPATH ${EDAUTILS_ROOT}/lib/testbenchgenerators.jar 
setenv PATH "${EDAUTILS_ROOT}/bin:$PATH"

echo ""
echo "Completed  the environment  setup, you're all set to run the tool(s) ..."
echo ""
echo "#####################################################################"
echo ""
exit 0
