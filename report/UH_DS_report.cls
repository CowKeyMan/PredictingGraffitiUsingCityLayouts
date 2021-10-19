%%
%% This is file `UH_DS_report.cls'
%%
%% Based heavily on HYgradu.cls of Uni Helsinki Dept. of Physics, which us based on
%% tktltiki v1.1, and the thesis LaTeX files of
%% the Dept. of Physics and former Dept. of Astronomy.
%%
%%% This work may be distributed and/or modified under the
  % conditions of the LaTeX Project Public License, either version 1.3
  % of this license or (at your option) any later version.
  % The latest version of this license is in
  %   http://www.latex-project.org/lppl.txt
  % and version 1.3 or later is part of all distributions of LaTeX
  % version 2005/12/01 or later.
%%
\NeedsTeXFormat{LaTeX2e}[2000/06/01]
\ProvidesClass{UH_DS_report}
  [2021/09/14 v1.2 UH Data Science Study Skills Template]
\newif\if@finnish
\newif\if@swedish
\newif\if@english
\newif\if@emptyfirstpagenumber
% programme specific content starts
%\newif\if@cs
%\newif\if@csm
% programme specific content ends

\RequirePackage{lastpage}
\RequirePackage{nomencl}
\RequirePackage{emptypage}
\RequirePackage{perpage}

\DeclareOption{finnish}{\@finnishtrue}
\DeclareOption{swedish}{\@swedishtrue}
\DeclareOption{english}{\@englishtrue}
% programme specific content starts
%\DeclareOption{cs}{\@cstrue}
%\DeclareOption{csm}{\@csmtrue}
% programme specific content ends
\DeclareOption{emptyfirstpagenumber}{\@emptyfirstpagenumbertrue}
\newif\if@defaulttypesize
\@defaulttypesizetrue
\newif\if@defaultpaper
\@defaultpapertrue
\newif\if@defaulttitlepage
\@defaulttitlepagetrue

\DeclareOption{10pt}{
  \@defaulttypesizefalse
  \PassOptionsToClass{10pt}{report}}
\DeclareOption{11pt}{
  \@defaulttypesizefalse
  \PassOptionsToClass{11pt}{report}}

\DeclareOption{a5paper}{
  \@defaultpaperfalse
  \PassOptionsToClass{a5paper}{report}}
\DeclareOption{b5paper}{
  \@defaultpaperfalse
  \PassOptionsToClass{b5paper}{report}}
\DeclareOption{letterpaper}{
  \@defaultpaperfalse
  \PassOptionsToClass{letterpaper}{report}}
\DeclareOption{legalpaper}{
  \@defaultpaperfalse
  \PassOptionsToClass{legalpaper}{report}}
\DeclareOption{executivepaper}{
  \@defaultpaperfalse
  \PassOptionsToClass{executivepaper}{report}}

\DeclareOption{notitlepage}{
  \@defaulttitlepagefalse
  \PassOptionsToClass{notitlepage}{report}}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\if@defaulttypesize
  \PassOptionsToClass{12pt}{report}
\fi
\if@defaultpaper
  \PassOptionsToClass{a4paper}{report}
\fi
\if@defaulttitlepage
  \PassOptionsToClass{titlepage}{report}
\fi
\ProcessOptions\relax
\LoadClass{report}[2000/05/19]
\RequirePackage{latexsym}[1998/08/17 v2.2e Standard LaTeX package (lasy symbols)]
\RequirePackage[latin9]{inputenc}[2000/07/01 v0.996 Input encoding file ]
\RequirePackage[T1]{fontenc}[2000/08/30 v1.91 Standard LaTeX package]
\if@finnish
  \RequirePackage[finnish]{babel}[2001/03/01 v3.7h The Babel package]
\else
  \if@english
    \RequirePackage[english]{babel}[2001/03/01 v3.7h The Babel package]
  \else
    \if@swedish
      \RequirePackage[swedish]{babel}[2001/03/01 v3.7h The Babel package]
    \else
      \RequirePackage[finnish]{babel}[2001/03/01 v3.7h The Babel package]
    \fi
  \fi
\fi
\RequirePackage{geometry}[1999/10/07 v2.2 Page Geometry]

\newcommand{\defaultsettings}{%
  \if@twoside
    \geometry{bindingoffset=0.5cm,top=2.5cm, left=2.5cm, right=2.5cm,
              textheight=24cm,
              headheight=0.52cm, headsep=0.5cm}%
  \else
    \geometry{top=2.5cm, left=2.5cm, right=2.5cm,
              textheight=24cm,
              headheight=0.52cm, headsep=0.5cm}%
  \fi
} %left 3.5, left 4.3
\defaultsettings
\setlength{\parindent}{1cm}
\setlength{\parskip}{0pt}
\pagestyle{myheadings}
\markright{}
\pagenumbering{roman}
\newcommand{\onehalfspacing}{%
  \ifcase\@ptsize\relax % 10pt
    \renewcommand{\baselinestretch}{1.25}%
  \or % 11pt
    \renewcommand{\baselinestretch}{1.213}%
  \or % 12pt
    \renewcommand{\baselinestretch}{1.241}%
  \fi
  \normalsize
}
\newcommand{\doublespacing}{
  \ifcase\@ptsize\relax % 10pt
    \renewcommand{\baselinestretch}{1.667}
  \or % 11pt
    \renewcommand{\baselinestretch}{1.618}
  \or % 12pt
    \renewcommand{\baselinestretch}{1.655}
  \fi
  \normalsize
}
\newcommand{\singlespacing}{%
  \renewcommand{\baselinestretch}{1.0}%
  \normalsize
}
\newcommand{\mytableofcontents}{%

\tableofcontents

\pagestyle{fancy}
\fancyhf{} % delete current header and footer
\fancyhead[LE,LO]{\itshape\nouppercase{\textsc\thepage}}
\fancyhead[RO]{\itshape\nouppercase{\textsc\leftmark}}
\fancyhead[RE]{\itshape\nouppercase{\textsc\rightmark}}

\if@twoside
	\pagestyle{fancy}
	\fancyhf{} % delete current header and footer
	\fancyhead[LE,RO]{\itshape\nouppercase{\textsc\thepage}}
	\fancyhead[LO]{\itshape\nouppercase{\textsc\rightmark}}
	\fancyhead[RE]{\itshape\nouppercase{\textsc\leftmark}}
	\newpage
	%\thispagestyle{empty}
	\cleardoublepage
\fi

%\pagenumbering{arabic}
}

\newcommand{\lastpage}{%
  \label{lastpage}%
}

\newcommand{\numberofpages}{%
  \@ifundefined{r@lastpage}{0}{\pageref{lastpage}}%
}
\renewcommand{\and}{%
  \\ % Rivinvaihto.
  \hspace{1em}%
}

\def\datefinnish{%
  \def\today{\number\day.\number\month.\number\year}}
\newcommand{\level}[1]{\gdef\@level{#1}}
\level{}
\newcommand{\prof}[1]{\gdef\@prof{#1}}
\newcommand{\address}[1]{\gdef\@address{#1}}
\newcommand{\censors}[3]{\gdef\@censor{#1\\&#2\\&#3}}
\newcommand{\quoting}[2]{\gdef\@quoting{\begin{center}\emph{#1}\\ --- #2\end{center}}}


% content specific to CS programme
\addto\captionsfinnish{%
  \def\dateofacceptance{hyv\"aksymisp\"aiv\"a}%
  \def\grade{arvosana}%
  \def\instructor{arvostelija}%
  \def\uh{\sc{Helsingin Yliopisto}}%
  \def\helsinki{Helsinki}%
  \def\ccs{ACM Computing Classification System (CCS):}%
}
\addto\captionsenglish{%
  \def\dateofacceptance{Date of acceptance}%
  \def\grade{Grade}%
  \def\instructor{Instructor}%
  \def\uh{\sc{University of Helsinki}}%
  \def\helsinki{Helsinki}%
  \def\ccs{ACM Computing Classification System (CCS):}%
}
\addto\captionsswedish{%
  \def\dateofacceptance{godk.datum}%
  \def\grade{vitsord}%
  \def\instructor{bed\"omare}%
  \def\uh{\sc{Helsingfors Universitet}}%
  \def\helsinki{Helsingfors}%
  \def\ccs{ACM Computing Classification System (CCS):}%
}
% content specific to CS programme

%--------------------------------------------------------------------------
% Set chapter titles
\renewcommand{\@makechapterhead}[1]{%
\vspace*{50 pt}%
{\setlength{\parindent}{0pt} \raggedright \normalfont
\bfseries\Huge
\thechapter. #1\par\nobreak\vspace{40 pt}}}

%--------------------------------------------------------------------------
% Nomenclature: titles and unit space
\makenomenclature
\if@finnish
	\renewcommand{\nomname}{Symboliluettelo}
\else
	\if@english
		\renewcommand{\nomname}{List of Symbols}
	\fi
	\if@swedish
		\renewcommand{\nomname}{Nomenklatur}
	\fi
\fi
\newcommand{\nomunit}[1]{%
\renewcommand{\nomentryend}{\hspace*{\fill}#1}}

\newcommand{\mynomenclature}{%
\ifnum0\pdffilesize{\jobname.nls}>0
	\printnomenclature
	\addcontentsline{toc}{chapter}{\nomname}
	\markboth{\nomname}{}
	\cleardoublepage
\fi
\pagenumbering{arabic}
}

\newcommand{\myappendixtitle}{%
	\titleformat{\chapter}{\large\bfseries}{\appendixname~\thechapter .}{0.5em}{}
	\titlespacing*{\chapter}{0pt}{-20pt}{40pt}
}

\renewcommand*{\thefootnote}{\fnsymbol{footnote}} %footnote symbols for one page only
\MakePerPage{footnote}

%--------------------------------------------------------------------------
% GENERATE TITLE PAGE
\renewcommand{\maketitle}{
\pagenumbering{roman}
\begin{titlepage}
\onehalfspacing

\begin{center}

\includegraphics[width=5cm]{UH-logo-ml.png}

\begin{large}

\vspace{1cm}
%\@level

\@programme

\end{large}


\vspace{1.5cm}
\begin{LARGE}
{\bf \@title}

\end{LARGE}

\vspace{2cm}
\begin{large}
\@author
\end{large}

\vspace{5.0cm}

\vspace{14pt}
\begin{large}
\@date
\end{large}

\vspace{1.0cm}

%\begin{large}
%
%\def\reallyempty{}
%\if@english
%  \begin{tabular}{l l}
%  Supervisor(s): & \@prof\\
%  &\\
%  \ifx\@censor\reallyempty
%  &\\
%  \else
%  Examiner(s): & \@censor\\
%  \fi
%  &\\
%  \end{tabular}
%  \end{large}
%   \else
%    \if@finnish
%     \begin{tabular}{l l}
%     Ohjaaja(t): & \@prof\\
%     &\\
%     \ifx\@censor\reallyempty
%     &\\
%     \else
%     Tarkastaja(t): & \@censor\\
%     \fi
%     &\\
%     \end{tabular}
%     \end{large}
%	\else
%	 \if@swedish
%	  \begin{tabular}{l l}
%	  Handledare: & \@prof\\
%	  &\\
%  	  \ifx\@censor\reallyempty
%	  &\\
%	  \else
%	  Granskare: & \@censor\\
%	  \fi
%	  &\\
%	  \end{tabular}
%	  \end{large}
%	  \fi
%       \fi
%      \fi

\vspace{20pt}

{\rm\sc
\uh

\@faculty
}

\vspace{0.25cm}
\@address

\end{center}
\if@twoside
	\newpage
	\cleardoublepage
\fi
 \end{titlepage}
}

%--------------------------------------------------------------------------

\def\division{\char'057}

\newcommand{\faculty}[1]{\gdef\@faculty{#1}}
\newcommand{\programme}[1]{\gdef\@programme{#1}}
\newcommand{\department}[1]{\gdef\@department{#1}}
%\newcommand{\subject}[1]{\gdef\@subject{#1}}
\newcommand{\depositeplace}[1]{\gdef\@depositeplace{#1}}
\newcommand{\additionalinformation}[1]{\gdef\@additionalinformation{#1}}
\newcommand{\numberofpagesinformation}[1]{\gdef\@numberofpagesinformation{#1}}
\newcommand{\classification}[1]{\gdef\@classification{#1}}
\newcommand{\keywords}[1]{\gdef\@keywords{#1}}



%--------------------------------------------------------------------------

\newsavebox{\@abstract}
\newenvironment{@summary}{
  \begin{lrbox}{\@abstract}
    \begin{minipage}[t]{5.95in}
      \setlength{\parskip}{2ex}
}{

      \if \@classification
      \else
        %\ccs\ \@classification
      \fi
    \end{minipage}
  \end{lrbox}
  \put(58, 625){\mbox{\usebox{\@abstract}}}
}

\def\abst@small{\fontsize{10}{12}\selectfont}
\def\abst@tiny{\fontsize{6}{7}\selectfont}


%--------------------------------------------------------------------------
% GENERATE ABSTRACT
\renewenvironment{abstract}{
\pagestyle{empty}
\if@twoside
\begin{picture}(580,820)(90,-64)%
\else
\begin{picture}(580,820)(80,-64)%
\fi
\put(58,  744){\makebox(100, 8)[l]{\abst@small\@faculty}}
\put(289, 744){\makebox(100, 8)[l]{\abst@small\@programme}}
%\put(289, 744){\makebox(100, 8)[l]{\abst@small\@subject}}
\put(58,  714){\makebox(100, 8)[l]{\abst@small\@author}}
\put(58,  684){\parbox[l]{450pt}{\renewcommand{\baselinestretch}{.9}\abst@small\@title}}
\put(58,  654){\makebox(100, 8)[l]{\abst@small\@level}}
\put(212, 654){\makebox(100, 8)[l]{\abst@small\@date}}
\put(366, 654){\makebox(100, 8)[l]{\abst@small\pageref{LastPage}}}
\put(58,  115) {\makebox(100, 8)[l]{\abst@small\@keywords}}
\put(58,  85) {\makebox(100, 8)[l]{\abst@small\@depositeplace}}
\put(58,  59) {\makebox(100, 8)[l]{\abst@small\@additionalinformation}}

\begin{@summary}\abst@small}
{\end{@summary}

\put(53,30){\framebox(462,746){}} % laatikko
\put(284,739){\line(0,1){37}} % pystyviiva
\put(53,739){\line(1,0){462}}
\put(53,709){\line(1,0){462}}
\put(53,679){\line(1,0){462}}
\put(53,649){\line(1,0){462}}
\put(207,649){\line(0,1){30}} % pystyviiva
\put(361,649){\line(0,1){30}} % pystyviiva


\put(53,80){\line(1,0){462}}
\put(53,110){\line(1,0){462}}
\put(53,140){\line(1,0){462}}



\put(53,781){\makebox(100,8)[l]{\abst@small HELSINGIN YLIOPISTO --- HELSINGFORS UNIVERSITET --- UNIVERSITY OF HELSINKI}}
\put(58,767){\makebox(150,6)[l]{\tiny Tiedekunta --- Fakultet --- Faculty}}
\put(289,767){\makebox(100,6)[l]{\abst@tiny Koulutusohjelma --- Utbildningsprogram --- Degree programme}}
\put(58,730){\makebox(100,5)[l]{\abst@tiny Tekij\"a --- F\"orfattare --- Author}}
\put(58,700){\makebox(100,5)[l]{\abst@tiny Ty\"on nimi --- Arbetets titel --- Title}}
\put(58,670){\makebox(100,5)[l]{\abst@tiny Ty\"on laji --- Arbetets art --- Level}}
\put(212,670){\makebox(100,5)[l]{\abst@tiny Aika --- Datum --- Month and year }}
\put(366,670){\makebox(100,5)[l]{\abst@tiny Sivum\"a\"ar\"a --- Sidantal --- Number of pages}}

\put(58,640){\makebox(100,5)[l]{\abst@tiny Tiivistelm\"a --- Referat --- Abstract}}
\put(58,131){\makebox(100,5)[l]{\abst@tiny Avainsanat --- Nyckelord --- Keywords}}
\put(58,101){\makebox(100,5)[l]{\abst@tiny S\"ailytyspaikka --- F\"orvaringsst\"alle --- Where deposited}}
\put(58,71){\makebox(100,5)[l]{\abst@tiny Muita tietoja --- \"Ovriga uppgifter --- Additional information}}
\end{picture}

\clearpage
\pagestyle{empty}
\if@twoside
	\newpage
	\thispagestyle{empty}
	\cleardoublepage
\fi

\ifdefined\@quoting
	\thispagestyle{empty}
	\pagebreak
	\hspace{0pt}
	\vfill
	\noindent \@quoting
	\vfill
	\hspace{0pt}
	\pagebreak
\fi
}

\if@finnish
\faculty{Matemaattis-luonnontieteellinen tiedekunta}
%\level{Maisterin tutkielma}
\level{Raportti}
% programme specific content starts
\programme{Datatieteen maisteriohjelma}
%\subject{Erikoistumislinja}
\address{PL 68 (Pietari Kalmin katu 5)\\00014 Helsingin yliopisto}
% programme specific content ends
\fi

\if@english
\faculty{Faculty of Science}
%\level{Master's thesis}
\level{Report}
\programme{Master's Programme in Data Science}
%\subject{Subprogramme}
\address{P. O. Box 68 (Pietari Kalmin katu 5)\\00014 University of Helsinki}
\fi

\if@swedish
\faculty{Matematisk-naturvetenskapliga fakulteten}
%\level{Magisteravhandling}
\level{Rapport}
\programme{Magisterprogrammet i data science}
%\subject{Studieinriktning}
\address{PB 68 (Pehr Kalms gata 5)\\00014 Helsingfors universitet}
% programme specific content ends
\fi



\endinput
%%
%% End of file
