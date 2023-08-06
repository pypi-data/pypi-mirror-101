#!/bin/bash

profile_file=/etc/profile.d/o2.sh
ld_file=/etc/ld.so.conf.d/o2-x86_64.conf
package_root=/opt/o2

if [ ! -f $profile_file ]; then

  echo "export PYTHONPATH=${package_root}/lib:\$PYTHONPATH" >> $profile_file
  echo "export ROOT_DYN_PATH=${package_root}/lib:\$ROOT_DYN_PATH" >> $profile_file
  echo "export ROOT_INCLUDE_PATH=${package_root}/include:\$ROOT_INCLUDE_PATH" >> $profile_file
  echo "export PATH=${package_root}/bin:\$PATH" >> $profile_file

  chmod a+x $profile_file
fi;

if [ ! -f $ld_file ]; then
  echo "${package_root}/lib" >> $ld_file
  /usr/sbin/ldconfig
fi;

versions_installed=$1
if [ $versions_installed == 1 ]; then #TODO: This needs to be adjusted so updates can be applied
  package=<%= @name %>
  package=${package#"o2-"} #trim o2- prefix
  package_underscore=${package//-/_}

  echo "export ${package_underscore^^}_ROOT=${package_root}" >> $profile_file

fi
