# XFactor

Projektbeschreibung sowie Guide für GIT

## User Guide GitHUB

### Synchronisierung Lokal + Setup

einen lokalen Ordner auf eurem Rechner erstellen wo der ganze Code drin landen soll

> git mit den Standardeinstellungen installieren <https://git-scm.com/>

im datei-explorer rechtsklick -> open git bash here
>`git clone https://github.com/Simmsel/XFactor`

### Aktualisierungen vom server runterladen

diesen teil am besten jedes Mal / jeden Tag machen, bevor ihr selber zum coden anfängt, damit ihr den aktuellsten stand habt und es zu keinen problemen beim hochladen kommt
im lokalen Ordner rechtsklick -> open git bash here  
`git pull`
>Achtung, dieser Schritt überschreibt lokale Änderungen die nicht hochgeladen sind. Wenn ihr gleichzeitig mit wem anders was gecoded habt dann erst `git fetch` und `git merge` machen um konflikte zu lösen und dann erst committen und pushen

### Status prüfen

`git status`
> schauen was aktuell geändert ist, ob ihr den aktuellen stand habt etc.

### Eigene änderungen auf den server packen

1. lokale änderungen übertragen  
`git add .`

2. lokal comitten  
`git commit -m "beschreibung was gemacht wurde"`

3. änderungen auf den server pushen (wenn ihr euch sicher seid)  
`git push origin main`
