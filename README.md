# CFPP2000-to-TSV

Outil pour convertir le corpus **CFPP2000** (XML) en un fichier tabulaire **dataset.tsv**.

## Installation
git clone https://github.com/yourusername/CFPP2000-to-TSV.git
cd CFPP2000-to-TSV

## Prérequis
Python 3.x

## Utilisation
python run_converter.py

Un fichier **dataset.tsv** sera généré à la racine du projet. Il peut être ouvert dans Python (pandas), R ou Excel.

## Exemple de sortie
| filename                    | duration | format | sample_rate | speakers                                | transcript                                |
|-----------------------------|----------|--------|-------------|----------------------------------------|-------------------------------------------|
| Alice_Cherviel_F_28_17e.mp3 | 46.06    | mp3    | 44100       | Sonia Branca-Rosoff (ENQ), Alice, spk3 | et voilà + bon alors ma première question |

## Structure du projet
/
├── README.md
├── dataset.tsv
└── run_converter.py

## Licence
MIT
