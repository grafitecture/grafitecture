# Inhalts-Empfehlungen für Suche und KI-Antworten (Phase 7.3)

Stand 05.11.2026. **Nichts davon ist umgesetzt** – das sind Vorschläge für Martin. Technik, Markup und strukturierte
Daten sind erledigt; was jetzt noch Sichtbarkeit bringt, sind Inhalte. Reihenfolge nach erwartetem Nutzen.

## 1. Referenzen lesbar machen (größter Hebel)

Heute stehen 29 Kunden als Logos da. Suchmaschinen und KI-Systeme sehen davon nur die Namen im `alt`-Text, aber nicht,
**was** Grafitecture für wen gebaut hat. Antwortmaschinen zitieren konkrete Fälle („Agentur X hat für Y eine
Content-Engine gebaut, die …“).

- Drei bis fünf Fallbeispiele mit je 2–3 Sätzen: Kunde, Branche, Aufgabe, was gebaut wurde, ein Ergebnis mit Zahl
  (z. B. Beiträge pro Monat, gesparte Stunden, Zeit bis zum Launch).
- Ideal als eigene Seiten (`/referenzen/<kunde>`), sonst als Text unter den Logos.

## 2. Erster Absatz: Wer, was, für wen, wo

Der Hero-Text sagt *was* (KI-Agenten, Websites, Content-Engines) und die Erfahrung, nennt aber weder Firmennamen noch
Ort; beides steht erst in „Über mich“ und im Footer. KI-Systeme gewichten den Anfang einer Seite stark.

- Vorschlag (nur Formulierungsidee): „Grafitecture in Mannheim baut KI-Systeme für Marken: autonome KI-Agenten,
  KI-gestützte Websites und Content-Engines für Mittelständler und Praxen. Seit 2000, von Diplom-Designer Martin
  Schweppe.“

## 3. Häufige Fragen (FAQ) als sichtbarer Abschnitt

Echte Fragen, die Interessenten stellen, mit kurzen, eigenständigen Antworten. Das sind genau die Sätze, die
ChatGPT, Perplexity und Google AI Overviews zitieren. Beispiele:

- Was kostet eine KI-Website / ein KI-Agent ungefähr? (Preisrahmen statt „klare Preise“)
- Wie lange dauert ein Projekt vom Erstgespräch bis zur Übergabe?
- Wo laufen die Systeme, und was passiert mit unseren Daten (DSGVO, Hosting in der EU)?
- Brauchen wir eigene Entwickler, um das System zu betreiben?
- Für welche Branchen arbeiten Sie? (Gesundheit, Gastronomie, Finanzen, Logistik stehen schon auf der Seite.)

Das `FAQPage`-Markup ergänze ich dann technisch (Google zeigt seit Mai 2026 keine FAQ-Rich-Results mehr, das Markup
hilft aber beim Verständnis).

## 4. Konkrete Fakten statt Adjektive

- Preisrahmen oder Einstiegspreise je Leistung.
- Typische Projektdauer (die Seite sagt „Wochen statt Monate“ – eine Zahl wäre zitierfähiger).
- Werkzeuge und Plattformen, mit denen gebaut wird (z. B. Claude, GitHub, Vercel): KI-Systeme ordnen Anbieter gern
  danach ein.

## 5. Einheitliche Firmendaten (NAP) und Profile

- Name, Adresse und ggf. Telefonnummer überall gleich: Website, Google-Unternehmensprofil, LinkedIn, Branchenbücher.
- Eine Telefonnummer auf der Seite würde Vertrauen und lokale Suche stärken (heute nur E-Mail). Erst dann kommt sie
  ins JSON-LD.
- LinkedIn (Martin und Firma) und das Google-Unternehmensprofil als `sameAs` ergänzen – bitte die Links schicken.

## 6. „Über mich“ als Entität stärken

Vorhanden und gut: Abschluss, Firma, Standort, „seit 2000“. Ergänzen könnte man: Studium (wo/wann), frühere
Stationen, Auszeichnungen, Vorträge, Veröffentlichungen. Die Überschrift „Human in the loop.“ ist stark als Gestaltung,
sagt Maschinen aber nicht, worum es geht – die Zeile darunter („Ich baue KI, die arbeitet …“) trägt das.

## 7. Später: Fachinhalte mit Autor und Datum

Wenn ein Blog oder „Einblicke“ geplant ist: jeder Beitrag mit Autor (Martin Schweppe), Veröffentlichungs- und
Änderungsdatum, Quellen. Die Technik dafür (Article-Markup, Sitemap, Canonical) ist vorbereitet.
