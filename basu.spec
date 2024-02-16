#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	sd-bus library extracted from systemd
Summary(pl.UTF-8):	Biblioteka sd-bus wydobyta z systemd
Name:		basu
Version:	0.2.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://git.sr.ht/~emersion/basu/refs/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	aafd850a07c0e8d2531bc54637a1ead6
URL:		https://sr.ht/~emersion/basu/
BuildRequires:	audit-libs-devel
BuildRequires:	gperf
BuildRequires:	libcap-devel
BuildRequires:	meson >= 0.54
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Some projects rely on the sd-bus library for DBus support. However not
all systems have systemd or elogind installed. This library provides
just sd-bus (and the busctl utility).

%description -l pl.UTF-8
Niektóre projekty polegają na bibliotece sd-bus do obsługi DBus;
jednak nie wszystkie systemy mają zainstalowane systemd lub elogind.
Ta biblioteka udostępnia samo sd-bus (oraz narzędzie busctl).

%package devel
Summary:	Header files for basu library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki basu
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libcap-devel

%description devel
Header files for basu library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki basu.

%package static
Summary:	Static basu library
Summary(pl.UTF-8):	Statyczna biblioteka basu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static basu library.

%description static -l pl.UTF-8
Statyczna biblioteka basu.

%prep
%setup -q

%build
%meson build

%ninja_build -C build \
	%{!?with_static_libs:--default-library=shared}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/basuctl
%attr(755,root,root) %{_libdir}/libbasu.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbasu.so
%{_includedir}/basu
%{_pkgconfigdir}/basu.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbasu.a
%endif
