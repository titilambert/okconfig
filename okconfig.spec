%{!?python_version: %define python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print get_python_version()")}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define is_suse %(test -e /etc/SuSE-release && echo 1 || echo 0)

Summary: Python Nagios Template management and configuration power tools
Name: okconfig
Version: 1.0.5
Release: 7%{?dist}
Source0: http://opensource.is/files/%{name}-%{version}.tar.gz
License: GPLv2
Group: System Environment/Libraries
Requires: python >= 2.3
BuildRequires: python-devel
%if %is_suse
BuildRequires: gettext-devel
%else
%if 0%{?fedora} >= 16
BuildRequires: python-setuptools
%else
%if 0%{?fedora} >= 8
BuildRequires: python-setuptools-devel
%else
%if 0%{?rhel} >= 5
BuildRequires: python-setuptools
%endif
%endif
%endif
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: http://opensource.is/trac
BuildArch: noarch 
Requires: pynag
Requires: nagios nagios-plugins-nrpe  nagios-plugins-ping nagios-plugins-ssh
Requires: nagios-okplugin-apc nagios-okplugin-brocade nagios-okplugin-mailblacklist 
Requires: nagios-okplugin-check_disks nagios-okplugin-check_time nagios-plugins-fping

%description
A robust template mechanism for Nagios configuration files. Providing
standardized set of configuration templates and select quality plugins 
to enterprise quality monitoring.



%prep
%setup -q

%build
%{__python} setup.py build

%install
test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --prefix=/usr --root=$RPM_BUILD_ROOT
install -m 755 -d usr/share/okconfig $RPM_BUILD_ROOT/%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT/etc/bash_completion.d/
mkdir -p $RPM_BUILD_ROOT/etc/profile.d/
mkdir -m 775 -p $RPM_BUILD_ROOT/etc/nagios/okconfig
mkdir -m 775 -p $RPM_BUILD_ROOT/etc/nagios/okconfig/groups
mkdir -m 775 -p $RPM_BUILD_ROOT/etc/nagios/okconfig/hosts
install -m 644 etc/okconfig.conf $RPM_BUILD_ROOT/%{_sysconfdir}/
install -m 644 etc/bash_completion.d/* $RPM_BUILD_ROOT/%{_sysconfdir}/bash_completion.d/
install -m 644 etc/profile.d/* $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%if "%{python_version}" >= "2.5"
%{python_sitelib}/okconfig*.egg-info
%endif
%dir %{python_sitelib}/okconfig
%{python_sitelib}/okconfig/*.py*
%{_bindir}/okconfig
%doc AUTHORS README LICENSE CHANGES
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/profile.d/nagios.csh
%config(noreplace) %{_sysconfdir}/profile.d/nagios.sh
%config(noreplace) %{_sysconfdir}/okconfig.conf
%config(noreplace) %{_sysconfdir}/bash_completion.d/okconfig
#%{_mandir}/man1/okconfig.1.gz
%defattr(0775, nagios, nagios)
%dir %{_sysconfdir}/nagios/okconfig
%dir %{_sysconfdir}/nagios/okconfig/groups
%dir %{_sysconfdir}/nagios/okconfig/hosts


%changelog
* Wed May 30 2012 Tomas Edwardsson <tommi@tommi.org> 1.0.5-1
- Fixed rsync path for tito, was missing root user (tommi@tommi.org)
- Added F17 to tito build (tommi@tommi.org)
- new okconfig binary with new syntax (palli@opensource.is)
- Merge branch 'master' of https://opensource.ok.is/git/okconfig
  (palli@opensource.is)
- addservice function added (palli@opensource.is)
- host_template now configurable when adding new hosts (palli@opensource.is)
- Issue #55, removed mssql till requirements are satisfied (tommi@tommi.org)
- rhcs6 examples added (palli@opensource.is)

* Mon Mar 12 2012 Pall Sigurdsson <palli@opensource.is> 1.0.4-1
- / added to end of every reponame. okconfig.spec now support fedora 16
  (palli@opensource.is)
- added more repos to releasers.conf (palli@opensource.is)

* Mon Mar 12 2012 Pall Sigurdsson <palli@opensource.is> 1.0.3-1
- tito releasers.conf added (palli@opensource.is)
- manpages commented out (palli@opensource.is)

* Mon Mar 12 2012 Pall Sigurdsson <palli@opensource.is> 1.0.2-1
- 

* Mon Mar 12 2012 Pall Sigurdsson <palli@opensource.is> 1.0.1-1
- new package built with tito

* Sun Oct  1 2011 Tomas Edwardsson <tommi@opensource.is> - 1.0-9
- Fixes to packaging and missing specifications

* Fri Jul 22 2011 Pall Sigurdsson <palli@opensource.is> - 1.0-1
- Initial RPM Creation, based heavily on the func spec file
