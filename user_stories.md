
1) Als Entwickler von Spezialsoftware (hops, cadet, fluxtopus) möchte ich einfach neue Notebookkernel erstellen können um meinen Anwendern einfach Zugriff auf die aktuellste Version meiner Software zu geben
2) Als Wissenschaflter möchte ich Berechnungen und Ergebnisse innerhalb vom Jupyterhub mit anderen Nutzern teilen um gemeinsam an der Auswertung wissenschaftlicher Daten und Simulationen zu arbeiten. (Stichwort Live Collaboration)
3) Als Workshopleiter (cadet) möchte ich Workshopteilnehmern schnell Zugriff (eigene User-Verwaltung) auf eine definierte Compute Umgebung geben können, damit Beispiele gerechnet werden können, ohne dass vorher auf den Systemen der User software installiert/kompiliert werden muss.


Constraints: 
1) Die Jupyterhubs sollten auf unseren eigenen Clusterknoten laufen (Damit können wir agiler rechnen, ohne dass wir Anträge stellen müssten)
2) Es müssen eigene Python-Kernel, die sich oft ändern können, zur Verfügung stehen
3) Der JupyterSpawner sollte auch vordefinierte Docker Images (gebaut in CI pipelines, gehostet in einer privaten container registry), die sich oft ändern können. (Debug-Versionen, Pre-Release oder Develop-branches)
4) Nutzer sind sowohl Interne (also im FZJ LDAP), als auch Externe (Workshopteilnehmer, Kollaborationsparter (Forschungs + Industrie))


Über das user management wollen wir abbilden können, wer auf welche unserer Compute-Nodes zugreifen kann
-CPU-Knoten
-high RAM Knoten
-GPU-Cluster

Am liebsten würden wir uns an den Jupyter-Server des JSC dranhängen. Möglicherweise ginge das über einen Pull Request für deren Custom Spawner.
