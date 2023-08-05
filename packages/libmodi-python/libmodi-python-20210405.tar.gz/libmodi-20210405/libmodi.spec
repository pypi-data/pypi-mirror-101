Name: libmodi
Version: 20210405
Release: 1
Summary: Library to access Mac OS disk image formats
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libmodi
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: bzip2          openssl          xz-libs zlib
BuildRequires: gcc bzip2-devel          openssl-devel          xz-devel zlib-devel

%description -n libmodi
Library to access Mac OS disk image formats

%package -n libmodi-static
Summary: Library to access Mac OS disk image formats
Group: Development/Libraries
Requires: libmodi = %{version}-%{release}

%description -n libmodi-static
Static library version of libmodi.

%package -n libmodi-devel
Summary: Header files and libraries for developing applications for libmodi
Group: Development/Libraries
Requires: libmodi = %{version}-%{release}

%description -n libmodi-devel
Header files and libraries for developing applications for libmodi.

%package -n libmodi-python2
Obsoletes: libmodi-python < %{version}
Provides: libmodi-python = %{version}
Summary: Python 2 bindings for libmodi
Group: System Environment/Libraries
Requires: libmodi = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libmodi-python2
Python 2 bindings for libmodi

%package -n libmodi-python3
Summary: Python 3 bindings for libmodi
Group: System Environment/Libraries
Requires: libmodi = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libmodi-python3
Python 3 bindings for libmodi

%package -n libmodi-tools
Summary: Several tools for reading Mac OS disk images
Group: Applications/System
Requires: libmodi = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libmodi-tools
Several tools for reading Mac OS disk images

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libmodi
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libmodi-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libmodi-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmodi.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libmodi-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libmodi-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libmodi-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Apr  5 2021 Joachim Metz <joachim.metz@gmail.com> 20210405-1
- Auto-generated

