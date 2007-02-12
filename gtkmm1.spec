%include	/usr/lib/rpm/macros.perl
%define		src_name	gtkmm
Summary:	A C++ interface for the GTK+ (a GUI library for X)
Summary(pl.UTF-8):   Interfejs C++ dla GTK+ (biblioteki interfejsu graficznego dla X)
Name:		gtkmm1
Version:	1.2.10
Release:	4
License:	LGPL
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/gtkmm/%{src_name}-%{version}.tar.gz
# Source0-md5:	a3816bef91a2796c3984b12954cc7fc9
Patch0:		%{name}-link.patch
Patch1:		%{name}-am18.patch
Patch2:		%{name}-gcc34.patch
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+-devel >= 1.2.7
BuildRequires:	libsigc++1-devel >= 1.0.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	rpm-perlprov
BuildRequires:	zlib-devel
Requires:	cpp
Obsoletes:	Gtk--
Obsoletes:	gtkmm < 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(a)'
%define		_ulibdir	%{_prefix}/lib

%description
This package provides a C++ interface for GTK+ (the Gimp ToolKit) GUI
library. The interface provides a convenient interface for C++
programmers to create GUIs with GTK+'s flexible object-oriented
framework. Features include type safe callbacks, widgets that are
extensible using inheritance and over 110 classes that can be freely
combined to quickly create complex user interfaces. This package
contains also GDK-- library, a C++ interface for GDK (General Drawing
Kit) library.

%description -l pl.UTF-8
Pakiet GTK-- udostępnia interfejs C++ dla GTK+. GTK+ (Gimp ToolKit)
jest biblioteką służącą do tworzenia graficznych interfejsów
użytkownika. Interfejs zawiera wygodny interfejs dla programistów C++
do tworzenia graficznych interfejsów użytkownika przy użyciu
elastycznego, zorientowanego obiektowo szkieletu GTK+. Biblioteka
zawiera callbacki z bezpiecznymi typami, widgety rozszerzalne poprzez
dziedziczenie i ponad 110 klas, które można dowolnie łączyć, aby
szybko stworzyć skomplikowane interfejsy użytkownika. W pakiecie
znajduje się także biblioteka GDK--, będąca interfejsem C++ dla GDK
(General Drawing Kit).

%package devel
Summary:	GTK-- and GDK-- header files, development documentation
Summary(pl.UTF-8):   Pliki nagłówkowe GTK-- i GDK--, dokumentacja dla programistów
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+-devel >= 1.2.7
Requires:	libsigc++1-devel >= 1.0.4
Obsoletes:	Gtk---devel
Obsoletes:	gtkmm-devel < 1.3

%description devel
Header files and development documentation for GTK-- library.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja dla programistów do biblioteki GTK--.

%package static
Summary:	GTK-- and GDK-- static libraries
Summary(pl.UTF-8):   Biblioteki statyczne GTK-- i GDK--
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	Gtk---static
Obsoletes:	gtkmm-static < 1.3

%description static
GTK-- and GDK-- static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne GTK-- i GDK--.

%prep
%setup -q -n %{src_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# AM_ACLOCAL_INCLUDE
tail -n +161 aclocal.m4 | head -n 16 > acinclude.m4
# GNOME_CXX_WARNINGS
tail -n +3762 aclocal.m4 | head -n 53 >> acinclude.m4

%build
CXXFLAGS="%{rpmcflags} -fno-exceptions"
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-static=yes

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir}

cp -dpr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%{__perl} -pi -e 's@#!/usr/bin/env perl@#!/usr/bin/perl@' \
	$RPM_BUILD_ROOT%{_bindir}/gtkmmconvert

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS NEWS
%attr(755,root,root) %{_libdir}/libgdkmm*.so.*.*
%attr(755,root,root) %{_libdir}/libgtkmm*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%dir %{_ulibdir}/gtkmm
%if "%{_ulibdir}" != "%{_libdir}"
%dir %{_libdir}/gtkmm
%endif
%{_libdir}/gtkmm/include
%dir %{_ulibdir}/gtkmm/proc
%{_ulibdir}/gtkmm/proc/*.m4
%attr(755,root,root) %{_ulibdir}/gtkmm/proc/gtkmmproc
%{_includedir}/*
%{_aclocaldir}/*
%{_examplesdir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
