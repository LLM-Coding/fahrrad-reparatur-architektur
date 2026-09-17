<div class="row flex-xl-nowrap">
    <main class="col-12 col-md-12 col-xl-12 pl-md-12" role="main">

        <!-- Hero -->
        <section class="row align-items-center py-4 mb-4">
            <div class="col-lg-6 mb-4 mb-lg-0">
                <h1 class="display-4">Wir bauen eine Software-Architektur</h1>
                <p class="lead">
                    Architekturdokumentation und ADRs zu Eberhard Wolffs Architektur-Kata
                    Fahrrad-Reparatur-System, software-architektur.tv Folgen 111 bis 113.
                </p>
                <p>
                    <a class="btn btn-primary btn-lg mr-2 mb-2" href="arc42/chapters/09_architecture_decisions.html">Zu den Entscheidungen</a>
                    <a class="btn btn-outline-secondary btn-lg mb-2" href="arc42/chapters/01_introduction_and_goals.html">Einf&uuml;hrung</a>
                </p>
            </div>
            <div class="col-lg-6 text-center">
                <!-- Hero-Bild, generiert (flache Illustration, keine Lizenzbindung) -->
                <img src="images/landingpage-hero.png" alt="Fahrradwerkstatt mit Montagest&auml;nder, Zahnr&auml;dern und Bausteinen" class="img-fluid rounded" width="1536" height="576">
            </div>
        </section>

        <!-- Kacheln -->
        <section class="row">

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: einfuehrung -->
                        <img src="images/icons/einfuehrung.png" alt="" width="56" height="56" class="mb-2">
                        <h2 class="h5 card-title">Einf&uuml;hrung und Ziele</h2>
                        <p class="card-text">Was das Fahrrad-Reparatur-System leisten soll und welche Qualit&auml;tsziele die Architektur pr&auml;gen.</p>
                        <a href="arc42/chapters/01_introduction_and_goals.html" class="stretched-link">Kapitel 1</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: kontext -->
                        <img src="images/icons/kontext.png" alt="" width="56" height="56" class="mb-2">
                        <h2 class="h5 card-title">Kontext</h2>
                        <p class="card-text">Wer mit dem System arbeitet und welche Nachbarsysteme es anbindet: Webshop, Kasse, Zahlungsdienst, Rechnungswesen.</p>
                        <a href="arc42/chapters/03_context_and_scope.html" class="stretched-link">Kapitel 3</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: bausteine -->
                        <img src="images/icons/bausteine.png" alt="" width="56" height="56" class="mb-2">
                        <h2 class="h5 card-title">Bausteine</h2>
                        <p class="card-text">Wie das System in Module zerf&auml;llt und welche Verantwortung jeder Baustein tr&auml;gt.</p>
                        <a href="arc42/chapters/05_building_block_view.html" class="stretched-link">Kapitel 5</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: entscheidungen -->
                        <img src="images/icons/entscheidungen.png" alt="" width="56" height="56" class="mb-2">
                        <h2 class="h5 card-title">Entscheidungen</h2>
                        <p class="card-text">Die ADRs aus den drei Folgen: welche Optionen zur Wahl standen und warum eine gewonnen hat.</p>
                        <a href="arc42/chapters/09_architecture_decisions.html" class="stretched-link">Kapitel 9</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: qualitaet -->
                        <img src="images/icons/qualitaet.png" alt="" width="56" height="56" class="mb-2">
                        <h2 class="h5 card-title">Qualit&auml;t</h2>
                        <p class="card-text">Messbare Qualit&auml;tsszenarien f&uuml;r Benutzbarkeit, Zuverl&auml;ssigkeit und &Auml;nderbarkeit, mit Bezug zu den ADRs.</p>
                        <a href="arc42/chapters/10_quality_requirements.html" class="stretched-link">Kapitel 10</a>
                    </div>
                </div>
            </div>

            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <!-- Icon: risiken -->
                        <img src="images/icons/risiken.svg" alt="" width="56" height="56" class="mb-2">
                        <h2 class="h5 card-title">Risiken</h2>
                        <p class="card-text">Offene Risiken und technische Schulden, priorisiert nach Wahrscheinlichkeit und Auswirkung.</p>
                        <a href="arc42/chapters/11_technical_risks.html" class="stretched-link">Kapitel 11</a>
                    </div>
                </div>
            </div>

        </section>

        <!-- Entscheidungslandkarte -->
        <section class="row mt-4 mb-4">
            <div class="col-12">
                <h2 class="h3">Die Entscheidungslandkarte</h2>
                <p>
                    17 Entscheidungen sind gefallen, eine ist vertagt, sechs sind offen. Die Karte zeigt, welche
                    Entscheidung auf welcher beruht und wo die Front der offenen Entscheidungen verl&auml;uft.
                </p>
                <a href="arc42/chapters/09_architecture_decisions.html" title="Entscheidungslandkarte, Kapitel 9">
                    <img src="images/09-entscheidungslandkarte.svg" alt="Entscheidungslandkarte der Architekturentscheidungen" class="img-fluid rounded border">
                </a>
                <p class="small text-muted mt-2 mb-0">
                    <span style="display:inline-block;width:.9em;height:.9em;background:#c8e6c9;border:1px solid #2e7d32;vertical-align:middle"></span> gefallen &nbsp;
                    <span style="display:inline-block;width:.9em;height:.9em;background:#fff59d;border:1px solid #f9a825;vertical-align:middle"></span> vertagt &nbsp;
                    <span style="display:inline-block;width:.9em;height:.9em;background:#ffcdd2;border:1px solid #c62828;vertical-align:middle"></span> offen
                </p>
            </div>
        </section>

        <!-- Quellen -->
        <footer class="border-top pt-3 mt-2 small text-muted">
            <p class="mb-1"><strong>Quellen:</strong>
                software-architektur.tv
                <a href="https://software-architektur.tv/2022/02/25/folge111.html">Folge 111</a>,
                <a href="https://software-architektur.tv/2022/03/11/folge112.html">Folge 112</a>,
                <a href="https://software-architektur.tv/2022/03/25/folge113.html">Folge 113</a>
                sowie das Repository
                <a href="https://github.com/LLM-Coding/fahrrad-reparatur-architektur">LLM-Coding/fahrrad-reparatur-architektur</a>.
            </p>
            <p class="mb-0">Titelbild und Icons: generiert (gpt-image-2), Risiken-Icon von Hand als SVG.</p>
        </footer>

    </main>
</div>
