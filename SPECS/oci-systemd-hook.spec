%global provider        github
%global provider_tld    com
%global project         projectatomic
%global repo            oci-systemd-hook
# https://github.com/projectatomic/oci-systemd-hook
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          2d0b8a328d2e0b22d00a47911a0e6ee16e0ea072
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           %{repo}
Epoch:          1
Version:        0.1.15
Release:        2.git%{shortcommit}%{?dist}
# golang / go-md2man not available on ppc64
ExcludeArch:    ppc64 i686
Summary:        OCI systemd hook for docker
Group:          Applications/Text
License:        GPLv3+
URL:            https://%{import_path}
Source0:        https://%{import_path}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(yajl)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pcre-devel
BuildRequires:  go-md2man
Obsoletes:      %{name} <= 1.10.3-46

%description
OCI systemd hooks enable running systemd in a OCI runc/docker container.

%prep
%setup -q -n %{name}-%{commit}

%build
aclocal
autoreconf -i
%configure --libexecdir=%{_libexecdir}/oci/hooks.d/
make %{?_smp_mflags}

%install
%make_install

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%doc README.md
%license LICENSE
%{_mandir}/man1/%{name}.1*
%dir %{_libexecdir}/oci
%dir %{_libexecdir}/oci/hooks.d
%{_libexecdir}/oci/hooks.d/%{name}
%dir %{_usr}/share/containers/oci/hooks.d
%{_usr}/share/containers/oci/hooks.d/oci-systemd-hook.json

%changelog
* Wed Aug 08 2018 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.15-2.git2d0b8a3
- Resolves: #1614020 - disable i686 temporarily cause no go-md2man

* Thu Dec 21 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.15-1.git
- Fix issue with oci-systemd-hook running in user namespaces
- fix json file to run container with proper stage field.

* Thu Sep 14 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.14-1.git1ba44c6
- Add CRI-O configuration file support

* Tue Aug 15 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.13-1.gitafe4b4a
- Allow volume mounting of files under /run directory
- Specifically docker.sock to fix a bug.

* Fri Aug 11 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.1.12-1.git1e84754
- bump to v0.1.12
- add BR: pcre-devel
- ExcludeArch: ppc64 because no golang or go-md2man

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.1.11-3.git1ac958a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.1.11-2.git1ac958a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.11-1.gitfbf3b42
- Allow container definitions where rootfs is not an absolute path

* Thu Jul 13 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.10-1.gitfbf3b42
- Use env variable to disable oci-systemd-hook

* Thu Jun 29 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.9-1.gitaa42622
- Cleaned up to work with newer versions of runc and as a cri-o hook

* Tue Jun 6 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.8-1.gitd899a8e
- Fixes for running with user namespace

* Wed Mar 29 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.7-1.gitfe22236
- rh-ulrich-o - Patch to allocate configData dynamically

* Mon Mar 6 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.6-1.git16f7c8a
- Reimplement systemd handling.
- Remove docker path from systemdhook

* Wed Feb 8 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.5-1.git16f7c8a
- Fix mounting of /var/log/journal inside of the container

* Thu Feb 2 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.4-10.git5db667f
- oci-systemd-hook: do not fail if /run/secrets does not exist
- Fix compiler -Wall -Wextra issues

* Thu Jan 12 2017 Dan Walsh <dwalsh@redhat.com> - 1:0.1.4-9.git671c428
- Resolves: #1412728
- built commit 671c428

* Tue Dec 20 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.4-8.git45455fe
- Resolves: #1364237
- built commit 45455fe

* Tue Oct 25 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:0.1.4-7.gita9c551a
- rebase

* Tue Jul 05 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.4-6.git337078c
- Resolves: #1355905
- built commit 337078c

* Tue Jul 05 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.4-5.git41491a3
- Obsoletes the subpackage earlier provided by docker

* Thu Jun 30 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1:0.1.4-4.git41491a3
- Bump Epoch to 1 so that it can obsolete subpackage from docker

* Tue Jun 28 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.4-3.git41491a3
- re-add provider_prefix since gofed needs it

* Thu Jun 23 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.4-2.git41491a3
- built commit 41491a3
- spec file cleanup
- remove provider_prefix and only use import_path

* Thu Feb 18 2016 Dan Walsh <dwalsh@redhat.com> - 0.1.4-1.gitde345df
- Fix up to prepare for review

* Mon Nov 23 2015 Mrunal Patel <mrunalp@gmail.com> - 0.1.3
- Fix bug in man page installation

* Mon Nov 23 2015 Mrunal Patel <mrunalp@gmail.com> - 0.1.2
- Add man pages

* Mon Nov 23 2015 Mrunal Patel <mrunalp@gmail.com> - 0.1.1
- Initial RPM release
