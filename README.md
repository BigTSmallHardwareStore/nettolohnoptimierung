# Nettolohnoptimierung

**Erklärung**

Mithilfe von diesem Tool lässt sich neben dem Nettolohn für Deutschland für 2022 auch der Nettolohngrenzverdienst berechnen, das heißt in der erzeugten Tabelle ist eine Spalte vorhanden, die anzeigt, wie viel man in der jeweiligen folgenden Stunde netto verdient. Dieses Kriterium dient neben dem Durchschnittslohn, welcher für alle Stunden gleich ist, als Entscheidungshilfe, ob es für einen persönlich mehr Lebensfreude bereitet auf zum Beispiel die 40. Wochenstunde zu verzichten und die Zeit mit Freunden und Familie zu verbringen, da der Nettostundenlohn für diese eine Stunde Mehrarbeit für einen persönlich nicht lohnend ist oder nicht.

Die Hauptbedienung erfolgt über das Terminal mittels User-Input. Für die meisten Felder sind Default-Werte hinterlegt, welche in Klammern angegeben sind.

**Bemerkungen und derzeitige Einschränkungen**

Derzeit sind nur die Bemessungsgrundlagen der alten Bundesländer hinterlegt. Eine Berechnung für die Lohnsteuerklasse 6 ist nicht möglich, da die primäre Idee für dieses Programm die Optimierung des Nettolohnes der Haupteinkommensquelle ist. Aktuell können nur die Nettolöhne für gesetzlich Versicherte errechnet werden. Die Möglichkeit der privaten (Kranken-) Versicherung ist noch nicht implementiert. Die Berechnung der Lohnsteuer erfolgt über die Schnittstelle des BMF, welche bei der Steuerberechnung Abweichungen im Cent-Bereich aufweist. Es ist eine Sleep-Funktion mit einem Zufallsbereich von 5 bis 15 Sekunden eingebaut, um die Anfragen an den Server sehr gering zu halten und eine Überlastung zu vermeiden, weshalb das Programm ein paar Minuten benötigt, bis es alle Anfragen durchgeführt hat. Am besten Kaffee holen und zurücklehnen ;)

Der Code darf von jedem verwendet und gern nach Belieben weiterentwickelt werden. Viel Spaß :) 
Über Tipps und Anmerkungen würde ich mich freuen.
