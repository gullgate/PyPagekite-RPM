Name: pagekite
Version: 0.3.19
Release: 0%{?dist}
Summary: System for running publicly visible webs behind restrictive firewalls
Group: Applications/System
License: AGPLv3
Packager: Edvin Dunaway <edvin@eddinn.net>
URL: https://pagekite.net/
Source0: http://vampire.eddinn.net/pagekite/%{name}-%{version}.tar.gz
Source1: pagekite.init
Source2: pagekite.sysconfig
Source3: pagekite.logrotate
Source4: README.fedora
Source5: pagekite.rc.sample
Source6: local.rc.sample
Source7: frontend.rc.sample
Source8: pagekite.net.ca_cert
Source9: pagekite.1.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python python-devel
Requires: pyOpenSSL

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%description
PageKite is a system for running publicly visible servers
on machines without a direct connection to the Internet,
such as mobile devices or computers behind restrictive firewalls.

%prep
%setup -q -n pagekite-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_initrddir}
install -d %{buildroot}/%{_sysconfdir}/logrotate.d
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -d %{buildroot}/%{_sysconfdir}/pagekite
install -d %{buildroot}/%{_localstatedir}/log
install -d %{buildroot}/%{_localstatedir}/log/pagekite
install -d %{buildroot}/%{_mandir}/man1
install -p -m 644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/pagekite/pagekite.rc
install -p -m 644 %{SOURCE7} %{buildroot}/%{_sysconfdir}/pagekite/frontend.rc
install -p -m 644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/pagekite/local.rc
install -p -m 644 %{SOURCE8} %{buildroot}/%{_sysconfdir}/pagekite/pagekite.net.ca_cert
install -p -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/pagekite
install -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/pagekite
install -p -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/pagekite
#touch %{buildroot}/%{_localstatedir}/log/pagekite/pagekite.log
cp %{SOURCE9} %{buildroot}/%{_mandir}/man1/pagekite.1.gz

# FC-4 and earlier won't create these automatically; create them here
# so that the %exclude below doesn't fail
touch %{buildroot}/%{_bindir}/pagekite.pyc
touch %{buildroot}/%{_bindir}/pagekite.pyo

%clean
rm -rf %{buildroot}

%pre
if ! /usr/bin/id pagekite &>/dev/null; then
    /usr/sbin/useradd -r -d %{logdir} -s /bin/sh -c "pagekite" pagekite || \
        echo "Unexpected error adding user \"pagekite\". Aborting installation."
fi

%post
/sbin/chkconfig --add pagekite
/sbin/service pagekite stop > /dev/null 2>&1
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service pagekite stop > /dev/null 2>&1
  /sbin/chkconfig --del pagekite
fi
exit 0

%postun
if [ $1 -eq 0 ]; then
    /usr/sbin/userdel pagekite || echo "User \"pagekite\" could not be deleted."
    /usr/sbin/groupdel pagekite || echo "Group \"pagekite\" could not be deleted."
fi
/sbin/service pagekite condrestart &>/dev/null || :

%files
%defattr(-,root,root)
%doc README.fedora README.md pagekite.1.gz
%doc HISTORY.txt agpl-3.0.txt
%doc pagekite.rc.sample local.rc.sample frontend.rc.sample
%{_mandir}/man1/*
%{_sysconfdir}/logrotate.d/pagekite
%exclude %{_bindir}/*.py[co]
%{_initrddir}/pagekite
%defattr(755,pagekite,pagekite)
%{_localstatedir}/log/pagekite
%{_bindir}/*.py
%{_sysconfdir}/sysconfig/pagekite
%config(noreplace) %{_sysconfdir}/pagekite/*.rc
%{_sysconfdir}/pagekite/pagekite.net.ca_cert

%changelog
* Fri May 6 2011 Edvin Dunaway <edvin@eddinn.net> 0.3.19-0
- added user/group pagekite install/uninstall and code fixup
* Thu May 5 2011 Edvin Dunaway <edvin@eddinn.net> 0.3.19-0
- adapting init script and message handling
* Wed May 4 2011 Edvin Dunaway <edvin@eddinn.net> 0.3.19-0
- script fixup and adding manpage
* Tue May 3 2011 Edvin Dunaway <edvin@eddinn.net> 0.3.19-0
- updated pagekite binary to stable
* Mon May 2 2011 Edvin Dunaway <edvin@eddinn.net> 0.3.18-0
- Initial build
