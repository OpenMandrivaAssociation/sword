%define lib_name_orig libsword
%define lib_major     4
%define lib_name      %mklibname %name %version
%define develname %mklibname -d %name
%define staticname %mklibname -d -s %name

Summary:        The SWORD Project framework for manipulating Bible texts
Summary(cs):    Programy pro studium Bible a vývojové nástroje
Summary(sk):    Programy pre ¹túdium Biblie a vývojové nástroje
Name:           sword
Version:        1.5.11
Release:        %mkrel 1
License:        GPLv2+
URL:            http://www.crosswire.org/sword/software/
Source:         http://www.crosswire.org/ftpmirror/pub/sword/source/v1.5/%{name}-%{version}.tar.gz
Source1:        ftp://ftp.zedz.net/pub/crypto/crypto/LIBS/sapphire/sapphire.zip 
Source2:        sword_icons.tar.bz2
Group:          System/Libraries
BuildRequires:  zlib-devel
BuildRequires:  curl-devel >= 7.10.5
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       %{lib_name} = %{version}
Requires:       curl >= 7.10.5


%description
The SWORD Project is an effort to create an ever expanding software package 
for research and study of God and His Word.  The SWORD Framework 
allows easy manipulation of Bible texts, commentaries, lexicons, dictionaries, 
etc.  Many frontends are build using this framework.  An installed module 
set may be shared between any frontend using the framework.

%description -l cs
Snahou projektu SWORD je vytvoøit volné (ve smyslu licence OpenSource)
programy, vývojové nástroje a pomùcky ke studiu Bible.
Mohou být instalovány dal¹í, volitelnì pøídavné moduly: rùzné pøeklady Bible,
komentáøe, výklady a slovníky.

%description -l sk
Cieµom projektu SWORD je vytvori» voµné (vo zmysle licencie OpenSource)
programy, vývojoví nástroje a pomôcky pre ¹túdium Biblie.. Mô¾u sa tie¾
nain¹talova» ïal¹ie voliteµné a prídavné moduly: rôzne preklady Biblie,
Biblické komentáre, lexikóny a slovníky.


#main package (contains *.so.[major].* only)
%package -n %{lib_name}
Summary:         Main library for sword #(!) summary for main lib RPM only
Group:           System/Libraries

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with sword.

%package -n %{develname}
Summary:         Include files for developing sword applications
Group:           System/Libraries
Requires:        %{lib_name} = %{version}
Provides:        %{name}-devel = %{version}-%{release} 
Obsoletes:       %mklibname -d %name 1.5.9

%description -n %{develname}
This package contains the headers that programmers 
will need to develop applications which will use the SWORD Bible Framework.

%package -n %{staticname}
Summary:         Static libs for developing sword applications
Group:           System/Libraries
Requires:        %{lib_name} = %{version}
Requires:	 %{develname} = %{version}
Provides:        %{name}-static-devel = %{version}-%{release} 
Obsoletes:       %mklibname -d -s %name 1.5.9

%description -n %{staticname}
This package contains the static libraries that programmers 
will need to develop applications which will use the SWORD Bible Framework.

%prep
%setup -q -a2

%{_bindir}/unzip -d sapphire %{SOURCE1}
%{__cp} -a sapphire/SAPPHIRE.H include/sapphire.h
%{__cp} -a sapphire/SAPPHIRE.CPP src/modules/common/sapphire.cpp

%build
%{configure2_5x} --disable-dependency-tracking --enable-utilities --with-curl --disable-debug --enable-shared --with-conf
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%{__install} -m 0755 utilities/{mkfastmod,mod2vpl,vpl2mod} %{buildroot}%{_bindir}

%clean
%{__rm} -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README AUTHORS NEWS INSTALL LICENSE ChangeLog 
%doc samples doc/*.*
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/sword.conf

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*%{name}-*.so

%files -n %{develname}
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_includedir}/sword
%{_includedir}/sword/*.*
%{_libdir}/*%{name}.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/*.a
