%include	/usr/lib/rpm/macros.perl
Summary:	A C++ interface for the GTK+ (a GUI library for X)
Summary(pl):	Interfejs C++ dla GTK+ (biblioteki interfejsu graficznego dla X)
Name:		gtkmm1
%define		src_name	gtkmm
Version:	1.2.10
Release:	2
License:	LGPL
Group:		X11/Libraries
Source0:	http://dl.sourceforge.net/gtkmm/%{src_name}-%{version}.tar.gz
# Source0-md5:	a3816bef91a2796c3984b12954cc7fc9
Patch0:		%{name}-link.patch
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+-devel
BuildRequires:	imlib-devel
BuildRequires:	libsigc++1-devel >= 1.0.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	rpm-perlprov
BuildRequires:	zlib-devel
Requires:	cpp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	Gtk--
Obsoletes:	gtkmm < 1.3

%define		_noautoreq	'perl(a)'

%description
This package provides a C++ interface for GTK+ (the Gimp ToolKit) GUI
library. The interface provides a convenient interface for C++
programmers to create GUIs with GTK+'s flexible object-oriented
framework. Features include type safe callbacks, widgets that are
extensible using inheritance and over 110 classes that can be freely
combined to quickly create complex user interfaces. This package
contains also GDK-- library, a C++ interface for GDK (General Drawing
Kit) library.

%description -l pl
Pakiet GTK-- udostêpnia interfejs C++ dla GTK+. GTK (Gimp ToolKit)
jest bibliotek± s³u¿±c± do tworzenia graficznych interfejsów
u¿ytkownika. Interfejs zawiera wygodny interfejs dla programistów C++
do tworzenia graficznych interfejsów u¿ytkownika przy u¿yciu
elastycznego, zorientowanego obiektowo szkieletu GTK+. Biblioteka
zawiera callbacki z bezpiecznymi typami, widgety rozszerzalne poprzez
dziedziczenie i ponad 110 klas, które mo¿na dowolnie ³±czyæ, aby
szybko stworzyæ skomplikowane interfejsy u¿ytkownika. W pakiecie
znajduje siê tak¿e biblioteka GDK--, bêd±ca interfejsem C++ dla GDK
(General Drawing Kit).

%package devel
Summary:	GTK-- and GDK-- header files, development documentation
Summary(pl):	Pliki nag³ówkowe GTK-- i GDK--, dokumentacja dla programistów
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	gtk+-devel
Requires:	libsigc++1-devel
Obsoletes:	Gtk---devel
Obsoletes:	gtkmm-devel < 1.3

%description devel
Header files and development documentation for GTK-- library.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja dla programistów do biblioteki GTK--.

%package static
Summary:	GTK-- and GDK-- static libraries
Summary(pl):	Biblioteki statyczne GTK-- i GDK--
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	Gtk---static
Obsoletes:	gtkmm-static < 1.3

%description static
GTK-- and GDK-- static libraries.

%description static -l pl
Biblioteki statyczne GTK-- i GDK--.

%prep
%setup -q -n %{src_name}-%{version}
%patch -p1

# AM_ACLOCAL_INCLUDE
tail +161 aclocal.m4 | head -n 16 > acinclude.m4
# GNOME_CXX_WARNINGS
tail +3762 aclocal.m4 | head -n 53 >> acinclude.m4

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
%dir %{_libdir}/gtkmm
%{_libdir}/gtkmm/include
%dir %{_libdir}/gtkmm/proc
%{_libdir}/gtkmm/proc/*.m4
%attr(755,root,root) %{_libdir}/gtkmm/proc/gtkmmproc
%{_includedir}/*
%{_aclocaldir}/*
%{_examplesdir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
